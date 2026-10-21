"""Charts page - delayed flights per date, airport, airline and hour (same filters as the dashboard)."""

import streamlit as st

from components.charts import delayed_by_airline, delayed_by_airport, delayed_by_date, delayed_by_hour
from components.filters import sidebar_filters
from utils.helpers import get_flights


def charts():
    st.title("Charts")
    st.caption("The filters in the sidebar are shared with the dashboard page.")

    df = sidebar_filters(get_flights())
    if df.empty:
        st.info("No flights match the selected filters.", icon=":material/info:")
        return

    delayed_by_date(df)

    col1, col2 = st.columns(2)
    with col1:
        delayed_by_airport(df)
    with col2:
        delayed_by_airline(df)

    delayed_by_hour(df)


if __name__ == "__main__":
    charts()
