-- aggregated punctuality per date, direction, Swedavia airport and airline
with mart_flights as (select * from {{ ref('mart_flight') }})

select
    flight_date,
    direction,
    swedavia_airport_iata,
    swedavia_airport,
    airline,
    count(*) as total_flights,
    count_if(is_completed) as completed_flights,
    count_if(is_delayed) as delayed_flights,
    count_if(is_on_time) as on_time_flights,
    count_if(is_cancelled) as cancelled_flights,
    round(avg(case when is_delayed then delay_minutes end), 1) as avg_delay_minutes_when_delayed,
    -- share of flights that have landed / departed (punctuality is only known for those)
    round(100 * count_if(is_delayed) / nullif(count_if(is_completed), 0), 1) as pct_delayed
from mart_flights
group by flight_date, direction, swedavia_airport_iata, swedavia_airport, airline
