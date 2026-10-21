USE ROLE flight_developer_role;
USE WAREHOUSE flight_wh;
USE DATABASE flight_punctuality;

SHOW TABLES IN SCHEMA staging;

--- 10 airports x 3 days in each table ---
SELECT query_airport, query_date, COUNT(*) FROM staging.arrivals   GROUP BY ALL ORDER BY 1, 2;
SELECT query_airport, query_date, COUNT(*) FROM staging.departures GROUP BY ALL ORDER BY 1, 2;

--- wikipedia tables ---
SELECT COUNT(*) FROM staging.wiki_airports;
SELECT COUNT(*) FROM staging.wiki_airlines;

SHOW COLUMNS IN TABLE flight_punctuality.staging.wiki_airports;

SHOW COLUMNS IN TABLE flight_punctuality.staging.wiki_airlines;


--- Checking all tables that dlt created ---
SHOW TABLES IN SCHEMA staging;

--- every field per table ---
SHOW COLUMNS IN TABLE staging.arrivals;
SHOW COLUMNS IN TABLE staging.departures;
SHOW COLUMNS IN TABLE staging.wiki_airports;
SHOW COLUMNS IN TABLE staging.wiki_airlines;

-- checking rreal rows, to see what the values look like
SELECT * FROM staging.arrivals      LIMIT 5;
SELECT * FROM staging.wiki_airlines LIMIT 5;
