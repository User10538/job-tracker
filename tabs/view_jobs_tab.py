from datetime import date
import streamlit as st
import pandas as pd
import sqlite3
import os

from utils.helpers import (
    open_job_link,
    status_emoji
)
# ------------------------
# VIEW JOBS
# ------------------------
def show():
    DB = "jobs.db"

    conn = sqlite3.connect(DB, check_same_thread=False)
    cursor = conn.cursor()

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

    rejected = len(
        df[df["status"] == "Rejected"]
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
        "Rejected",
        rejected
    )

    st.sidebar.metric(
        "Interviews",
        interviews
    )

    #st.sidebar.metric(
    #    "Offers",
    #    offers
    #)

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
                "job_description",
                "keywords",
                "recruiter_notes",
                "ai_prompt"
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

        resume_path = current_job.get(
            "resume_file",
            ""
        )

        if (
            resume_path
            and os.path.exists(resume_path)
        ):

            st.subheader(
                "📄 Resume Used"
            )

            st.write(
                os.path.basename(
                    resume_path
                )
            )

            with open(
                resume_path,
                "rb"
            ) as file:

                st.download_button(
                    "📥 Download Resume",
                    file,
                    file_name=os.path.basename(
                        resume_path
                    ),
                    key=f"download_resume_{selected_job}"
                )

        
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
        # Edit the Job details
        # ------------------------

        st.divider()

        st.subheader("Edit Job Details")

        edit_title = st.text_input(
            "Job Title",
            value=current_job["title"],
            key=f"edit_title_{selected_job}"
        )

        edit_company = st.text_input(
            "Company",
            value=current_job["company"],
            key=f"edit_company_{selected_job}"

        )

        edit_url = st.text_input(
            "URL",
            value=current_job["url"],
            key=f"edit_url_{selected_job}"
        )

        edit_notes = st.text_area(
            "Notes",
            value=current_job["notes"],
            key=f"edit_notes_{selected_job}"
        )

        edit_job_description = st.text_area(
            "Job Description",
            value=current_job["job_description"],
            height=250,
            key=f"edit_job_description_{selected_job}"
        )

        edit_keywords = st.text_area(
            "Keywords",
            value=current_job["keywords"],
            height=100,
            key=f"edit_keywords_{selected_job}"
        )

        edit_recruiter_notes = st.text_area(
            "Edit Recruiter Notes",
            value=current_job["recruiter_notes"],
            height=250,
            key=f"edit_recruiter_notes_{selected_job}"
        )

        edit_ai_prompt = st.text_area(
            "AI Prompt",
            value=current_job["ai_prompt"],
            height=300,
            key=f"edit_ai_prompt_{selected_job}"
        )

        edit_interview_date = st.text_input(
            "Interview Date",
            value=current_job["interview_date"],
            key=f"edit_interview_date_{selected_job}"
        )

        edit_followup_date = st.text_input(
            "Follow-up Date",
            value=current_job["followup_date"],
            key=f"edit_followup_date_{selected_job}"
        )

        st.divider()

        st.subheader("🤖 AI Prompt")

        if current_job["ai_prompt"]:


            st.code(
                current_job["ai_prompt"],
                language="text"
            )

        st.text_area(
            "Copy into ChatGPT",
            value=current_job["ai_prompt"],
            height=300,
            key="view_ai_prompt"
        )

        if st.button("💾 Save Changes"):
            cursor.execute(
                    """
                    UPDATE jobs
                    SET
                        title = ?,
                        company = ?,
                        url = ?,
                        notes = ?,
                        interview_date = ?,
                        followup_date = ?,
                        job_description = ?,
                        keywords = ?,
                        recruiter_notes = ?,
                        ai_prompt = ?
                    WHERE id = ?
                    """,
                    (
                        edit_title,
                        edit_company,
                        edit_url,
                        edit_notes,
                        edit_interview_date,
                        edit_followup_date,
                        edit_job_description,
                        edit_keywords,
                        edit_recruiter_notes,
                        edit_ai_prompt,
                        int(selected_job)
                    )
                )
            conn.commit()
            
            st.success(
                    "Changes saved!"
                )

            st.rerun()
