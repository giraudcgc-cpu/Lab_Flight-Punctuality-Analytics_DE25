USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS flight_dlt_user
    PASSWORD = "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"
    DEFAULT_ROLE = flight_dlt_role
    DEFAULT_WAREHOUSE = flight_wh
    DEFAULT_NAMESPACE = 'flight_punctuality.staging';
    ALTER USER flight_dlt_user SET PASSWORD = "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}";
    
--- Checking ---
DESC USER flight_dlt_user;
