import time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from data_extract_load.config import (
    DAYS_BACK,
    LOCAL_TIMEZONE,
    SWEDAVIA_AIRPORTS,
    SWEDAVIA_API_KEY,
    SWEDAVIA_BASE_URL,
)

DIRECTIONS = ("arrivals", "departures")


def last_n_dates(days_back: int = DAYS_BACK) -> list[str]:
    """Today and the days before it in Swedish local time, e.g. 3 -> [today, -1, -2]."""
    today = datetime.now(ZoneInfo(LOCAL_TIMEZONE)).date()
    return [(today - timedelta(days=n)).isoformat() for n in range(days_back)]


def _headers() -> dict:
    if not SWEDAVIA_API_KEY:
        raise ValueError(
            "SWEDAVIA_API_KEY is missing. Add it to the .env file in the repo root."
        )
    # the API key is sent in this header on every request
    return {
        "Ocp-Apim-Subscription-Key": SWEDAVIA_API_KEY,
        "Accept": "application/json",
    }


def get_flights(direction: str, airport: str, flight_date: str | date) -> dict:
    """Raw json response for one airport, one direction and one date.

    e.g. GET https://api.swedavia.se/flightinfo/v2/ARN/arrivals/2026-10-07
    """
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {DIRECTIONS}")

    url = f"{SWEDAVIA_BASE_URL}/{airport}/{direction}/{flight_date}"

    for attempt in range(3):
        response = requests.get(url, headers=_headers(), timeout=30)
        # 429 = too many requests -> wait and retry
        if response.status_code == 429:
            time.sleep(5 * (attempt + 1))
            continue
        response.raise_for_status()
        return response.json()

    response.raise_for_status()
    return {}


def iter_flights(direction: str, airports=SWEDAVIA_AIRPORTS, dates=None):
    """Yield one flight (dict) at a time for all airports and dates."""
    dates = dates or last_n_dates()
    extracted_at = datetime.now(ZoneInfo("UTC")).isoformat()

    for airport in airports:
        for flight_date in dates:
            payload = get_flights(direction, airport, flight_date)
            flights = payload.get("flights", [])

            if payload.get("numberOfFlights", len(flights)) > len(flights):
                print(
                    f"WARNING: {airport} {direction} {flight_date} returned "
                    f"{len(flights)} of {payload['numberOfFlights']} flights"
                )

            for flight in flights:
                # metadata telling which request the row came from
                flight["query_airport"] = airport
                flight["query_date"] = flight_date
                flight["extracted_at"] = extracted_at
                yield flight
