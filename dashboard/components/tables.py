import pandas as pd
import streamlit as st

from components.charts import punctuality_by


def punctuality_per_airline(df: pd.DataFrame):
    """Table: flights, delayed, cancelled and % delayed per airline."""
    with st.container(border=True):
        st.subheader("Punctuality per airline")
        st.dataframe(
            punctuality_by(df, "airline").sort_values("delayed_flights", ascending=False),
            hide_index=True,
            alt="Punctuality per airline",
            column_config={
                "airline": "Airline",
                "total_flights": "Flights",
                "completed_flights": "Landed / departed",
                "delayed_flights": "Delayed",
                "cancelled_flights": "Cancelled",
                "pct_delayed": st.column_config.ProgressColumn("% delayed", format="%.1f %%", min_value=0, max_value=100),
            },
        )


def most_delayed_flights(df: pd.DataFrame, top_n: int = 100):
    """Table: the flights with the longest delay."""
    with st.container(border=True):
        st.subheader("Most delayed flights")
        st.dataframe(
            df[df["is_delayed"]]
            .sort_values("delay_minutes", ascending=False)
            [["flight_date", "direction", "flight_id", "airline", "swedavia_airport",
              "other_airport", "scheduled_time_local", "actual_time_local", "delay_minutes", "flight_status"]]
            .head(top_n),
            hide_index=True,
            alt="Most delayed flights",
            column_config={
                "flight_date": "Date",
                "direction": "Direction",
                "flight_id": "Flight",
                "airline": "Airline",
                "swedavia_airport": "Swedavia airport",
                "other_airport": "From / to",
                "scheduled_time_local": st.column_config.DatetimeColumn("Scheduled", format="YYYY-MM-DD HH:mm"),
                "actual_time_local": st.column_config.DatetimeColumn("Actual", format="YYYY-MM-DD HH:mm"),
                "delay_minutes": st.column_config.NumberColumn("Delay (min)"),
                "flight_status": "Status",
            },
        )
