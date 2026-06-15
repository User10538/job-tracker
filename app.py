import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

from utils.helpers import (
    detect_source,
    open_job_link,
    status_emoji
)

from utils.database import (
    add_column_if_missing
)

DB = "jobs.db"

# ------------------------
# DATABASE
# ------------------------

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

add_column_if_missing(
    cursor,
    conn,
    "interview_date"
)

add_column_if_missing(
    cursor,
    conn,
    "followup_date"
)

add_column_if_missing(
    cursor,
    conn,
    "job_description"
)

# ------------------------
# PAGE CONFIG
# ------------------------

st.set_page_config(
    page_title="Personal Job Tracker",
    layout="wide"
)

st.title("📋 Personal Job Tracker")

# ------------------------
# TABS
# ------------------------

tab1, tab2 = st.tabs(
    ["Add Job", "View Jobs"]
)

# ------------------------
# ADD JOB
# ------------------------

with tab1:

    st.subheader("Add a Job")

    title = st.text_input("Job Title")

    company = st.text_input("Company")

    url = st.text_input("Job URL")

    source = detect_source(url)

    st.info(f"Detected Source: {source}")

    application_date = st.date_input(
        "Application Date",
        value=date.today()
    )

    interview_date = st.date_input(
    "Interview Date",
    value=date.today()
    )

    followup_date = st.date_input(
        "Follow-up Date",
        value=date.today()
    )

    status = st.selectbox(
        "Status",
        [
            "New",
            "Applied",
            "Interview",
            "Rejected",
            "Offer"
        ]
    )

    notes = st.text_area("Notes")

    job_description = st.text_area(
    "Job Description",
    height=250
    )

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
                interview_date,
                followup_date,
                status,
                notes,
                job_description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                company,
                source,
                url,
                str(application_date),
                str(interview_date),
                str(followup_date),
                status,
                notes,
                job_description
            )
        )

        conn.commit()

        st.success("Job saved!")

# ------------------------
# VIEW JOBS
# ------------------------

with tab2:

    df = pd.read_sql_query(
        "SELECT * FROM jobs ORDER BY id DESC",
        conn
    )

    # ------------------------
    # SIDEBAR METRICS
    # ------------------------

    st.sidebar.title("Dashboard")

    total_jobs = len(df)

    applied = len(
        df[df["status"] == "Applied"]
    )

    interviews = len(
        df[df["status"] == "Interview"]
    )

    offers = len(
        df[df["status"] == "Offer"]
    )

    st.sidebar.metric(
        "Total Jobs",
        total_jobs
    )

    st.sidebar.metric(
        "Applied",
        applied
    )

    st.sidebar.metric(
        "Interviews",
        interviews
    )

    st.sidebar.metric(
        "Offers",
        offers
    )

    st.sidebar.divider()

    st.sidebar.subheader(
        "Upcoming Interviews"
    )

    interview_jobs = df[
        df["status"] == "Interview"
    ]

    if not interview_jobs.empty:

        for _, row in interview_jobs.iterrows():

            st.sidebar.write(
                f"📅 {row['company']}"
            )

            st.sidebar.caption(
                row["interview_date"]
            )

    else:

        st.sidebar.write(
            "No interviews scheduled"
        )

    st.subheader("Tracked Jobs")

    if not df.empty:

        # ------------------------
        # TOP METRICS
        # ------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Jobs",
            total_jobs
        )

        col2.metric(
            "Applied",
            applied
        )

        col3.metric(
            "Interviews",
            interviews
        )

        col4.metric(
            "Offers",
            offers
        )

        st.divider()

        # ------------------------
        # FILTER
        # ------------------------

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

        filtered_df = df.copy()

        if selected_status != "All":

            filtered_df = filtered_df[
                filtered_df["status"]
                == selected_status
            ]

        search = st.text_input(
            "Search Job Title or Company"
        )

        if search:

            filtered_df = filtered_df[
                filtered_df["title"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered_df["company"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        display_df = filtered_df.copy()

        display_df["status"] = display_df["status"].apply(
            lambda x: f"{status_emoji(x)} {x}"
        )

        table_df = display_df.drop(
            columns=[
                "id",
                "url",
                "job_description"
            ],
            errors="ignore"
        )

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )
        # ------------------------
        # EXPORT
        # ------------------------

        csv = filtered_df.to_csv(
            index=False
        )

        st.download_button(
            "Download CSV",
            csv,
            "jobs.csv",
            "text/csv"
        )

        st.divider()

        # ------------------------
        # UPDATE STATUS
        # ------------------------

        st.subheader(
            "Update Job Status"
        )

        job_options = {
            f"{row['company']} - {row['title']}":
            row['id']
            for _, row
            in df.iterrows()
        }

        selected_label = st.selectbox(
            "Select Job",
            list(job_options.keys())
        )

        selected_job = job_options[
            selected_label
        ]

        current_job = df[
            df["id"] == selected_job
        ].iloc[0]

        open_job_link(current_job["url"])

        statuses = [
            "New",
            "Applied",
            "Interview",
            "Rejected",
            "Offer"
        ]

        new_status = st.selectbox(
            "New Status",
            statuses,
            index=statuses.index(
                current_job["status"]
            )
        )

        col_a, col_b = st.columns(2)

        with col_a:

            if st.button(
                "Update Status"
            ):

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
                    "Status updated!"
                )

                st.rerun()

        with col_b:

            if st.button(
                "Delete Job"
            ):

                cursor.execute(
                    """
                    DELETE FROM jobs
                    WHERE id = ?
                    """,
                    (
                        int(selected_job),
                    )
                )

                conn.commit()

                st.success(
                    "Job deleted!"
                )

                st.rerun()

        # ------------------------
        # FUNNEL
        # ------------------------

        st.divider()

        st.subheader(
            "Application Funnel"
        )

        funnel_data = pd.DataFrame(
            {
                "Count": [
                    applied,
                    interviews,
                    offers
                ]
            },
            index=[
                "Applied",
                "Interview",
                "Offer"
            ]
        )

        st.bar_chart(
            funnel_data
        )

    else:

        st.info(
            "No jobs added yet."
        )
