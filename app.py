import streamlit as st
import sqlite3
import pandas as pd

DB = "jobs.db"

# Database setup
conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    source TEXT,
    url TEXT,
    application_date TEXT,
    status TEXT,
    notes TEXT
)
""")
conn.commit()

st.set_page_config(page_title="Job Tracker", layout="wide")

st.title("📋 Personal Job Tracker")

tab1, tab2 = st.tabs(["Add Job", "View Jobs"])

with tab1:
    st.subheader("Add a Job")

    title = st.text_input("Job Title")
    company = st.text_input("Company")

    source = st.selectbox(
        "Source",
        ["LinkedIn", "Seek", "Indeed", "Other"]
    )

    url = st.text_input("Job URL")

    application_date = st.date_input(
        "Application Date"
    )

    status = st.selectbox(
        "Status",
        ["New", "Applied", "Interview", "Rejected", "Offer"]
    )

    notes = st.text_area("Notes")

    if st.button("Save Job"):

        cursor.execute(
            """
            INSERT INTO jobs
            (
                title,
                company,
                source,
                url,
                application_date,
                status,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                company,
                source,
                url,
                str(application_date),
                status,
                notes
            )
        )

        conn.commit()

        st.success("Job saved!")

with tab2:

    st.subheader("Tracked Jobs")

    df = pd.read_sql_query(
        "SELECT * FROM jobs ORDER BY id DESC",
        conn
    )

    if not df.empty:

        # Dashboard Stats
        total_jobs = len(df)
        applied = len(df[df["status"] == "Applied"])
        interviews = len(df[df["status"] == "Interview"])
        offers = len(df[df["status"] == "Offer"])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Jobs", total_jobs)
        col2.metric("Applied", applied)
        col3.metric("Interviews", interviews)
        col4.metric("Offers", offers)

        st.divider()

        # Status Filter
        selected_status = st.selectbox(
            "Filter by Status",
            [
                "All",
                "New",
                "Applied",
                "Interview",
                "Rejected",
                "Offer"
            ]
        )

        if selected_status != "All":
            df = df[df["status"] == selected_status]

        # Search Box
        search = st.text_input(
            "Search Job Title or Company"
        )

        if search:
            df = df[
                df["title"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                df["company"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
    df,
    use_container_width=True
)

st.divider()
st.subheader("Update Job Status")

job_ids = df["id"].tolist()

if job_ids:

    selected_job = st.selectbox(
        "Select Job ID",
        job_ids
    )

    current_job = df[df["id"] == selected_job].iloc[0]

    st.write(
        f"**{current_job['title']}** at **{current_job['company']}**"
    )

    new_status = st.selectbox(
        "New Status",
        [
            "New",
            "Applied",
            "Interview",
            "Rejected",
            "Offer"
        ],
        index=[
            "New",
            "Applied",
            "Interview",
            "Rejected",
            "Offer"
        ].index(current_job["status"])
    )

    if st.button("Update Status"):

        cursor.execute(
            """
            UPDATE jobs
            SET status = ?
            WHERE id = ?
            """,
            (
                new_status,
                int(selected_job)
            )
        )

        conn.commit()

        st.success(
            f"Job {selected_job} updated to {new_status}"
        )

        st.rerun()
        
        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "jobs.csv",
            "text/csv"
        )

    else:
        st.info("No jobs added yet.")
