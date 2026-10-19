"""Entry point of the dashboard. Run from the repo root with:  streamlit run dashboard/app.py"""

import streamlit as st

from utils.constants import FILTER_KEYS, LOGO_PATH
from utils.helpers import logo_exists

st.set_page_config(
    page_title="Flight punctuality",
    page_icon=":material/flight:",
    layout="wide",
)

if logo_exists():
    st.logo(LOGO_PATH, size="large")

# keep the filter selections when the user switches between pages
for key in FILTER_KEYS:
    if key in st.session_state:
        st.session_state[key] = st.session_state[key]

pages = [
    st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True),
    st.Page("app_pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("app_pages/charts.py", title="Charts", icon=":material/bar_chart:"),
]



pg = st.navigation(pages, position="top")  # builds the navigation menu at the top
pg.run()                                   # runs the page the user selected
