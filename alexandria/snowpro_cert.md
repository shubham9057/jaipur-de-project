## EXAM FORMAT FOR SNOW PRO CORE CERTIFICATION

Exam Version: COF-C02<br>
Total Number of Questions: 100<br>
Question Types: Multiple Select, Multiple Choice<br>
Time Limit: 115 minutes<br>
Languages: English, Japanese, Korean<br>
Passing Score: 750 + Scaled Scoring from 0 - 1000<br>
Unscored Content: Exams may include unscored items to gather statistical information for future use. These items are not identified on the form and do not impact your score, and additional time is factored into account for this content.

## PREREQUISITE KNOWLEDGE
While there are no strict prerequisites, the following knowledge and skills are highly recommended:

- Understanding of Snowflake Concepts: Familiarity with Snowflake’s architecture, including virtual warehouses, storage, and compute separation.
- SQL Proficiency: A solid grasp of SQL for querying and manipulating data within Snowflake.
- Cloud Platform Experience: Basic knowledge of cloud environments such as AWS, Azure, or Google Cloud is beneficial.
- Data Warehousing Fundamentals: Concepts like ETL processes, data modeling, and performance optimization are helpful.

## SUBJECT DOMAIN BREAKDOWNS
The following table contains the domains and weightings covered on the exam. It is not a
comprehensive listing of all the content that will be presented on the exam.

<pre>
Domain                                                Domain Weightings
1.0 Snowflake AI Data Cloud Features and Architecture  24%
2.0 Account Access and Security                        18%
3.0 Performance and Cost Optimization Concepts         16%
4.0 Data Loading and Unloading                         12%
5.0 Data Transformations                               18%
6.0 Data Protection and Data Sharing                   12%
</pre>


Domain 1.0: Snowflake AI Data Cloud Features and Architecture

- Outline key features of the Snowflake Data Cloud.
    - Interoperable storage
    - Elastic compute
    - Snowflake layers
    - Overview of Snowflake editions

-  Outline key Snowflake tools and user interfaces.
    - Snowsight
    - SnowSQL
    - Snowflake connectors
    - Snowflake drivers
    - Snowpark
    - SnowCD
    - Streamlit in Snowflake
    - Cortex (AI/ML services)
    - Snowflake SQL API


- Outline Snowflake’s catalog and objects.
    - Databases
    - Stages
    - Schema types
    - Table types
    - View types
    - Data types
    - User-Defined Functions (UDFs)
    - User Defined Table Functions (UDTFs)
    - Stored procedures
    - Streams
    - Tasks
    - Pipes
    - Shares
    - Sequences

- Outline Snowflake storage concepts.
    - Micro-partitions
    - Data clustering
    - Data storage monitoring

Domain 2.0: Account Access and Security

- Outline security principles.
    - Network security and policies
    - Multi-Factor Authentication (MFA)
    - Federated authentication
    - Key pair authentication
    - Single Sign-On (SSO)

- Define the entities and roles that are used in Snowflake.
    - Overview of access control
         - Access control frameworks
         - Access control privileges
    - Outline how privileges can be granted and revoked
    - Explain role hierarchy and privilege inheritance

- Outline data governance capabilities in Snowflake.
    - Accounts
    - Organizations
    - Secure views
    - Secure functions
    - Information schemas
    - Access history
         - Tracking read/write operations
    - Overview of row/column-level security
    - Object tags

Domain 3.0: Performance and Cost Optimization Concepts

- Explain the use of the Query Profile.
    - Explain plans
    - Data spilling
    - Use of the data cache
    - Micro-partition pruning
    - Query history

- Explain virtual warehouse configurations.
    - Types of warehouses
    - Multi-clustering warehouses
         - Scaling policies
         - Scaling modes
    - Warehouse sizing
    - Warehouse settings and access

- Outline virtual warehouse performance tools.
    - Monitoring warehouse loads
    - Scaling up compared to scaling out
    - Query acceleration service

- Optimize query performance.
    - Describe the use of materialized views
    - Use of specific SELECT commands
    - Clustering
    - Search optimization service
    - Persisted query results
    - Understanding the impact of different types of caching
         - Metadata cache
         - Result cache
         - Warehouse cache

- Describe cost optimization concepts and best practices in Snowflake.
    - Understanding and exploring the costs of different Snowflake features and services
         - Cost insights feature in Snowsight
         - Use of different table types and sizes
         - Use of views
         - Use of search optimization paths
         - Storage costs
         - Compute costs
- Understand and explore cloud services costs in Snowflake

- Costs considerations when using serverless features

- Cost considerations when moving data among regions
   - Replication
   - Fail-over

- Monitor and control costs
    - Resource monitors
    - Snowflake Budgets service

- Attribute costs
    - Cost center tagging
    - Use of the ACCOUNT_USAGE schema


Domain 4.0: Data Loading and Unloading

- Define concepts and best practices that should be considered when loading data.
    - Stages and stage types
    - File size and formats
    - Folder structures
    - Ad hoc/bulk loading
    - Snowpipe

