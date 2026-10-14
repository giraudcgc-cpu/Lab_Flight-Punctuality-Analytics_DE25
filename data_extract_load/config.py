import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]

# load .env from the repo root no matter where the script is started from
load_dotenv(REPO_ROOT / ".env")


#Swedavia FlightInfo API                                                    

# API key goes in the .env file
SWEDAVIA_API_KEY = os.getenv("SWEDAVIA_API_KEY")
SWEDAVIA_BASE_URL = "https://api.swedavia.se/flightinfo/v2"

# the ten airports operated by Swedavia (= all airports available in the API)
SWEDAVIA_AIRPORTS = [
    "ARN",  # Stockholm Arlanda
    "BMA",  # Stockholm Bromma
    "GOT",  # Göteborg Landvetter
    "MMX",  # Malmö
    "LLA",  # Luleå
    "UME",  # Umeå
    "OSD",  # Åre Östersund
    "VBY",  # Visby
    "RNB",  # Ronneby
    "KRN",  # Kiruna
]

#the past three days INCLUDING the current extraction date
DAYS_BACK = 3
LOCAL_TIMEZONE = "Europe/Stockholm"


#  Wikipedia                                                                  
WIKI_AIRPORTS_URL = "https://en.wikipedia.org/wiki/List_of_airports_in_Sweden"
WIKI_AIRLINES_URL = "https://en.wikipedia.org/wiki/List_of_airline_codes"

# wikipedia blocks requests without a descriptive user agent
WIKI_USER_AGENT = "flight-punctuality-student-project/1.0 (educational use)"


#  Snowflake connection for dlt (service user flight_dlt_user)                
def snowflake_dlt_credentials() -> dict:
    """Credentials dict passed to dlt's snowflake destination (password auth)."""
    return {
        "host": os.getenv("SNOWFLAKE_ACCOUNT"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "flight_punctuality"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "flight_wh"),
        "username": os.getenv("DLT_SNOWFLAKE_USER", "flight_dlt_user"),
        "role": os.getenv("DLT_SNOWFLAKE_ROLE", "flight_dlt_role"),
        "password": os.getenv("DLT_SNOWFLAKE_PASSWORD"),
    }
