USE ROLE SECURITYADMIN;

GRANT USAGE ON WAREHOUSE flight_wh TO ROLE flight_developer_role;
GRANT USAGE ON DATABASE flight_punctuality TO ROLE flight_developer_role;
GRANT USAGE ON ALL SCHEMAS IN DATABASE flight_punctuality TO ROLE flight_developer_role;


GRANT ROLE flight_developer_role TO ROLE SYSADMIN;
GRANT ROLE flight_developer_role TO USER "giraudcgc";
GRANT ROLE flight_developer_role TO USER dennis;
GRANT ROLE flight_developer_role TO USER karl;

SHOW ROLES;
SHOW USERS;

USE ROLE ACCOUNTADMIN;
GRANT ROLE ACCOUNTADMIN TO USER dennis;

SHOW GRANTS TO ROLE flight_developer_role;

USE ROLE SECURITYADMIN;
SHOW USERS;