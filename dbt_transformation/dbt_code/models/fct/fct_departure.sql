with
    departures as (
        select
            *,
            -- punctuality can only be measured once the flight has an actual time
            {{ delay_minutes('scheduled_utc', 'actual_utc') }} as raw_delay_minutes
        from {{ ref('src_departures') }}
    )

select
    -- keys
    {{ dbt_utils.generate_surrogate_key(['flight_id', 'swedavia_airport_iata', 'scheduled_utc']) }} as departure_id,
    {{ date_key(to_local_time('scheduled_utc')) }} as date_key,
    {{ dbt_utils.generate_surrogate_key(['swedavia_airport_iata']) }} as departure_airport_key,
    {{ dbt_utils.generate_surrogate_key(['other_airport_iata']) }} as destination_airport_key,
    {{ dbt_utils.generate_surrogate_key(['airline_iata', 'airline_icao']) }} as airline_key,
    {{ dbt_utils.generate_surrogate_key(['status_code']) }} as flight_status_key,

    -- degenerate dimension and times
    flight_id,
    {{ to_local_time('scheduled_utc') }} as scheduled_departure_local,
    {{ to_local_time('actual_utc') }} as actual_departure_local,

    -- measures
    raw_delay_minutes as delay_minutes,
    coalesce(raw_delay_minutes > {{ var('delay_threshold_minutes') }}, false) as is_delayed,
    coalesce(status_code = 'CAN', false) as is_cancelled,
    actual_utc is not null as is_completed
from departures
