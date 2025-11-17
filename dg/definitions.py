from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbt_build,downstream_job,trigger_sensor,new_file_sensor
from .project import de_project
from .schedules import daily_dbt_schedule

defs = Definitions(
    assets=[dbt_build],
    schedules=[daily_dbt_schedule],
    jobs =[downstream_job],
    sensors=[trigger_sensor,new_file_sensor],
    resources={
        "dbt": DbtCliResource(project_dir=de_project),
    },

)
