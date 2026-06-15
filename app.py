
import sqlite3

conn = sqlite3.connect("jobs.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS jobs(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 source TEXT,
 title TEXT,
 company TEXT,
 url TEXT UNIQUE,
 status TEXT DEFAULT 'new'
)
""")

conn.commit()
print("Job Tracker initialized.")
