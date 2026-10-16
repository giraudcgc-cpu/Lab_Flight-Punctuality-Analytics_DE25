USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS flight_dbt_user
    TYPE = LEGACY_SERVICE
    PASSWORD = "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"
    DEFAULT_ROLE = flight_dbt_role
    DEFAULT_WAREHOUSE = flight_wh
    DEFAULT_NAMESPACE = 'flight_punctuality.warehouse'
    COMMENT = 'Service user for dbt (transformation)';
ALTER USER flight_dbt_user SET PASSWORD =  "{{ env_var('DBT_SNOWFLAKE_PASSWORD') }}"; -- used to replace the previous user password created
-- check
DESC USER flight_dbt_user;