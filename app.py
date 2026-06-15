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
    status = st.selectbox(
        "Status",
        ["New", "Applied", "Interview", "Rejected", "Offer"]
    )
    notes = st.text_area("Notes")

    if st.button("Save Job"):
        cursor.execute(
            """
            INSERT INTO jobs
            (title, company, source, status, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, company, source, status, notes)
        )
        conn.commit()
        st.success("Job saved!")

with tab2:
    st.subheader("Tracked Jobs")

    df = pd.read_sql_query(
        "SELECT * FROM jobs ORDER BY id DESC",
        conn
    )

    st.dataframe(df, use_container_width=True)

    if not df.empty:
        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "jobs.csv",
            "text/csv"
        )
