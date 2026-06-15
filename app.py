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

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Jobs",
            len(df)
        )

        col2.metric(
            "Applied",
            len(df[df["status"] == "Applied"])
        )

        col3.metric(
            "Interviews",
            len(df[df["status"] == "Interview"])
        )

        col4.metric(
            "Offers",
            len(df[df["status"] == "Offer"])
        )

        search = st.text_input(
            "Search Company or Job"
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

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "jobs.csv",
            "text/csv"
        )

    else:
        st.info("No jobs added yet.")
