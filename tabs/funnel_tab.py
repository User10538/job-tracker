# ------------------------
# FUNNEL tab3
# ------------------------
import streamlit as st
import pandas as pd

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
            offers
            ]
            },
            index=[
                "Applied",
                "Interview",
                "Offer"
            ]
        )
    st.bar_chart(
        funnel_data
        )
