with
    flights as (
        select * from {{ ref('src_arrivals') }}
        union all
        select * from {{ ref('src_departures') }}
    ),

    swedavia_airports as (
        select distinct
            swedavia_airport_iata as airport_iata,
            null as api_airport_name,
            true as is_swedavia_airport
        from flights
    ),

    other_airports as (
        select
            other_airport_iata as airport_iata,
            max(other_airport_name) as api_airport_name,
            false as is_swedavia_airport
        from flights
        where other_airport_iata is not null
        group by other_airport_iata
    ),

    all_airports as (
        select
            airport_iata,
            max(api_airport_name) as api_airport_name,
            max(is_swedavia_airport) as is_swedavia_airport
        from (
            select * from swedavia_airports
            union all
            select * from other_airports
        )
        group by airport_iata
    ),

    wiki_airports as (select * from {{ ref('src_wiki_airports') }})

select
    {{ dbt_utils.generate_surrogate_key(['a.airport_iata']) }} as airport_key,
    a.airport_iata,
    coalesce(w.airport_name, a.api_airport_name, a.airport_iata) as airport_name,
    case
        when a.is_swedavia_airport then 'Swedavia airport'
        when w.airport_iata is not null then 'Other Swedish airport'
        else 'Foreign airport'
    end as airport_category
from all_airports a
left join wiki_airports w
    on a.airport_iata = w.airport_iata
