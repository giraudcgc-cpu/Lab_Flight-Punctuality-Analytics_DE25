USE ROLE SECURITYADMIN;

-- compute
GRANT USAGE ON WAREHOUSE flight_wh TO ROLE flight_reporter_role;

GRANT USAGE ON DATABASE flight_punctuality TO ROLE flight_reporter_role;
GRANT USAGE ON SCHEMA flight_punctuality.marts TO ROLE flight_reporter_role;

-- read all tables and views in marts (now and the ones dbt creates later)
GRANT SELECT ON ALL TABLES IN SCHEMA flight_punctuality.marts TO ROLE flight_reporter_role;
GRANT SELECT ON FUTURE TABLES IN SCHEMA flight_punctuality.marts TO ROLE flight_reporter_role;
GRANT SELECT ON ALL VIEWS IN SCHEMA flight_punctuality.marts TO ROLE flight_reporter_role;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA flight_punctuality.marts TO ROLE flight_reporter_role;

-- give the role to the reporter user
GRANT ROLE flight_reporter_role TO USER flight_reporter_user;

-- developers (and through them SYSADMIN) can test what the dashboard sees
GRANT ROLE flight_reporter_role TO ROLE flight_developer_role;

-- check
SHOW GRANTS TO ROLE flight_reporter_role;
SHOW FUTURE GRANTS IN SCHEMA flight_punctuality.marts;
