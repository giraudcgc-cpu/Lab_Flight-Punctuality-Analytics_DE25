with
    flights as (
        select * from {{ ref('src_arrivals') }}
        union all
        select * from {{ ref('src_departures') }}
    ),

    airlines as (
        select
            airline_iata,
            airline_icao,
            max(airline_name) as api_airline_name
        from flights
        group by airline_iata, airline_icao
    ),

    wiki_airlines as (select * from {{ ref('src_wiki_airlines') }})

select
    {{ dbt_utils.generate_surrogate_key(['a.airline_iata', 'a.airline_icao']) }} as airline_key,
    a.airline_iata,
    a.airline_icao,
    coalesce(a.api_airline_name, w.airline_name, 'Unknown airline') as airline_name
from airlines a
left join wiki_airlines w
    on a.airline_icao = w.airline_icao
