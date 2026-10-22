import base64
import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

# .env lives in the repo root (two levels above this folder: dashboard/utils/)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _connect():
    key_b64 = os.getenv("REPORTER_SNOWFLAKE_PRIVATE_KEY_B64")

    if key_b64:
        key_path = Path("/tmp/flight_reporter_user.p8")
        key_path.write_bytes(base64.b64decode(key_b64.strip()))
        os.chmod(key_path, 0o600)
        private_key_path = str(key_path)
    else:
        private_key_path = os.getenv(
            "REPORTER_SNOWFLAKE_PRIVATE_KEY_PATH"
        )
    params = dict(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("REPORTER_SNOWFLAKE_USER", "flight_reporter_user"),
        role=os.getenv("REPORTER_SNOWFLAKE_ROLE", "flight_reporter_role"),
        private_key_file=private_key_path,
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "flight_wh"),
        database=os.getenv("SNOWFLAKE_DATABASE", "flight_punctuality"),
        schema="marts",
    )
    passphrase = os.getenv("REPORTER_SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
    if passphrase:
        params["private_key_file_pwd"] = passphrase
    return snowflake.connector.connect(**params)


def query(sql: str) -> pd.DataFrame:
    with _connect() as conn:
        df = conn.cursor().execute(sql).fetch_pandas_all()
    # snowflake returns UPPERCASE column names -> lowercase for pandas
    df.columns = [c.lower() for c in df.columns]
    return df


def load_flights() -> pd.DataFrame:
    df = query("select * from mart_flight")
    df["flight_date"] = pd.to_datetime(df["flight_date"]).dt.date
    return df
