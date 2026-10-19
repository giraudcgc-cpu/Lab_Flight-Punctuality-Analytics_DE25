"""Home page - logo, intro text and the key numbers."""

import streamlit as st

from components.kpis import show_kpis
from utils.constants import LOGO_PATH, MARKDOWN_PATH
from utils.helpers import get_flights, logo_exists, read_textfile


def home():
    with st.container(horizontal=True, vertical_alignment="center"):
        if logo_exists():
            st.image(LOGO_PATH, width=120, alt="Logo")
        with st.container():
            st.title("Flight punctuality at Swedavia airports")
            st.caption("Are Swedish flights on time? Arrivals and departures for the last three days.")

    st.markdown(read_textfile(MARKDOWN_PATH / "intro.md"))

    st.subheader("Key numbers, all flights")
    try:
        show_kpis(get_flights())
    except Exception:  # keep the page alive if Snowflake is unreachable
        st.warning("Could not load the flights from Snowflake. Check the reporter settings in .env.")

    if st.button("Open the dashboard", icon=":material/arrow_forward:", type="primary"):
        st.switch_page("app_pages/dashboard.py")


if __name__ == "__main__":
    home()
