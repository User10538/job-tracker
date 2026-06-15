import streamlit as st


def detect_source(url):

    url = (url or "").lower()

    if "linkedin" in url:
        return "LinkedIn"

    if "seek" in url:
        return "Seek"

    if "indeed" in url:
        return "Indeed"

    return "Other"


def open_job_link(url):

    if url:
        st.markdown(
            f"### 🔗 [Open Job Posting]({url})"
        )


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
