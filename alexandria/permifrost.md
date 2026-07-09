# Permifrost
An open-source project for managing Snowflake permissions and roles through YAML configuration.
- [Docs](https://gitlab.com/gitlab-data/permifrost)  
- [Implementation Blog](https://medium.com/yousign-engineering-product/snowflake-rbac-implementation-with-permifrost-3d30652825ad)
- [Opinionated guide used by Meltano](https://github.com/meltano/squared/blob/main/data/utilities/permifrost/README.md)

## Overview
Permifrost is a declaritive framework for Snowflake Role Based Access Control (RBAC). It performs the role of SECURITYADMIN by managing user and role priveleges in a Snowflake account.

Permifrost is provided as a python package which enforces compliance of a Snowflake account with a specification file written in YAML. This spec declares the state of priveleges in the account, such as:  
- the roles that each user is granted  
- the databases, schemas, and priveleges on those objects that each role is granted

### How does it work?
When run, Permifrost will compare the state of the account with the spec and perform GRANT, REVOKE, and ALTER statements as the SECURITYADMIN to make the account meet the spec. There are some operations it will not perform and instead produces warnings and errors to be addressed separately.

### What can be declared?
Objects:
- databases
- roles (and role hierarchy)
    - read/write privileges on:
        - databases
        - schemas
        - tables (and views)
- users (service and human)
    - role membership
- warehouses
- integrations  

Check out the [example spec file](https://gitlab.com/gitlab-data/permifrost/blob/master/tests/permifrost/specs/snowflake_spec.yml). Partially shown here:  


Permifrost uses an abstracted privelege model with only "read" and "write" options that map to Snowflake priveleges:  
| Objects | Permifrost permissions | Snowflake grants |
| --- | --- | --- |
| Databases | read | usage |
|  | write | monitor, create schema |
| Schemas | read | usage |
|  | write | monitor, create table, create view, create stage, create file format, create sequence, create function, create pipe |
| Table | read | select |
|  | write | insert, update, delete, truncate, references |

### What _should_ be declared?
Your Snowflake account security model will depend on your needs. Follow the best practices provided by Snowflake and change only if you need to. Here are some resources:  
- [RBAC article](../../concepts/data-engineering/rbac.md)
- [Snowflake Access Control Considerations](https://docs.snowflake.com/en/user-guide/security-access-control-considerations)
- [Understanding RBAC (3-part series by prior Snowflake Solutions Architect)](https://articles.analytics.today/understanding-snowflake-role-based-access-control-a-complete-guide-to-rbac)

### Prerequisites
- All objects declared in the spec must already exist in the account.  

- [Required environment variables](https://gitlab.com/gitlab-data/permifrost#connection-parameters) must be set.


## Tidbits
- Permifrost will not create or drop objects.   
    -  Objects existing in Snowflake, but not declared in the spec, are unknown and unaffected by Permifrost. This can result in differences between the account and the spec.

    - Automating these steps can be done with any snowflake-supported scripting language. An advanced setup could even read from the same YAML configuration. In some case, a more extensive [infrastructure-as-code](../../concepts/devops-and-infrastructure/infrastructure-as-code.md) tool will be required instead of Permifrost.   
