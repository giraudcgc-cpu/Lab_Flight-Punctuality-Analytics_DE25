SELECT event_timestamp, error_code, error_message, first_authentication_factor
FROM TABLE(SNOWFLAKE.INFORMATION_SCHEMA.LOGIN_HISTORY_BY_USER(USER_NAME => 'FLIGHT_DBT_USER'))
ORDER BY event_timestamp DESC
LIMIT 5;

--- check ---
DESC USER flight_dbt_user;