{# convert a UTC timestamp to Swedish local time (timestamp without time zone) #}
{% macro to_local_time(column) %}
    convert_timezone('UTC', '{{ var("local_timezone") }}', {{ column }}::timestamp_ntz)
{% endmacro %}


{# integer date key yyyymmdd, e.g. 2026-10-07 -> 20261007 #}
{% macro date_key(column) %}
    to_number(to_char({{ column }}, 'YYYYMMDD'))
{% endmacro %}


{# minutes between scheduled and actual time, null if the flight hasn't happened yet #}
{% macro delay_minutes(scheduled, actual) %}
    datediff('minute', {{ scheduled }}, {{ actual }})
{% endmacro %}
