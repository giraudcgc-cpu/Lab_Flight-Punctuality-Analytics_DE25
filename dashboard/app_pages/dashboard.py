"""Dashboard page - filters, KPIs and tables."""

import streamlit as st

from components.filters import sidebar_filters
from components.kpis import show_kpis
from components.tables import most_delayed_flights, punctuality_per_airline
from utils.helpers import get_flights


def dashboard():
    st.title("Dashboard")
    st.caption("A flight is **delayed** when it is more than 15 minutes later than scheduled.")

    df = sidebar_filters(get_flights())
    if df.empty:
        st.info("No flights match the selected filters.", icon=":material/info:")
        return

    show_kpis(df)
    punctuality_per_airline(df)
    most_delayed_flights(df)


if __name__ == "__main__":
    dashboard()
