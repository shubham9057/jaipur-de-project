# dbt Best Practices

## 1. Project Structure
- Organize models in logical folders (`staging`, `marts`, `intermediate`)
- Keep raw models separate from transformed models
- Use consistent naming conventions for models

## 2. Naming Conventions
- Prefix staging models with `stg_`
- Prefix mart models with appropriate domain names
- Use snake_case for all model names and columns
- Name source tables with prefix `src_`

## 3. Testing and Documentation
- Write tests for all key models and columns
- Add descriptions to models and columns
- Use generic tests (unique, not_null, accepted_values, relationships)
- Document assumptions and transformations

## 4. Model Materialization
- Use `table` materialization for frequently queried models
- Use `view` for simple transformations to save warehouse space
- Use `incremental` for large fact tables with append-only patterns
- Use `ephemeral` for intermediate calculations

## 5. Performance Optimization
- Avoid SELECT * in models; explicitly list needed columns
- Use dbt's `ref()` and `source()` functions for lineage tracking
- Implement proper indexing strategy in your warehouse
- Monitor query performance and optimize expensive transformations

## 6. Version Control and Collaboration
- Commit frequently with meaningful messages
- Use feature branches for new features
- Document changes in commit messages
- Review code before merging to main branch

## 7. CI/CD Integration
- Implement automated dbt runs on pull requests
- Run all tests before production deployment
- Use environment-specific configurations (dev, staging, prod)
- Schedule regular full refreshes of models
