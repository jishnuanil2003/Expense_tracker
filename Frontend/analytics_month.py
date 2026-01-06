import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_month_tab():
    st.title("Monthly Expense Analytics")

    response = requests.get(f"{API_URL}/analytics/month")

    if response.status_code != 200:
        st.error(f"API Error {response.status_code}")
        st.write(response.text)
        return

    data = response.json()

    if not data:
        st.warning("No data available")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Sort by month number to keep Jan → Dec order
    df = df.sort_values(by="total")

    # Bar chart
    st.bar_chart(
        df.set_index("month_name")["total"],
        use_container_width=True
    )

    # Format table
    df_display = df[["month_name", "total"]].rename(
        columns={
            "month_name": "Month",
            "total": "Total Expense"
        }
    )

    df_display["Total Expense"] = df_display["Total Expense"].map("{:.2f}".format)

    st.table(df_display)