- Outline different commands used to load data and when they should be used.
    - CREATE STAGE
    - CREATE FILE FORMAT
    - CREATE PIPE
    - CREATE EXTERNAL TABLE
    - COPY INTO
    - INSERT/INSERT OVERWRITE
    - PUT
    - VALIDATE

-  Define concepts and best practices that should be considered when unloading data.
    - File size and formats
          - Overview of compression methods
    - Empty strings and NULL values
    - Unloading to a single file
    - Unloading relational tables

- Outline the different commands used to unload data and when they should be used.
    - GET
    - LIST
    - COPY INTO
    - CREATE STAGE
    - CREATE FILE FORMAT

Domain 5.0: Data Transformations

- Explain how to work with standard data.
    - Estimation functions
    - Sampling
    - SAMPLE command
    - /TABLESAMPLE command
    - Sampling methods
         - Fraction-based
         - Fixed-size

- Supported function types
    - System functions
    - Table functions
    - External functions
    - User-Defined Functions (UDFs)

- Stored procedures

- Streams

- Tasks

- Explain how to work with semi-structured data.
    - Supported data formats, data types, and sizes
    - VARIANT column
    - Flattening the nested structure
        - FLATTEN command
        - LATERAL FLATTEN command
    - Semi-structured data functions
        - ARRAY/OBJECT creation and manipulation
        - Extracting values
        - Type predicates

- Explain how to work with unstructured data.
    - Define and use directory tables
    - SQL file functions
    - Types of URLs available to access files
    - Processind unstructured data
        - User-Defined Functions (UDFs) for unstructured data analyisis
        - Stored procedure

Domain 6.0: Data Protection and Data Sharing

- Outline Continuous Data Protection with Snowflake.
    - Time Travel
    - Fail-safe
    - Data encryption
    - Cloning
    - Replication and failover

-  Outline Snowflake data sharing capabilities.
   - Account types
   - Snowflake Marketplace
   - Data Exchange
   - Access control options
       - DDL commands to create and manage shares
       - Privileges required for working with shares

-  Secure Data Sharing
       - Direct shares
       - Data Listings


## Resources 

- [Snowflake Documentation](https://docs.snowflake.com/en/user-guide-getting-started)
- Youtube Playlist
     - https://youtu.be/AR88dZG-hwo?si=O4J5HwAoMl4i6zXC
     - https://www.youtube.com/playlist?list=PLc2EZr8W2QIBqETApuLNGGB8X_WL47AKb
- [SnowPro Core Certification Exam Study Guide](https://training.snowflake.com/lmt/clmsCatalogDetails.prMain?site=sf&in_offeringId=98873983&in_language_identifier=en-us&in_region=us&in_from_module=CLMSSHARE.PRMAIN)
- [Start your 30-Day free trail](https://signup.snowflake.com/)
- Enroll to the level up courses available on the learning portal. You can login with community credentials
     - https://learn.snowflake.com/en/courses/uni-lvlup-101/
     - https://learn.snowflake.com/en/courses/uni-lvlup-102/
     - https://learn.snowflake.com/en/courses/uni-lvlup-103/
     - https://learn.snowflake.com/en/courses/uni-lvlup-104/
     - https://learn.snowflake.com/en/courses/uni-lvlup-105/
     - https://learn.snowflake.com/en/courses/uni-lvlup-106/
     - https://learn.snowflake.com/en/courses/uni-lvlup-107/
     - https://learn.snowflake.com/en/courses/uni-lvlup-108/
     - https://learn.snowflake.com/en/courses/uni-lvlup-109/
     - https://docs.google.com/document/d/1FdDaoL9Lle4JI6AVcw2Ooc5oHCRkAe_MaJf-OyMBGyc/edit
- [Atrium LMS Portal Course](https://atrium.tovuti.io/courses/course/snowflake-snowpro-core)
- [Udemy Course Link](https://www.udemy.com/course/ultimate-snowpro-core-certification-course-exam/)
- [Snowflake practice exams](https://www.udemy.com/course/snowflake-snowpro-core-certification-questions-exam/?couponCode=ST7MT290425G3 )
- [Sample questions](https://docs.google.com/spreadsheets/d/1g6WS0KPMZyxDPj6Pb-LeXYJTzG7rIkjRJUOT15AjVuY/edit?gid=0#gid=0 )


## Requesting an Exam Voucher

Fill out this **[Free Voucher Request Form](https://docs.google.com/forms/d/e/1FAIpQLSeqD9VduYBlwRwz9zmnVodhufZp686iiQTtBy9G-hO1vF4ioQ/viewform)**. After completing the form, Snowflake will provide the voucher code and registration instructions in 2-3 business days via Email. Only request a voucher when you are prepared to take the exam, as the voucher must be used within a 90-day window.

If vouchers are no longer available through the form listed above, contact the DE Manager (Naresh Keerthi) to request a voucher.
