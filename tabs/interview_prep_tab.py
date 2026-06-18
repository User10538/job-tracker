"""
Interview Preparation tab 3
"""

import sqlite3
import streamlit as st
import pandas as pd

def show():
    DB = "jobs.db"

    conn = sqlite3.connect(DB, check_same_thread=False)
    cursor = conn.cursor()

    df = pd.read_sql_query(
        "SELECT * FROM jobs ORDER BY id DESC",
        conn
    )

    st.divider()
    
    st.subheader(
        "Interview Preparation"
        )
    st.write("Prepare for upcoming interview")
