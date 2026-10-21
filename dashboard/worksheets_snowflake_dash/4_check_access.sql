USE ROLE flight_reporter_role;
USE WAREHOUSE flight_wh;
USE DATABASE flight_punctuality;

--- this should WORK (the dashboard reads the marts) ---
SELECT * FROM marts.mart_flights LIMIT 10;
SELECT * FROM marts.mart_punctuality_daily ORDER BY delayed_flights DESC LIMIT 20;

--- this should FAIL (the reporter can only read marts) ---
SELECT * FROM warehouse.fct_arrivals LIMIT 1;

