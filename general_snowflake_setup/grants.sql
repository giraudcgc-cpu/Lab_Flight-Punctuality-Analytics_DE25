USE ROLE SECURITYADMIN;

--- Warehouse | database | schema ---
GRANT USAGE ON WAREHOUSE flight_wh TO ROLE flight_developer_role;
GRANT USAGE ON DATABASE flight_punctuality TO ROLE flight_developer_role;
GRANT USAGE ON ALL SCHEMAS IN DATABASE flight_punctuality TO ROLE flight_developer_role;

--- granting roles ---
GRANT ROLE flight_developer_role TO ROLE SYSADMIN;
GRANT ROLE flight_developer_role TO USER "giraudcgc";
GRANT ROLE flight_developer_role TO USER dennis;
GRANT ROLE flight_developer_role TO USER karl;

--- check ---
SHOW ROLES;
SHOW USERS;


SHOW GRANTS TO ROLE flight_developer_role;

USE ROLE SECURITYADMIN;
SHOW USERS;