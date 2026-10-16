with stg_arrivals as (select * from {{ source('staging', 'arrivals') }})

select
    flight_id,
    query_airport as swedavia_airport_iata,
    flight_leg_identifier__departure_airport_iata as other_airport_iata,
    departure_airport_english as other_airport_name,
    airline_operator__iata as airline_iata,
    airline_operator__icao as airline_icao,
    airline_operator__name as airline_name,
    location_and_status__flight_leg_status as status_code,
    location_and_status__flight_leg_status_english as status_name,
    arrival_time__scheduled_utc as scheduled_utc,
    arrival_time__actual_utc as actual_utc
from stg_arrivals
where arrival_time__scheduled_utc is not null
    -- DEL = deleted from the flight plan (re-planned or never operated), not a real flight
    and coalesce(location_and_status__flight_leg_status, '') != 'DEL'
qualify row_number() over (
    partition by flight_id, query_airport, arrival_time__scheduled_utc
    order by extracted_at desc
) = 1

