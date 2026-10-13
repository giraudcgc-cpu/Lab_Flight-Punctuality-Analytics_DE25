--- Copy of team_users.local.sql (not in git) ---

USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS dennis
    TYPE = PERSON
    PASSWORD = '<enter_PASSWORD>'
    EMAIL = '<DENNIS_EMAIL>'
    DEFAULT_ROLE = flight_developer_role
    DEFAULT_WAREHOUSE = flight_wh;

CREATE USER IF NOT EXISTS karl
    TYPE = PERSON
    PASSWORD = '<enter_PASSWORD>'
    EMAIL = '<KARL_EMAIL>'
    DEFAULT_ROLE = flight_developer_role
    DEFAULT_WAREHOUSE = flight_wh;

ALTER USER "giraudcgc" SET DEFAULT_ROLE = flight_developer_role DEFAULT_WAREHOUSE = flight_wh;

USE ROLE SECURITYADMIN;
GRANT ROLE flight_developer_role TO USER giraudcgc;
GRANT ROLE flight_developer_role TO USER dennis;
GRANT ROLE flight_developer_role TO USER karl;

USE ROLE ACCOUNTADMIN;
GRANT ROLE ACCOUNTADMIN TO USER dennis;

