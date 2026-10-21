USE ROLE SYSADMIN;

--- Warehouse ---
CREATE WAREHOUSE IF NOT EXISTS flight_wh
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for the flight punctuality pipeline';

--- database ---
CREATE DATABASE IF NOT EXISTS flight_punctuality;

--- schema ---
CREATE SCHEMA IF NOT EXISTS flight_punctuality.staging;
CREATE SCHEMA IF NOT EXISTS flight_punctuality.warehouse;
CREATE SCHEMA IF NOT EXISTS flight_punctuality.marts;

--- check ---
SHOW SCHEMAS IN DATABASE flight_punctuality;
SHOW WAREHOUSES;