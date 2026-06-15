import streamlit as st
import re

def extract_keywords(text):

    common_keywords = [
        "Azure",
        "AWS",
        "GCP",
        "Intune",
        "PowerShell",
        "Active Directory",
        "Office 365",
        "Microsoft 365",
        "Exchange",
        "VMware",
        "Citrix",
        "Linux",
        "Windows Server",
        "Docker",
        "Kubernetes",
        "Python",
        "SQL",
        "Networking",
        "Cisco",
        "Security",
        "ITIL",
        "ServiceNow"
    ]

    found = []

    text = text.lower()

    for keyword in common_keywords:

        if keyword.lower() in text:
            found.append(keyword)

    return ", ".join(found)



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
