with stg_wiki_airports as (select * from {{ source('staging', 'wiki_airports') }})

select
    upper(trim(iata)) as airport_iata,
    airportname as airport_name
from stg_wiki_airports
where iata is not null
qualify row_number() over (partition by upper(trim(iata)) order by icao nulls last) = 1
