import dlt

from data_extract_load.config import snowflake_dlt_credentials
from data_extract_load.swedavia_api import iter_flights
from data_extract_load.wikipedia import get_airline_codes, get_swedish_airports

# truncate the staging_staging schema that dlt creates together with dagster
dlt.config["load.truncate_staging_dataset"] = True


def _flight_columns(time_field: str, other_airport_field: str) -> dict:
    """Column hints for the columns dbt uses.

    Guarantees the columns exist in snowflake with the right type, even if
    e.g. no flight has an actual time yet.
    """
    text_columns = [
        "flight_id",
        "airline_operator__iata",
        "airline_operator__icao",
        "airline_operator__name",
        "location_and_status__terminal",
        "location_and_status__flight_leg_status",
        "location_and_status__flight_leg_status_english",
        "location_and_status__flight_leg_status_swedish",
        "flight_leg_identifier__callsign",
        "flight_leg_identifier__aircraft_registration",
        "flight_leg_identifier__departure_airport_iata",
        "flight_leg_identifier__arrival_airport_iata",
        "flight_leg_identifier__departure_airport_icao",
        "flight_leg_identifier__arrival_airport_icao",
        other_airport_field,  # name of the airport at the other end of the flight
        "query_airport",
    ]
    timestamp_columns = [
        f"{time_field}__scheduled_utc",
        f"{time_field}__estimated_utc",
        f"{time_field}__actual_utc",
        "extracted_at",
    ]
    # a NEW dict per column - dlt writes the column name into each hint
    columns = {name: {"data_type": "text", "nullable": True} for name in text_columns}
    columns |= {name: {"data_type": "timestamp", "nullable": True} for name in timestamp_columns}
    columns["query_date"] = {"data_type": "date", "nullable": True}
    return columns


# write_disposition="replace": every run holds exactly the latest 3 days
@dlt.resource(
    name="arrivals",
    table_name="arrivals",
    write_disposition="replace",
    columns=_flight_columns("arrival_time", "departure_airport_english"),
)
def arrivals_resource():
    yield from iter_flights("arrivals")


@dlt.resource(
    name="departures",
    table_name="departures",
    write_disposition="replace",
    columns=_flight_columns("departure_time", "arrival_airport_english"),
)
def departures_resource():
    yield from iter_flights("departures")


@dlt.resource(name="wiki_airports", table_name="wiki_airports", write_disposition="replace")
def wiki_airports_resource():
    yield get_swedish_airports().astype(object).where(lambda df: df.notna(), None).to_dict("records")


@dlt.resource(name="wiki_airlines", table_name="wiki_airlines", write_disposition="replace")
def wiki_airlines_resource():
    yield get_airline_codes().astype(object).where(lambda df: df.notna(), None).to_dict("records")


# dagster only works with dlt source, not dlt resource
@dlt.source(name="swedavia_source")
def swedavia_source():
    return arrivals_resource(), departures_resource()


@dlt.source(name="wikipedia_source")
def wikipedia_source():
    return wiki_airports_resource(), wiki_airlines_resource()


def snowflake_destination():
    return dlt.destinations.snowflake(credentials=snowflake_dlt_credentials())


def make_pipeline(pipeline_name: str) -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name=pipeline_name,
        destination=snowflake_destination(),
        dataset_name="staging",
    )