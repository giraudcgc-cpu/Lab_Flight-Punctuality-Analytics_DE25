from collections.abc import Mapping
from pathlib import Path
from typing import Any

import dagster as dg
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets

from data_extract_load.config import REPO_ROOT
from data_extract_load.sources import make_pipeline, swedavia_source, wikipedia_source


# =============================================================================
# SHARED HELPERS
# =============================================================================

def staging_key(table: str) -> dg.AssetKey:
    """Common asset key for staging tables, used by both dlt and dbt so that
    dlt's output lines up with dbt's sources in the asset graph."""
    return dg.AssetKey(["staging", table])


# =============================================================================
# EXTRACT & LOAD (dlt)
# =============================================================================

class StagingDltTranslator(DagsterDltTranslator):
    """Key dlt assets ["staging", <resource>] so they match dbt's source keys."""

    def get_asset_spec(self, data):
        default = super().get_asset_spec(data)
        return default.replace_attributes(
            key=staging_key(data.resource.name),
            group_name="extract_load",
        )


dlt_resource = DagsterDltResource()


@dlt_assets(
    dlt_source=swedavia_source(),
    dlt_pipeline=make_pipeline("swedavia_flights"),
    name="swedavia",
    dagster_dlt_translator=StagingDltTranslator(),
)
def dlt_swedavia_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


@dlt_assets(
    dlt_source=wikipedia_source(),
    dlt_pipeline=make_pipeline("wikipedia_reference"),
    name="wikipedia",
    dagster_dlt_translator=StagingDltTranslator(),
)
def dlt_wikipedia_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


# =============================================================================
# TRANSFORMATION (dbt)
# =============================================================================

# --- Project & resource setup ------------------------------------------------

DBT_DIR = REPO_ROOT / "dbt_transformation" / "dbt_code"

dbt_project = DbtProject(
    project_dir=DBT_DIR,
    profiles_dir=Path.home() / ".dbt",  # profiles.yml lives outside the repo
)
dbt_resource = DbtCliResource(project_dir=dbt_project)

# Regenerates the dbt manifest automatically in dev
dbt_project.prepare_if_dev()


# --- Translator --------------------------------------------------------------

class TransformationDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> dg.AssetKey:
        # dbt sources -> same keys the dlt assets produce
        if dbt_resource_props["resource_type"] == "source":
            return staging_key(dbt_resource_props["name"])
        return super().get_asset_key(dbt_resource_props)

    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> str:
        return "transformation"


# --- Assets ------------------------------------------------------------------

@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=TransformationDbtTranslator(),
)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    # build = run + test, in dependency order
    yield from dbt.cli(["build"], context=context).stream()


# =============================================================================
# ORCHESTRATION (jobs, schedules, sensors)
# =============================================================================

# --- Jobs --------------------------------------------------------------------

job_dlt = dg.define_asset_job(
    "job_dlt",
    selection=dg.AssetSelection.assets(dlt_swedavia_load, dlt_wikipedia_load),
)
job_dbt = dg.define_asset_job(
    "job_dbt",
    selection=dg.AssetSelection.assets(dbt_models),
)

# --- Schedule: run the dlt load daily at 06:00 (stopped by default) ----------

schedule_dlt = dg.ScheduleDefinition(
    job=job_dlt,
    cron_schedule="0 6 * * *",
    execution_timezone="Europe/Stockholm",
)

# --- Sensor: when a dlt run succeeds, kick off the dbt job -------------------

@dg.run_status_sensor(
    run_status=dg.DagsterRunStatus.SUCCESS,
    monitored_jobs=[job_dlt],
    request_job=job_dbt,
)
def dlt_load_sensor(context: dg.RunStatusSensorContext):
    return dg.RunRequest(run_key=context.dagster_run.run_id)


# =============================================================================
# DEFINITIONS
# =============================================================================

defs = dg.Definitions(
    assets=[dlt_swedavia_load, dlt_wikipedia_load, dbt_models],
    resources={"dlt": dlt_resource, "dbt": dbt_resource},
    jobs=[job_dlt, job_dbt],
    schedules=[schedule_dlt],
    sensors=[dlt_load_sensor],
)