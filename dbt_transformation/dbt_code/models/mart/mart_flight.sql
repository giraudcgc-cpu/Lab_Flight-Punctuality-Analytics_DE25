-- one row per flight (arrivals and departures) with readable names,
-- ready for the dashboard: delayed flights by airport, airline and date
with
    fct_arrivals as (select * from {{ ref('fct_arrival') }}),
    fct_departures as (select * from {{ ref('fct_departure') }}),
    dim_airport as (select * from {{ ref('dim_airport') }}),
    dim_airline as (select * from {{ ref('dim_airline') }}),
    dim_date as (select * from {{ ref('dim_date') }}),
    dim_flight_status as (select * from {{ ref('dim_flight_status') }}),

    flights as (
        select
            'Arrival' as direction,
            arrival_id as flight_key,
            date_key,
            arrival_airport_key as swedavia_airport_key,
            origin_airport_key as other_airport_key,
            airline_key,
            flight_status_key,
            flight_id,
            scheduled_arrival_local as scheduled_time_local,
            actual_arrival_local as actual_time_local,
            delay_minutes,
            is_delayed,
            is_cancelled,
            is_completed
        from fct_arrivals

        union all

        select
            'Departure' as direction,
            departure_id as flight_key,
            date_key,
            departure_airport_key as swedavia_airport_key,
            destination_airport_key as other_airport_key,
            airline_key,
            flight_status_key,
            flight_id,
            scheduled_departure_local as scheduled_time_local,
            actual_departure_local as actual_time_local,
            delay_minutes,
            is_delayed,
            is_cancelled,
            is_completed
        from fct_departures
    )

select
    f.flight_key,
    f.direction,
    d.full_date as flight_date,
    d.day_name,
    d.is_weekend,
    f.scheduled_time_local,
    f.actual_time_local,
    hour(f.scheduled_time_local) as scheduled_hour_local,
    sa.airport_iata as swedavia_airport_iata,
    sa.airport_name as swedavia_airport,
    oa.airport_name as other_airport,
    oa.airport_category as other_airport_category,
    al.airline_name as airline,
    f.flight_id,
    st.status_name as flight_status,
    st.status_category,
    f.delay_minutes,
    f.is_delayed,
    -- on time = landed / departed within the delay threshold
    f.is_completed and not f.is_delayed as is_on_time,
    f.is_cancelled,
    f.is_completed
from flights f
left join dim_date d on f.date_key = d.date_key
left join dim_airport sa on f.swedavia_airport_key = sa.airport_key
left join dim_airport oa on f.other_airport_key = oa.airport_key
left join dim_airline al on f.airline_key = al.airline_key
left join dim_flight_status st on f.flight_status_key = st.flight_status_key
