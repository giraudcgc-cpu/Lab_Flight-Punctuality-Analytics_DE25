import re
from io import StringIO

import pandas as pd
import requests

from data_extract_load.config import (
    WIKI_AIRLINES_URL,
    WIKI_AIRPORTS_URL,
    WIKI_USER_AGENT,
)


def _read_tables(url: str) -> list[pd.DataFrame]:
    response = requests.get(url, headers={"User-Agent": WIKI_USER_AGENT}, timeout=30)
    response.raise_for_status()
    return pd.read_html(StringIO(response.text))

#logical cleaning for the messy wikipedia data to establish a usable table 
def _snake_case(column) -> str:
    # flatten multi-level headers and drop footnotes like "[1]"
    if isinstance(column, tuple):
        column = column[-1]
    column = re.sub(r"\[.*?\]", "", str(column))
    column = re.sub(r"[^0-9a-zA-Z]+", "_", column).strip("_").lower()
    return column


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [_snake_case(c) for c in df.columns]
    # remove footnote markers inside cells and turn "—"/"-" into missing values
    df = df.astype("string").apply(lambda s: s.str.replace(r"\[.*?\]", "", regex=True).str.strip())
    return df.replace({"—": pd.NA, "–": pd.NA, "-": pd.NA, "": pd.NA, "nan": pd.NA})


def get_swedish_airports() -> pd.DataFrame:
    """Table from 'List of airports in Sweden' (city, icao, iata, name, usage, ...)."""
    tables = _read_tables(WIKI_AIRPORTS_URL)
    # pick the table that has both IATA and ICAO columns
    table = next(
        t for t in tables
        if {"iata", "icao"} <= {_snake_case(c) for c in t.columns}
    )
    df = _clean(table)
    # the passengers column is renamed every year, e.g. passengers_2023 -> passengers
    df = df.rename(columns=lambda c: "passengers" if c.startswith("passengers") else c)
    return df.dropna(subset=["icao"]).reset_index(drop=True)


def get_airline_codes() -> pd.DataFrame:
    """Table from 'List of airline codes' (iata, icao, airline, call sign, country, comments)."""
    tables = _read_tables(WIKI_AIRLINES_URL)
    table = max(
        (t for t in tables if {"iata", "icao"} <= {_snake_case(c) for c in t.columns}),
        key=len,
    )
    df = _clean(table)
    return df.dropna(subset=["airline"]).reset_index(drop=True)
