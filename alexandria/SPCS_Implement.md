# Snowpark Container Services (SPCS) Implementation Guide: Airflow Deployment

## Overview

Snowpark Container Services (SPCS) is a full-container service that helps users easily execute, scale up/down, and deploy Docker containers in a secure manner within the Snowflake environment. SPCS removes the need to take any data out of the Snowflake environment security boundaries to perform orchestration, transformations, or applications.

The purpose of this document is to provide a detailed, step-by-step implementation plan for building a native Apache Airflow environment on Snowflake.

## Table of Contents

- [Overview](#overview)
- [Core Architecture & Structural Foundations](#core-architecture--structural-foundations)
- [1. Prerequisites & Enterprise Governance](#1-prerequisites--enterprise-governance)
- [2. Snowflake Infrastructure Provisioning](#2-snowflake-infrastructure-provisioning)
- [3. Building Custom Images & Dependency Management](#3-building-custom-images--dependency-management)
    - [3.1 Write the Local Dockerfile](#31-write-the-local-dockerfile)
    - [3.2 Authenticate, Tag, and Push via CLI](#32-authenticate-tag-and-push-via-cli)
- [4. Service Specification & Volume Mapping (`airflow_spec.yaml`)](#4-service-specification--volume-mapping-airflow_specyaml)
- [5. Storage Initialization (Pre-Deployment)](#5-storage-initialization-pre-deployment)
- [6. Automated DAG Deployment (GitHub CI/CD Integration)](#6-automated-dag-deployment-github-cicd-integration)
    - [6.1 Establish Secure GitHub Authentication](#61-establish-secure-github-authentication)
    - [6.2 Create the Snowflake Git Repository Object](#62-create-the-snowflake-git-repository-object)
    - [6.3 Build the Automation Engine (Snowflake Task)](#63-build-the-automation-engine-snowflake-task)
    - [6.4 Initializing Pipeline & Start the Service](#64-initializing-pipeline--start-the-service)
- [7. Troubleshooting & Connecting to the Outside World](#7-troubleshooting--connecting-to-the-outside-world)
- [8. Resources & Training Reference Blocks](#8-resources--training-reference-blocks)



## Core Architecture & Structural Foundations

While deploying Airflow in Snowflake, there are two major aspects that you have to consider:

1. **"Separate Houses" Problem (Storage Isolation)**<br>
In general, engineers divide Airflow in two separate containers: one for the Web UI container and another one for the Scheduler. Nonetheless, in the cloud, each of the containers is allocated to have its private, isolated hard disk drive. In case you employ a simple local database (such as SQLite), both of these containers will not be able to access it. Therefore, while working, the Webserver will generate the database on its private hard drive, while the Scheduler will examine an empty hard drive belonging to it and crash immediately, being unable to find the database.

2. **"All-in-One" Approach**<br>
In order to solve this problem, we put everything in **one single container.** Using the particular command – `airflow standalone`, Airflow manages to place the Web UI, Scheduler, and the database in the same container to use the same hard disk drive.

3. **The Airflow 3.0 Update**<br>
If you are using a newer version of Airflow (version 3.0 or higher), the creators actually deleted the old setup commands we used to use (like `airflow webserver` and `airflow users create`). They did this because the new `airflow standalone` command is so much better—it automatically sets up the database, creates an admin user, and turns everything on with just one single word.

## 1. Prerequisites & Enterprise Governance

Before executing infrastructure setup statements, ensure the following enterprise state is met:

- **Privileged Access Management:** Following the principle of least privilege, you should execute these steps using a dedicated infrastructure role (e.g., `SPCS_ADMIN` or an elevated `SYSADMIN`). This custom role must be explicitly granted the global `CREATE COMPUTE POOL`, `CREATE INTEGRATION`, and `BIND SERVICE ENDPOINT` privileges, as well as the schema-level `CREATE SECRET` privilege by an account administrator prior to deployment.

- **Local Tooling:** Docker Desktop (or its equivalent container runtime environment tool) must be operational on your local machine.

- **SnowSQL CLI:** The command-line utility must be installed, configured, and authenticated to your target account.

> 💡 **Important Concept: Local Docker vs. SPCS Cloud Compute**
> One of the most frequent questions asked by new developers going through these requirements is: *"Do I need to keep Docker Desktop running constantly on my laptop 24/7 for Airflow to run my DAGs?"*
> 
> **And the Answer is: No!** You only need to have Docker Desktop up and running on your laptop for the few minutes you will spend building and pushing your own image onto Snowflake (Step 3). After the successful deployment of the image and the initiation of the SPCS service, Snowflake will start doing everything from its cloud-based servers (Compute Pool). You can safely shutdown Docker Desktop, turn off your laptop and go on vacation—Airflow will run your DAGs 24/7 from the cloud.

## 2. Snowflake Infrastructure Provisioning

Run the following SQL script to establish the required hardware compute capacity and the secure internal image registry.

```sql
-- 2.1 Establish Object Hierarchy Context
CREATE DATABASE IF NOT EXISTS <DATABASE_NAME>;
CREATE SCHEMA IF NOT EXISTS <DATABASE_NAME>.<SCHEMA_NAME>;
USE SCHEMA <DATABASE_NAME>.<SCHEMA_NAME>;

-- 2.2 Create the Compute Pool
-- This allocates the underlying virtual machines that execute the Docker daemon.
CREATE COMPUTE POOL IF NOT EXISTS <COMPUTE_POOL_NAME>
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_S
  AUTO_RESUME = TRUE;

-- Verify pool allocation and hardware provisioning status
DESCRIBE COMPUTE POOL <COMPUTE_POOL_NAME>;

-- 2.3 Initialize the Image Repository
-- This creates Snowflake's secure internal version of an OCI-compliant container registry (Docker Hub).
CREATE IMAGE REPOSITORY <IMAGE_REPOSITORY_NAME>;

-- 2.4 Fetch the Internal Registry Endpoint
-- Execute this command and record the 'repository_url' column value.
-- Format will resemble: <orgname>-<accountname>.registry.snowflakecomputing.com/<dbname>/<schemaname>/<repo_name>
SHOW IMAGE REPOSITORIES;
```

## 3. Building Custom Images & Dependency Management

When you're working inside a secure corporate network, you can't just `pip install` packages like `faker` or `boto3` on the fly while a container is spinning up. Because outbound public internet is blocked, that runtime installation will just fail. 

To handle this properly, we need to follow the principle of immutable infrastructure—meaning every single library and system dependency has to be baked directly into our custom image locally before we push it to Snowflake.

### 3.1 Write the Local Dockerfile

In your local repository root directory, construct a plain-text configuration file explicitly named `Dockerfile` (with no trailing extension):

```Dockerfile
# Use the official Apache Airflow distribution as our baseline
# Note: Replace this with an internally approved golden image if policy requires it
FROM apache/airflow:3.1.6

# Switch to root if system-level binary dependencies are required, otherwise remain as airflow user
USER airflow

# Permanently inject custom runtime libraries directly into the image layer
RUN pip install --no-cache-dir pandas boto3 <your_custom_libraries>
```

### 3.2 Authenticate, Tag, and Push via CLI
Execute these commands in your machine's terminal window from the location of your `Dockerfile`:

```Bash
# Step 1: Authenticate local Docker daemon to the remote Snowflake Private Registry
docker login <YOUR_SNOWFLAKE_REGISTRY_URL> -u <YOUR_SNOWFLAKE_USERNAME>

# Step 2: Compile and bake the custom image layer locally
# Note: Do not omit the trailing period '.' which denotes the current directory build context
docker build -t <YOUR_SNOWFLAKE_REGISTRY_URL>/<IMAGE_NAME>:<TAG> .

# Step 3: Push the image up to Snowflake's Image Storage Engine
docker push <YOUR_SNOWFLAKE_REGISTRY_URL>/<IMAGE_NAME>:<TAG>
```

### What Do These Three Commands Actually Do?
Imagine Docker Images as building your own custom cake and delivering it to a secured warehouse (Snowflake).

1. **`docker login` (Unlocking the Warehouse):**
Snowflake is a highly secure environment. It will not accept random files from the internet. This command sends your Snowflake username and password to the Snowflake Image Registry, proving you have the authority to upload images to your specific ecommerce_spcs database.

2. **`docker build` (Baking the Cake):**
This command tells your local computer to read your Dockerfile line by line. It downloads the base Apache Airflow software, installs your custom Python packages (like pandas or boto3), and freezes them all together into a single, immutable snapshot on your laptop's hard drive.

- The -t stands for tag. It acts as the name tag stuck to the front of your image so Docker knows what to call it.

3. **`docker push` (Shipping the Delivery):**
Once the image is built and sitting on your laptop, this command actually uploads that massive file over the internet and drops it directly into Snowflake's internal Image Repository. Once it is there, Snowflake SPCS can finally spin it up.


## 4. Service Specification & Volume Mapping (`airflow_spec.yaml`)

For the purpose of maintaining our DAGs and configuration scripts, we will mount the Snowflake Stage directly onto the container instance. This will make the file management process much more convenient as you simply need to upload your files on the stage, and they will immediately appear inside the container instance without needing to restart the whole service.

Create an application specification file named `airflow_spec.yaml`:

```YAML
spec:
  containers:
    - name: airflow-all-in-one
      image: <YOUR_SNOWFLAKE_REGISTRY_URL>/<IMAGE_NAME>:<TAG>
      env:
        AIRFLOW__CORE__EXECUTOR: SequentialExecutor
        AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: sqlite:////opt/airflow/airflow.db
      command:
        - "airflow"
        - "standalone"
      volumeMounts:
        - name: dags-volume
          mountPath: /opt/airflow/dags
  endpoints:
    - name: airflow-ui
      port: 8080
      public: true
  volumes:
    - name: dags-volume
      source: "@<DATABASE_NAME>.<SCHEMA_NAME>.<DAGS_STAGE_NAME>"
```

## 5. Storage Initialization (Pre-Deployment)

With our fully automated GitHub CI/CD pipeline handling all file transfers, we no longer need to use the SnowSQL CLI to manually upload files from a local laptop.

In this step, we simply initialize the empty Snowflake storage stages that will act as the landing zones for our automated GitHub sync.

```SQL
-- 5.1 Initialize Storage Volumes
-- Create the internal stage allocated to holding the configuration YAML file
CREATE STAGE IF NOT EXISTS <DATABASE_NAME>.<SCHEMA_NAME>.<SPECS_STAGE_NAME>;

-- Create the dedicated stage allocated to holding runtime Python DAG execution files
CREATE STAGE IF NOT EXISTS <DATABASE_NAME>.<SCHEMA_NAME>.<DAGS_STAGE_NAME>
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```


## 6. Automated DAG Deployment (GitHub CI/CD Integration)

In traditional setups, engineers must manually run SnowSQL PUT commands from their terminal every time they change a line of Python code. This is slow, error-prone, and makes team collaboration difficult.

To achieve true enterprise automation, we utilize **Snowflake Git Integration**. This creates a fully automated CI/CD (Continuous Integration / Continuous Deployment) pipeline.

**The automated workflow:** `Developer writes code ➔ git push ➔ GitHub ➔ Snowflake automatically detects the change and updates Airflow.`

### 6.1 Establish Secure GitHub Authentication

Snowflake needs a secure key (Personal Access Token) to read your GitHub repository.

**Why are we doing this?** We cannot use standard passwords. We must store a secure token in Snowflake's internal Secret Manager, and then create an API Integration (a secure network tunnel) that is only allowed to talk to your specific GitHub username.

```SQL
USE ROLE <YOUR_INFRASTRUCTURE_ROLE>;
USE DATABASE <DATABASE_NAME>;
USE SCHEMA <SCHEMA_NAME>;

-- 1. Store the GitHub Token securely in Snowflake
-- NEVER commit your actual password/token to your code repository!
CREATE OR REPLACE SECRET github_pat_secret
  TYPE = PASSWORD
  USERNAME = '<YOUR_GITHUB_USERNAME>'
  PASSWORD = '<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>';

-- 2. Create the network pathway to your specific GitHub account
CREATE OR REPLACE API INTEGRATION github_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/<YOUR_GITHUB_USERNAME>')
  ALLOWED_AUTHENTICATION_SECRETS = (github_pat_secret)
  ENABLED = TRUE;
```

### 6.2 Create the Snowflake Git Repository Object

This command creates a virtual mirror of your remote GitHub repository directly inside your Snowflake database. It links the URL of your code to the secure tunnel we just built.

```SQL
-- Link your target repo to the secure connection
CREATE OR REPLACE GIT REPOSITORY <GIT_REPOSITORY_NAME>
  API_INTEGRATION = github_api_integration
  GIT_CREDENTIALS = github_pat_secret
  ORIGIN = 'https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git';
```

### 6.3 Build the Automation Engine (Snowflake Task)

**Why are we doing this?** Snowflake will not automatically guess when you push new code to GitHub. We must create a scheduled background "Task" that wakes up every 5 minutes (you can set according to you), checks GitHub for changes (`FETCH`), and copies only the specific Python DAGs into the Airflow storage stage (`COPY FILES`).

CRITICAL NOTE: The `FROM` path in the COPY FILES command must exactly match the nested folder structure of your GitHub repository where your `.py` files live.

```SQL
-- 1. Create a serverless task that runs every 5 minutes
CREATE OR REPLACE TASK <SYNC_TASK_NAME>
  SCHEDULE = '5 MINUTE'
  AS
  EXECUTE IMMEDIATE $$
    BEGIN
      -- Step A: Pull the latest commits from your GitHub Repo mirror
      ALTER GIT REPOSITORY <GIT_REPOSITORY_NAME> FETCH;
      
      -- NOTE: Change 'main' to 'master' if your default branch is named differently!
      -- Step B: Copy the Python files from the EXACT nested GitHub folder into the Airflow Stage
      COPY FILES 
        INTO @<DATABASE_NAME>.<SCHEMA_NAME>.<DAGS_STAGE_NAME> 
        FROM @<GIT_REPOSITORY_NAME>/branches/main/<PATH_TO_YOUR_DAGS_FOLDER>/;

      -- Step C: Route the configuration YAML file into the Specs Stage
      COPY FILES 
        INTO @<DATABASE_NAME>.<SCHEMA_NAME>.<SPECS_STAGE_NAME> 
        FROM @<GIT_REPOSITORY_NAME>/branches/main/<PATH_TO_YOUR_YAML_FILE>/airflow_spec.yaml;
    END;
  $$;

-- 2. Turn the automation on!
ALTER TASK <SYNC_TASK_NAME> RESUME;
```

### 6.4 Initializing Pipeline & Start the Service

To launch the Airflow container, Snowflake must first read your `airflow_spec.yaml` configuration file. Because we moved our infrastructure setup to GitHub for automation, this file does not exist in Snowflake yet.

Before we can start the service, we must manually trigger our sync task one time. This instantly pulls both the YAML configuration and your Python DAGs from GitHub into their respective Snowflake Stages. Once the files land in the stages, we can safely boot the container.

```SQL
-- 1. Manually sync the GitHub mirror
ALTER GIT REPOSITORY <GIT_REPOSITORY_NAME> FETCH;

-- 2. Force the copy task to run immediately
EXECUTE TASK <SYNC_TASK_NAME>;

-- (Wait 5 to 10 seconds here to ensure the backend file transfer is complete)

-- 3. Start the Airflow Service
DROP SERVICE IF EXISTS airflow_service;

CREATE SERVICE airflow_service
  IN COMPUTE POOL <COMPUTE_POOL_NAME>
  FROM @<DATABASE_NAME>.<SCHEMA_NAME>.<SPECS_STAGE_NAME>
  SPECIFICATION_FILE = 'airflow_spec.yaml';

-- 4. Fetch the secure public URL (ingress_url) to access your Airflow Web UI
SHOW ENDPOINTS IN SERVICE airflow_service;
```

## 7. Troubleshooting & Connecting to the Outside World

### 7.1 Real-Time Container Diagnostics Check

If you experience service termination or web connection dropping errors, execute these debugging requests directly in your SQL console:

```SQL
-- Check the current status (e.g., PENDING, PROVISIONING, RUNNING, FAILED)
CALL SYSTEM$GET_SERVICE_STATUS('airflow_service');

-- Extract the internal logs to see exactly what the container is doing (or why it crashed)
SELECT SYSTEM$GET_SERVICE_LOGS('airflow_service', '0', 'airflow-all-in-one');
```

### 7.2 Extracting the Auto-Generated Admin Credentials

Because we used the `airflow standalone` command in our YAML file, Airflow automatically set up the database and generated a secure, randomized password for the Admin user.

To find the password:

1. Run the `SYSTEM$GET_SERVICE_LOGS` query shown above.

2. Click on the log output and scroll to the very bottom.

3. Locate the text box that looks exactly like this:

```Plaintext
=================================================================
Airflow is ready
Login with username: admin
Password:  <your_auto_generated_password_here>
=================================================================
```

### 7.3 Enterprise Egress Firewall Matrices: Paid Accounts vs. Free Trial Limits

By default, Snowflake acts like a highly secure vault—it **completely blocks containers from accessing the public internet**. If your Airflow DAGs need to push data to an Amazon S3 bucket, call an external API, or download a file, the firewall will block it and your task will fail with a `NameResolutionError`.

```Plaintext
NameResolutionError: AWSHTTPSConnection(host='<bucket>.s3.amazonaws.com'): 
Failed to resolve local network path or service name not known
```
**For Standard/Commercial Snowflake Accounts:**
You can open a safe pathway through the firewall by creating a Network Rule and binding it to your service:

```SQL
-- 1. Whitelist the specific website or service (Example: Amazon S3)
CREATE OR REPLACE NETWORK RULE s3_outbound_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('<your_bucket_id>.s3.amazonaws.com', 's3.amazonaws.com');

-- 2. Bundle that rule into an Access Integration
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION s3_external_access
  ALLOWED_NETWORK_RULES = (s3_outbound_rule)
  ENABLED = true;

-- 3. Restart your service and attach the integration
CREATE SERVICE airflow_service
  IN COMPUTE POOL <COMPUTE_POOL_NAME>
  FROM @<SPECS_STAGE_NAME>
  SPECIFICATION_FILE = 'airflow_spec.yaml'
  EXTERNAL_ACCESS_INTEGRATIONS = (s3_external_access);
```

### ⚠️ Important Note for Free Trial Accounts

In case you are working on a proof-of-concept in a 30-Day Snowflake Free Trial environment, the above SQL commands will result in the following error message:
`SQL compilation error: External access is not supported for trial accounts.`

In order to prevent malicious individuals from using cloud compute resources for free to mine cryptocurrency, Snowflake completely blocks internet access for any free trial users. In case you are a trial user, you need to either:

1. Change your Python code to push data to a **Snowflake Internal Stage** instead of an external service like S3.

2. Run Airflow locally on your laptop using Docker Desktop, which can freely connect to both Snowflake and the internet.

## 8. Resources & Training Reference Blocks

### Snowflake Container Services (SPCS) Core

- [Snowpark Container Services Overview](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview) - Core SPCS Concepts

- [SPCS Specification Reference (YAML)](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/specification-reference) - YAML Spec Cheatsheet

- [Working with Image Registries](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-registry-repository) - Image Registry Guide

- [Monitoring and Logging for SPCS](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/monitoring-services) - Debugging & Logging

### Apache Airflow

- [Airflow CLI & 'Standalone' Documentation](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html) - Standalone CLI Magic

- [Airflow Best Practices for Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) - Docker Best Practices
