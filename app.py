import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

from utils.helpers import (
    detect_source,
    open_job_link,
    status_emoji,
    extract_keywords,
    generate_recruiter_notes
)

from tabs.funnel_tab import show as show_funnel
from tabs.interview_prep_tab import show as show_interview_prep
from tabs.view_jobs_tab import show as show_view_jobs

from utils.database import (add_column_if_missing)

DB = "jobs.db"

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

for col in [
    "interview_date","followup_date","job_description",
    "keywords","recruiter_notes","ai_prompt","resume_file"
]:
    add_column_if_missing(cursor, conn, col)

st.set_page_config(page_title="Personal Job Tracker", layout="wide")
st.title("📋 Personal Job Tracker")

conn = sqlite3.connect("jobs.db")

df = pd.read_sql_query(
    "SELECT * FROM jobs",
    conn
)

applied = len(df[df["status"] == "Applied"])
interviews = len(df[df["status"] == "Interview"])
offers = len(df[df["status"] == "Offer"])
rejected = len(df[df["status"] == "Rejected"])

tab1, tab2, tab3, tab4 = st.tabs(["Add Job","View Jobs","Funnel","Interview Prep"])

# ------------------------
# ADD JOBS
# ------------------------

with tab1:
    st.subheader("Add a Job")

    title = st.text_input("Job Title")
    company = st.text_input("Company")
    url = st.text_input("Job URL")
    source = detect_source(url)
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

# ------------------------
# VIEW JOBS
# ------------------------
with tab2:
    show_view_jobs()

# ------------------------
# Funnel
# ------------------------

with tab3:
    show_funnel(
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected
    )
        
# ------------------------
# Interview Preparation
# ------------------------


with tab4:
    show_interview_prep()
