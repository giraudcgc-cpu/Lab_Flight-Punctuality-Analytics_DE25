import dlt
import requests

API_URL = ""


@dlt.resource(name="flights", write_disposition="replace")
def flights(api_key: str = dlt.secrets.value):
    resp = requests.get(
        API_URL,
        headers={
            "Accept": "application/json",
            "Ocp-Apim-Subscription-Key": api_key,
        },
        timeout=30,
    )
    resp.raise_for_status()
    yield resp.json()["flights"]


@dlt.source(name="my_api")
def my_api_source():
    return flights


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="my_api_pipeline",
        destination="snowflake",
        dataset_name="staging",
    )
    print(pipeline.run(my_api_source()))