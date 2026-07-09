# SnowConvert
Convert SQL code from legacy systems into Snowflake SQL.
- [Docs](https://docs.snowconvert.com/sc)  
- [Official Training (free)](https://learn.snowflake.com/en/courses/OD-SC-D/)   

## Overview
SnowConvert is a local program you run to assess and convert legacy SQL code into Snowflake SQL as part of a migration from those systems onto Snowflake. It helps with the database migration step of a migration project. It does not help with all the other steps, such as data migration, external integrations, or data validations.  

SnowConvert works for these legacy systems:  
- Teradata
- Oracle
- SQL Server
- Redshift
- Azure Synapse
- Sybase IQ  

_[See documentation for latest information.](https://docs.snowconvert.com/sc/general/about)_

## Install
Install from Snowflake directly:  
_Home page > Data > Migrations > Download (under "For SQL workloads, use SnowConvert to migrate your code") > Select your OS_

## Usage
### 1 - 🏗 Extract legacy code
- Identify the subset of the database you want to assess or convert. Extract the .sql files (and other supported files if applicable) from your source system related to this subset. 
    - Start with a small subset of related code to convert - not the whole project.

- For each source, follow the best practices for extraction, which typically involve a custom extraction script: https://docs.snowconvert.com/sc/general/getting-started/best-practices  

- Remove code you don’t want to convert, such as back-ups, system-specific code like statistics gathering, or DBA task-based code that will not be relevant in Snowflake.  

- Each object (DDL) should be in its own file (.sql)
    - This can be done manually before conversion. Or in the “Conversion Settings” enable the “Prepare Code” option, which will do this automatically.

### 2 - 🧐 Run Assessment
- Assessment with SnowConvert does not require an access code. Use this as a first step to assess how much code could be automatically converted.  

- Review assessment for code completion, valid files, etc.
### 3 - ⏩ Run Conversion
- Conversion requires an access code. Click the "Get an Access Code" button on the Project Creation page.
    - Submit your business details. You will receive the code via email. This is usually very quick. I _think_ that the [official training](https://learn.snowflake.com/en/courses/OD-SC-D/) must be completed before you can get an access code.  

- Conversion process takes some time.  

- Output will be in the same structure as the input. Additional files will be generated.
### 4 - 📊 Evaluate Reports and Code
- FDM - Functional Difference Message - these messages flag code that will require manual review because the source system functionality is different from snowflake. Review these to validate whether they need to be altered or not.  

- EWI - Errors Warnings and Issues - requires manual review and must be fixed. A CSV file for these issues contains detail.
    - Some common types of issues:
        - missing dependencies - needs inclusion or confirmation that it will not break
        - parsing error - needs fixing
        - dynamic sql - need to review string is expected and valid SQL  

- Reports such as the code units csv file contain detail of all code units converted
### 5 - 📝 Modify Input Code
- Fix the errors in the source code.  

- Some EWI messages are uncommented in the code to force a fix (won't compile). Be sure to remove these flags after fixing the issue.
### 6 - 🔄 Repeat
- Try again! Use the "Retry Conversion" button on the Conversion Results page.

## Deploy the Converted Code
SnowConvert's role in the migration process ends once you are happy with the converted code. It does not connect to any systems for deployment. You need to take the converted code and deploy it to Snowflake separately.

## Tidbits
- On MacOS ARM (M1 chip), the program expects a `~/.config` directory to exist. I had to create this manually before the program would open. I did not need to modify the default file permissions as the program told me to.  

- Open a previously closed project with the "Open project" option. Then select the `<name>.snowct` file created in the source directory.

<br></br>
| Change Log |
|-|
|2025-04-01 - Elias Athey - Created after taking official training|
||
