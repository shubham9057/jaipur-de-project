# OAuth in Snowflake

Snowflake supports two OAuth flows for authentication: **Snowflake OAuth** and **External OAuth**. Both allow token-based access without passing passwords, and both are great for applications to access Snowflake through a service user, but they differ in where the authorization server lives and who manages it.

| | Snowflake OAuth | External OAuth |
| --- | --- | --- |
| Authorization server | Managed by Snowflake | Your identity provider (Okta, Entra ID, PingFederate, etc.) |
| Setup complexity | Lower — configured entirely in Snowflake | Higher — requires coordinating Snowflake + IdP configuration |
| Token management | Snowflake issues and validates tokens | IdP issues tokens, Snowflake validates via security integration |
| SSO integration | Limited — separate from corporate SSO | Leverages existing corporate SSO/IdP |
| Audience | Partner tools (Tableau, Looker, etc.), quick custom integrations | Service accounts, programmatic access, enterprise SSO-driven workflows |
| Role mapping | Uses Snowflake default role | Can map IdP groups/scopes to Snowflake roles |
| Revocation | Managed in Snowflake | Managed at the IdP; Snowflake honors token expiry |

## When to use which

**Snowflake OAuth** is simpler and works well when:

- You're integrating a [supported partner application](https://docs.snowflake.com/en/user-guide/oauth-partner)
- You want fast setup without IdP coordination
- The connecting users already have Snowflake credentials

## Official documentation

- [Introduction to OAuth](https://docs.snowflake.com/en/user-guide/oauth-intro)
- [Snowflake OAuth for partner applications](https://docs.snowflake.com/en/user-guide/oauth-partner)
- [Snowflake OAuth for custom clients](https://docs.snowflake.com/en/user-guide/oauth-custom)
- [External OAuth overview](https://docs.snowflake.com/en/user-guide/oauth-ext-overview)
- [External OAuth — custom authorization servers](https://docs.snowflake.com/en/user-guide/oauth-ext-custom)
- [External OAuth — Okta](https://docs.snowflake.com/en/user-guide/oauth-okta)
- [External OAuth — Microsoft Entra ID](https://docs.snowflake.com/en/user-guide/oauth-azure)
- [CREATE SECURITY INTEGRATION (Snowflake OAuth)](https://docs.snowflake.com/en/sql-reference/sql/create-security-integration-oauth-snowflake)
