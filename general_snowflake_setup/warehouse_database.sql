USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS flight_wh
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for the flight punctuality pipeline';

CREATE DATABASE IF NOT EXISTS flight_punctuality;

CREATE SCHEMA IF NOT EXISTS flight_punctuality.staging;
CREATE SCHEMA IF NOT EXISTS flight_punctuality.warehouse;
CREATE SCHEMA IF NOT EXISTS flight_punctuality.marts;

SHOW SCHEMAS IN DATABASE flight_punctuality;
SHOW WAREHOUSES;