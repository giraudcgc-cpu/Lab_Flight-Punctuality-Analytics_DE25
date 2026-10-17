from pathlib import Path

import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets

from data_extract_load.load_pipeline import make_pipeline
from data_extract_load.sources import swedavia_source, wikipedia_source

ROOT = Path(__file__).parent.parent


# ---------- dlt ----------
class StagingTranslator(DagsterDltTranslator):
    """Name dlt assets ["staging", <table>] so they match dbt's source keys."""

    def get_asset_spec(self, data):
        default = super().get_asset_spec(data)
        return default.replace_attributes(
            key=dg.AssetKey(["staging", data.resource.name]),
            group_name="ingestion",
        )


@dlt_assets(
    dlt_source=swedavia_source(),
    dlt_pipeline=make_pipeline("swedavia"),
    name="swedavia",
    dagster_dlt_translator=StagingTranslator(),
)
def swedavia_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


@dlt_assets(
    dlt_source=wikipedia_source(),
    dlt_pipeline=make_pipeline("wikipedia"),
    name="wikipedia",
    dagster_dlt_translator=StagingTranslator(),
)
def wikipedia_assets(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


# ---------- dbt ----------
dbt_project = DbtProject(
    project_dir=ROOT / "dbt_transformation" / "dbt_code",
    profiles_dir=Path.home() / ".dbt",  # folder containing profiles.yml
)
dbt_project.prepare_if_dev()


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# ---------- job + schedule ----------
full_pipeline = dg.define_asset_job("full_pipeline", selection=dg.AssetSelection.all())

defs = dg.Definitions(
    assets=[swedavia_assets, wikipedia_assets, dbt_models],
    resources={
        "dlt": DagsterDltResource(),
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
    jobs=[full_pipeline],
    schedules=[dg.ScheduleDefinition(job=full_pipeline, cron_schedule="0 6 * * *")],
)