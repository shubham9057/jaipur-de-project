from dagster import AssetExecutionContext,AssetSelection,sensor,AssetKey, asset_sensor,op, RunRequest, SkipReason
from dagster import Definitions, ScheduleDefinition, define_asset_job ,RunConfig,DefaultSensorStatus
from dagster_dbt import DbtCliResource, dbt_assets
from .project import de_project
import os



@dbt_assets(manifest=de_project.manifest_path)
def dbt_build(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


test_job = define_asset_job(
    name="test_job",
    selection=["raw_pos_menu", "raw_pos_location"]
)
downstream_job = define_asset_job(
    name="downstream_job",
    selection=["orders"]
)
test_job_file = define_asset_job(
    name="test_job_file",
    selection=["raw_pos_location"]
)




@asset_sensor(asset_key=AssetKey("raw_pos_menu"), job_name="downstream_job")
def trigger_sensor():
    return RunRequest()





def check_for_new_files() -> list[str]:
    """Checks the given directory for any files and returns their paths."""
    # Ensure the directories exist
    BASE_DIR = os.getcwd()
    INPUT_DIRECTORY = os.path.join(BASE_DIR, "data_inbox")
    PROCESSED_DIRECTORY=os.path.join(BASE_DIR, "processed_files")
    os.makedirs(INPUT_DIRECTORY, exist_ok=True)
    os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
    
    # Get all the files in the input directory, ignoring subdirectories
    new_files = [
        f for f in os.listdir(INPUT_DIRECTORY) 
        if os.path.isfile(os.path.join(INPUT_DIRECTORY, f))
    ]
    return new_files


@sensor(
    job=test_job_file,
    minimum_interval_seconds=5,
    default_status=DefaultSensorStatus.RUNNING,  # Sensor is turned on by default
)
def new_file_sensor():
    new_files = check_for_new_files()
    # New files, run `my_job`
    if new_files:
        for filename in new_files:
            yield RunRequest(run_key=filename)
    # No new files, skip the run and log the reason
    else:
        yield SkipReason("No new files found")