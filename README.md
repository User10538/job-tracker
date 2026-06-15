# Personal Job Tracker

## Project Overview

Personal Job Tracker is a local web application built with Python, Streamlit, and SQLite to help manage job applications during a job search.

The application runs locally on Windows and stores all data in a SQLite database (`jobs.db`).

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Database

* SQLite

## Development Environment

* Visual Studio Code
* GitHub (optional)

---

# To run it in VS Code, use streamlit run app.py

# Features Implemented

## 1. Job Management

Users can create and store job applications with:

* Job Title
* Company Name
* Job URL
* Source
* Application Date
* Status
* Notes

### Supported Sources

The application automatically detects:

* LinkedIn
* Seek
* Indeed
* Other

Example:

```text
https://www.linkedin.com/jobs/view/12345
```

Automatically becomes:

```text
Source: LinkedIn
```

---

## 2. Application Status Tracking

Each application can be assigned a status:

* New
* Applied
* Interview
* Rejected
* Offer

Status can be updated from the dashboard without re-creating the job entry.

---

## 3. Dashboard Metrics

The application displays:

* Total Jobs
* Applied Jobs
* Interviews
* Offers
* Rejected Jobs

Additional metric:

* Interview Rate %

Formula:

```text
Interview Rate =
(Interviews / Applied) × 100
```

---

## 4. Search and Filtering

Users can:

### Search

Search by:

* Company Name
* Job Title

### Filter

Filter jobs by:

* All
* New
* Applied
* Interview
* Rejected
* Offer

---

## 5. Job URL Tracking

Each job can store the original application URL.

The dashboard provides:

```text
Open Job Posting
```

which opens the original LinkedIn, Seek, or Indeed listing.

---

## 6. Data Export

Users can export application data as:

```text
jobs.csv
```

for reporting or backup purposes.

---

## 7. Job Deletion

Applications can be removed directly from the dashboard.

A delete button was added:

```text
🗑️ Delete Job
```

---

## 8. Application Funnel

The dashboard includes a visual funnel showing:

* Applied
* Interview
* Offer

Displayed as a bar chart.

---

## 9. Status Indicators

Statuses are color-coded using emojis:

| Status    | Indicator |
| --------- | --------- |
| New       | 🟡        |
| Applied   | 🔵        |
| Interview | 🟣        |
| Rejected  | 🔴        |
| Offer     | 🟢        |

---

# Database Schema

Current Jobs Table

```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    source TEXT,
    url TEXT,
    application_date TEXT,
    status TEXT,
    notes TEXT
);
```

---

# Database Upgrade Plan

Planned fields:

```sql
interview_date TEXT
followup_date TEXT
```

Migration strategy:

```python
ALTER TABLE jobs
ADD COLUMN interview_date TEXT

ALTER TABLE jobs
ADD COLUMN followup_date TEXT
```

without deleting existing data.

---

# Problems Solved During Development

## SQLite Schema Mismatch

Issue:

```text
sqlite3.OperationalError:
table jobs has no column named application_date
```

Cause:

Database schema did not match updated code.

Solution:

* Recreated database OR
* Added columns using ALTER TABLE.

---

## current_job NameError

Issue:

```text
NameError:
name 'current_job' is not defined
```

Cause:

Variable used before assignment.

Solution:

```python
current_job = df[
    df["id"] == selected_job
].iloc[0]
```

must be defined before:

```python
current_job["url"]
```

---

# Future Roadmap

## Version 4

Interview Management

Features:

* Interview Date
* Follow-up Date
* Upcoming Interviews Sidebar

---

## Version 5

Resume Tracking

Features:

* Resume Upload
* Resume Version Tracking
* Resume Attached to Application

Example:

```text
Microsoft
Resume_ITSupport_v2.pdf
```

---

## Version 6

Job URL Import

Goal:

```text
Paste Job URL
↓
Auto-fill company and title
↓
Save Job
```

---

## Version 7

Notifications

Features:

* Interview reminders
* Follow-up reminders
* Daily application summaries

---

# Current Status

Version: 3.0

Status: Working

Implemented:

* Add Job
* View Jobs
* Search
* Filter
* Update Status
* Delete Job
* Export CSV
* Dashboard Metrics
* URL Tracking
* Application Funnel

Platform:

* Windows
* Streamlit
* SQLite

Deployment:

* Localhost (http://localhost:8501)

```
```
