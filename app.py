import streamlit as st
import sqlite3
import pandas as pd

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

    source = st.selectbox(
        "Source",
        [
            "LinkedIn",
            "Seek",
            "Indeed",
            "Other"
        ]
    )

    url = st.text_input("Job URL")

    application_date = st.date_input(
        "Application Date"
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

        # ------------------------
        # STATUS EMOJIS
        # ------------------------

        def status_emoji(status):

            mapping = {
                "New": "🟡",
                "Applied": "🔵",
                "Interview": "🟣",
                "Rejected": "🔴",
                "Offer": "🟢"
            }

            return mapping.get(
                status,
                "⚪"
            )

        display_df = filtered_df.copy()

        display_df["status"] = (
            display_df["status"]
            .apply(
                lambda x:
                f"{status_emoji(x)} {x}"
            )
        )

        st.dataframe(
            display_df,
            use_container_width=True
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
