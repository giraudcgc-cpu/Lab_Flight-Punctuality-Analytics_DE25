USE ROLE SECURITYADMIN;

GRANT USAGE ON WAREHOUSE flight_wh TO ROLE flight_dlt_role;

GRANT USAGE ON DATABASE flight_punctuality TO ROLE flight_dlt_role;

--- dlt creates a helper schema called "staging_staging" to replace loads ---
GRANT CREATE SCHEMA ON DATABASE flight_punctuality TO ROLE flight_dlt_role;

--- staging ---
GRANT USAGE, CREATE TABLE ON SCHEMA flight_punctuality.staging TO ROLE flight_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA flight_punctuality.staging TO ROLE flight_dlt_role;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA flight_punctuality.staging TO ROLE flight_dlt_role;

GRANT ROLE flight_dlt_role TO USER flight_dlt_user;

--- developers (including SYSADMIN) can do everything dlt can do ---
GRANT ROLE flight_dlt_role TO ROLE flight_developer_role;

--- checking ---
SHOW GRANTS TO ROLE flight_dlt_role;
SHOW GRANTS TO USER flight_dlt_user;