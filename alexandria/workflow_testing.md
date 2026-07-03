# Snowflake Workflow Testing

## Test Connection to Snowflake
This workflow tests the connection and data query execution against Snowflake data warehouse.

### Test Queries
- SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER;
- Verify ETL pipeline execution in Snowflake
- Validate data transformation results

### Expected Outcomes
- Connection successful to Snowflake account
- Query execution completes without errors
- Data integrity checks pass
