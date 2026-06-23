import sqlite3
import streamlit as st
import pandas as pd

from tabs.funnel_tab import show as show_funnel
from tabs.interview_prep_tab import show as show_interview_prep
from tabs.view_jobs_tab import show as show_view_jobs
from tabs.add_job_tab import show as show_add_job

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
    notes TEXT, 
    resume_text TEXT
)
""")
conn.commit()

for col in [
    "interview_date","followup_date","job_description",
    "keywords","recruiter_notes","ai_prompt","resume_file", "resume_text"
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

tab1, tab2, tab3, tab4 = st.tabs(["Add Job","View Jobs","Interview Prep","Funnel"])

# ------------------------
# ADD JOBS
# ------------------------

with tab1:
    show_add_job()

# ------------------------
# VIEW JOBS
# ------------------------
with tab2:
    show_view_jobs()
      
# ------------------------
# Interview Preparation
# ------------------------

with tab3:
    show_interview_prep()

# ------------------------
# Funnel
# ------------------------

with tab4:
    show_funnel(
        applied=applied,
        interviews=interviews,
        offers=offers,
        rejected=rejected
    )
