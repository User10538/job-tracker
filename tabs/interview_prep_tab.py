"""
Interview Preparation tab
"""

import sqlite3
import streamlit as st
import pandas as pd


def show():
    conn = sqlite3.connect("jobs.db")

    df = pd.read_sql_query(
        """
        SELECT *
        FROM jobs
        WHERE status = 'Interview'
        ORDER BY interview_date
        """,
        conn
    )

    st.subheader("🎤 Interview Preparation")

    if df.empty:
        st.info("No upcoming interviews.")
        return

    selected_job = st.selectbox(
        "Select Interview",
        [
            f"{row['company']} - {row['title']}"
            for _, row in df.iterrows()
        ],
        key="interview_select"
    )

    current_job = df[
        (
            df["company"] + " - " + df["title"]
        ) == selected_job
    ].iloc[0]

    st.divider()

    st.write(f"**Company:** {current_job['company']}")
    st.write(f"**Role:** {current_job['title']}")
    st.write(f"**Interview Date:** {current_job['interview_date']}")

    st.divider()

    st.subheader("Recruiter Notes")
    st.text_area(
        "",
        value=current_job.get("recruiter_notes", ""),
        height=200,
        disabled=True
    )

    st.subheader("AI Interview Prompt")
    st.text_area(
        "",
        value=current_job.get("ai_prompt", ""),
        height=300,
        disabled=True
    )
