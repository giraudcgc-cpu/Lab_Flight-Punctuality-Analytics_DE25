"""Reusable helper functions (reading files and loading the flights)."""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.connect_data_warehouse import load_flights
from utils.constants import LOGO_PATH


def read_textfile(path: Path) -> str:
    """Open a text/markdown file and return its full contents as a string."""
    with open(path, encoding="utf-8") as file:
        return file.read()


def logo_exists() -> bool:
    """True when a (non-empty) logo.png has been added to assets/image/."""
    return LOGO_PATH.exists() and LOGO_PATH.stat().st_size > 0


@st.cache_data(ttl="1h", show_spinner="Loading flights from Snowflake...")
def get_flights() -> pd.DataFrame:
    """All flights from marts.mart_flights, cached for one hour."""
    return load_flights()
