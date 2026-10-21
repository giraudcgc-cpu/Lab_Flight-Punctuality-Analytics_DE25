
                                           
#   Altair charts used by the dashboard     
                                           

import altair as alt
import pandas as pd
import streamlit as st

# fixed colors per direction (colorblind-safe pair, same color on every chart)
DIRECTION_COLORS = alt.Scale(
    domain=["Arrival", "Departure"],
    range=["#2a78d6", "#eb6834"],
)
SINGLE_COLOR = "#2a78d6"


def punctuality_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Total, delayed and % delayed flights grouped by one column."""
    grouped = (
        df.groupby(column, dropna=False)
        .agg(
            total_flights=("flight_key", "count"),
            completed_flights=("is_completed", "sum"),
            delayed_flights=("is_delayed", "sum"),
            cancelled_flights=("is_cancelled", "sum"),
        )
        .reset_index()
    )
    # punctuality is only known for flights that have landed / departed
    completed = grouped["completed_flights"]
    grouped["pct_delayed"] = (100 * grouped["delayed_flights"] / completed.where(completed > 0)).round(1)
    return grouped


def delayed_by_date_chart(df: pd.DataFrame) -> alt.Chart:
    """Grouped bars: delayed arrivals vs delayed departures per date."""
    data = (
        df.groupby(["flight_date", "direction"])
        .agg(delayed_flights=("is_delayed", "sum"), total_flights=("flight_key", "count"))
        .reset_index()
    )
    data["flight_date"] = data["flight_date"].astype(str)
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusEnd=4)
        .encode(
            x=alt.X("flight_date:N", title="Date"),
            xOffset=alt.XOffset("direction:N"),
            y=alt.Y("delayed_flights:Q", title="Delayed flights"),
            color=alt.Color("direction:N", scale=DIRECTION_COLORS, title="Direction",
                            legend=alt.Legend(orient="top")),
            tooltip=[
                alt.Tooltip("flight_date:N", title="Date"),
                alt.Tooltip("direction:N", title="Direction"),
                alt.Tooltip("delayed_flights:Q", title="Delayed"),
                alt.Tooltip("total_flights:Q", title="Total flights"),
            ],
        )
    )


def ranked_bar_chart(df: pd.DataFrame, column: str, title: str, top_n: int = 15) -> alt.Chart:
    """Horizontal bars sorted by number of delayed flights."""
    data = punctuality_by(df, column).nlargest(top_n, "delayed_flights")
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusEnd=4, color=SINGLE_COLOR)
        .encode(
            x=alt.X("delayed_flights:Q", title="Delayed flights"),
            y=alt.Y(f"{column}:N", sort="-x", title=title),
            tooltip=[
                alt.Tooltip(f"{column}:N", title=title),
                alt.Tooltip("delayed_flights:Q", title="Delayed"),
                alt.Tooltip("total_flights:Q", title="Total flights"),
                alt.Tooltip("pct_delayed:Q", title="% delayed"),
            ],
        )
    )


def delayed_by_hour_chart(df: pd.DataFrame) -> alt.Chart:
    """Share of delayed flights per scheduled hour of the day."""
    data = punctuality_by(df, "scheduled_hour_local")
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusEnd=4, color=SINGLE_COLOR)
        .encode(
            x=alt.X("scheduled_hour_local:O", title="Scheduled hour (local time)"),
            y=alt.Y("pct_delayed:Q", title="% delayed"),
            tooltip=[
                alt.Tooltip("scheduled_hour_local:O", title="Hour"),
                alt.Tooltip("pct_delayed:Q", title="% delayed"),
                alt.Tooltip("delayed_flights:Q", title="Delayed"),
                alt.Tooltip("total_flights:Q", title="Total flights"),
            ],
        )
    )



#  chart cards used by the charts page                               

def delayed_by_date(df: pd.DataFrame):
    with st.container(border=True):
        st.subheader("Delayed flights per date")
        st.altair_chart(delayed_by_date_chart(df), alt="Delayed arrivals and departures per date")


def delayed_by_airport(df: pd.DataFrame):
    with st.container(border=True):
        st.subheader("Delayed flights by airport")
        st.altair_chart(ranked_bar_chart(df, "swedavia_airport", "Airport", top_n=10),
                        alt="Delayed flights per Swedavia airport")


def delayed_by_airline(df: pd.DataFrame):
    with st.container(border=True):
        st.subheader("Top 15 airlines by delayed flights")
        st.altair_chart(ranked_bar_chart(df, "airline", "Airline"), alt="Airlines with most delayed flights")


def delayed_by_hour(df: pd.DataFrame):
    with st.container(border=True):
        st.subheader("Share of delayed flights by hour of the day")
        st.altair_chart(delayed_by_hour_chart(df), alt="Percentage delayed per scheduled hour")
