import pandas as pd
import streamlit as st

from utils.helpers import get_flights


def _keep_valid(key: str, options: list, default: list):
    """Set the filter's start value, and drop old selections that are no longer in the data."""
    if key not in st.session_state:
        st.session_state[key] = default
    else:
        st.session_state[key] = [value for value in st.session_state[key] if value in options]


def sidebar_filters(flights: pd.DataFrame) -> pd.DataFrame:
    """Draw the filters in the sidebar and return the filtered flights."""
    directions = ["Arrival", "Departure"]
    airports = sorted(flights["swedavia_airport"].dropna().unique())
    airlines = sorted(flights["airline"].dropna().unique())
    dates = sorted(flights["flight_date"].unique())

    _keep_valid("filter_direction", directions, directions)
    _keep_valid("filter_airports", airports, [])
    _keep_valid("filter_airlines", airlines, [])
    _keep_valid("filter_dates", dates, dates)

    with st.sidebar:
        st.header("Filters")
        st.segmented_control("Direction", directions, selection_mode="multi", key="filter_direction")
        st.multiselect("Swedavia airport", airports, placeholder="All airports", key="filter_airports")
        st.multiselect("Airline", airlines, placeholder="All airlines", key="filter_airlines")
        st.pills("Date", dates, selection_mode="multi", key="filter_dates")
        if st.button("Refresh data", icon=":material/refresh:"):
            get_flights.clear()
            st.rerun()

    df = flights[
        flights["direction"].isin(st.session_state.filter_direction)
        & flights["flight_date"].isin(st.session_state.filter_dates)
    ]
    if st.session_state.filter_airports:
        df = df[df["swedavia_airport"].isin(st.session_state.filter_airports)]
    if st.session_state.filter_airlines:
        df = df[df["airline"].isin(st.session_state.filter_airlines)]
    return df
