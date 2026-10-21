USE ROLE SECURITYADMIN;

--- warehouse ---
GRANT USAGE ON WAREHOUSE flight_wh TO ROLE flight_dbt_role;

--- database ---
GRANT USAGE ON DATABASE flight_punctuality TO ROLE flight_dbt_role;

--- Schema staging: read only (tables that exist now and tables dlt creates later) ---
GRANT USAGE ON SCHEMA flight_punctuality.staging TO ROLE flight_dbt_role;
GRANT SELECT ON ALL TABLES IN SCHEMA flight_punctuality.staging TO ROLE flight_dbt_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA flight_punctuality.staging TO ROLE flight_dbt_role;

---  warehouse + marts: create tables and views ---
---  dbt owns what it creates, so it can also read, replace and drop them ---
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA flight_punctuality.warehouse TO ROLE flight_dbt_role;
GRANT USAGE, CREATE TABLE, CREATE VIEW ON SCHEMA flight_punctuality.marts     TO ROLE flight_dbt_role;

GRANT ROLE flight_dbt_role TO USER flight_dbt_user;

--- developers (and through them SYSADMIN) can do everything dbt can do ---
GRANT ROLE flight_dbt_role TO ROLE flight_developer_role;

--- check ---
SHOW GRANTS TO ROLE flight_dbt_role;
SHOW FUTURE GRANTS IN SCHEMA flight_punctuality.staging;
