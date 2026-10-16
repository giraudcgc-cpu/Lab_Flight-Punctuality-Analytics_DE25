USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS flight_dbt_role
    COMMENT = 'dbt: transform staging -> warehouse -> marts';

-- check
SHOW ROLES LIKE 'flight_dbt_role';