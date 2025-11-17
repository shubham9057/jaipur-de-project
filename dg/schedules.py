from dagster_dbt import build_schedule_from_dbt_selection
from dagster import Definitions, ScheduleDefinition, define_asset_job
from .assets import dbt_build
from .assets import test_job,downstream_job

schedules = [
#     build_schedule_from_dbt_selection(
#         [dbt_build],
#         job_name="materialize_dbt_models",
#         cron_schedule="0 0 * * *",
#         dbt_select="fqn:*",
#     ),
]

daily_dbt_schedule = ScheduleDefinition(
    job=test_job,
    cron_schedule="0 1 * * *",  # This cron expression means "run at 1:00 AM every day"
    execution_timezone="Asia/Kolkata" # Set to your local timezone
)