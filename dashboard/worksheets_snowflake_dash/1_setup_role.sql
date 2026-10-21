USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS flight_reporter_role
    COMMENT = 'Streamlit dashboard / stakeholders: read the marts only';

-- check
SHOW ROLES LIKE 'flight_reporter_role';
