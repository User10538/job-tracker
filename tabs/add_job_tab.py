'''
ADD JOBS tab1
'''

import sqlite3
import os
from datetime import date
import streamlit as st
import pandas as pd

from utils.helpers import (
    detect_source,
    extract_keywords,
    generate_recruiter_notes
)

DB = "jobs.db"
conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()

df = pd.read_sql_query(
    "SELECT * FROM jobs ORDER BY id DESC",
    conn
    )

def show():
    st.subheader("Add a Job")

    title = st.text_input("Job Title")
    company = st.text_input("Company")
    url = st.text_input("Job URL")
    st.write("Before detect_source")

    source = detect_source(url)

    st.write("Source =", source)

    st.info(f"Detected Source: {source}")

    application_date = st.date_input("Application Date", value=date.today())
    interview_date = st.date_input("Interview Date", value=date.today())
    followup_date = st.date_input("Follow-up Date", value=date.today())

    status = st.selectbox("Status",
        ["New","Applied","Interview","Rejected","Offer"])

    notes = st.text_area("Notes", key="new_notes")
    resume_file = st.file_uploader("Resume Used", type=["pdf","docx"])
    job_description = st.text_area("Job Description", height=250)

    keywords = ""
    recruiter_notes = ""
    ai_prompt = ""

    if job_description:
        keywords = extract_keywords(job_description)
        recruiter_notes = generate_recruiter_notes(keywords)

        ai_prompt = f"""Analyze this job description:

{job_description}

Provide:
1. Job Summary
2. Recruiter Questions
3. Technical Questions
4. Key Skills
5. Interview Preparation Notes
"""

        st.subheader("Recruiter Cheat Sheet")
        st.text_area("Recruiter Notes", recruiter_notes, height=250)
        st.success(f"Keywords: {keywords}")
        st.subheader("🤖 ChatGPT Prompt")
        st.code(ai_prompt)

        if st.button("Save Job"):
            try:
                resume_path = ""

                if resume_file:
                    os.makedirs("resumes", exist_ok=True)
                    resume_path = os.path.join("resumes", resume_file.name)

                    with open(resume_path, "wb") as f:
                        f.write(resume_file.getbuffer())

                cursor.execute("""
                INSERT INTO jobs (
                    title, company, source, url,
                    application_date, interview_date,
                    followup_date, status, notes,
                    job_description, keywords,
                    recruiter_notes, ai_prompt,
                    resume_file
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    title, company, source, url,
                    str(application_date),
                    str(interview_date),
                    str(followup_date),
                    status, notes,
                    job_description, keywords,
                    recruiter_notes, ai_prompt,
                    resume_path
                ))

                conn.commit()
                st.success("Job saved!")

            except Exception as e:
                st.exception(e)
