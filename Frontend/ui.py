import streamlit as st
from add_update_ui import update_tab
from analytics import analytics_tab
from analytics_month import analytics_month_tab


st.title("Expense Tracking System")

tab1, tab2,tab3 = st.tabs(["Add/Update", "Analytics","Monthly Analytics"])

with tab1:
    update_tab()

with tab2:
    analytics_tab()

with tab3:
    analytics_month_tab()