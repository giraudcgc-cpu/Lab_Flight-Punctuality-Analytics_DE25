import os

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def query_flight(
    query="SELECT * FROM FLIGHT_PUNCTUALITY.MARTS.MART_PUNCTUALITY_DAILY",
):
    with snowflake.connector.connect(
        user=os.getenv("REPORTER_SNOWFLAKE_USER"),
        private_key_file=os.getenv("REPORTER_SNOWFLAKE_PRIVATE_KEY_PATH"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("REPORTER_SNOWFLAKE_ROLE"),
    ) as conn:
        return pd.read_sql(query, conn)