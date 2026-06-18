import streamlit as st
import pandas as pd
# ------------------------
# FUNNEL tab3
# ------------------------

def show(applied, interviews, offers, rejected):
    st.divider()

    st.subheader(
            "Application Funnel"
        )
    
    funnel_data = pd.DataFrame(
        {
            "Count": [
            applied,
            interviews,
            offers,
            rejected
            ]
            },
            index=[
                "Applied",
                "Interview",
                "Offer",
                "Rejected"
            ]
        )
    st.bar_chart(
        funnel_data
        )
