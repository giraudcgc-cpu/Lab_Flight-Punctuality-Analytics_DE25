import pandas as pd
import streamlit as st


def show_kpis(df: pd.DataFrame):
    """Metric cards: flights, delayed, % delayed, on-time %, average delay and cancelled flights."""
    total = len(df)
    completed = int(df["is_completed"].sum())
    delayed = int(df["is_delayed"].sum())
    on_time = int(df["is_on_time"].sum())
    cancelled = int(df["is_cancelled"].sum())
    # punctuality is only known for flights that have landed / departed
    pct_delayed = 100 * delayed / max(completed, 1)
    pct_on_time = 100 * on_time / max(completed, 1)
    avg_delay = df.loc[df["is_delayed"], "delay_minutes"].mean()

    with st.container(horizontal=True):
        st.metric("Flights", f"{total:,}", border=True,
                  help=f"{completed:,} have landed / departed, the rest are cancelled or still scheduled")
        st.metric("Delayed flights", f"{delayed:,}", border=True)
        st.metric("Share delayed", f"{pct_delayed:.1f} %", border=True,
                  help="Delayed flights / flights that have landed or departed")
        st.metric("On time", f"{pct_on_time:.1f} %", border=True,
                  help="Landed / departed at most 15 minutes after the scheduled time")
        st.metric("Average delay when delayed", f"{avg_delay:.0f} min" if delayed else "-", border=True)
        st.metric("Cancelled flights", f"{cancelled:,}", border=True)
