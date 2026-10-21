with stg_wiki_airlines as (select * from {{ source('staging', 'wiki_airlines') }})

select
    upper(trim(icao)) as airline_icao,
    airline as airline_name
from stg_wiki_airlines
where icao is not null
qualify row_number() over (
    partition by upper(trim(icao))
    order by
        case
            when comments ilike '%defunct%' or comments ilike '%became%' then 1
            else 0
        end,
        iata nulls last
) = 1