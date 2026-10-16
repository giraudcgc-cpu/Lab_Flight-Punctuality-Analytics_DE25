-- one row per calendar date that has a scheduled flight
with
    flight_dates as (
        select scheduled_utc from {{ ref('src_arrivals') }}
        union all
        select scheduled_utc from {{ ref('src_departures') }}
    ),

    dates as (
        select distinct {{ to_local_time('scheduled_utc') }}::date as full_date
        from flight_dates
    )

select
    {{ date_key('full_date') }} as date_key,
    full_date,
    dayname(full_date) as day_name,
    dayofweekiso(full_date) in (6, 7) as is_weekend
from dates
