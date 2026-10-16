-- one row per flight leg status code from the API
-- codes seen in the data: LAN = landed, ACT = departed, CAN = cancelled,
-- SCH = scheduled, SEQ = new estimated time (DEL = deleted is filtered out in src)
with
    statuses as (
        select status_code, status_name from {{ ref('src_arrivals') }}
        union all
        select status_code, status_name from {{ ref('src_departures') }}
    ),

    -- the API adds the time to some statuses, e.g. 'Landed 07:55' -> 'Landed'
    statuses_clean as (
        select
            status_code,
            trim(regexp_replace(status_name, '[0-9]{2}:[0-9]{2}', '')) as status_name
        from statuses
    )

select
    {{ dbt_utils.generate_surrogate_key(['status_code']) }} as flight_status_key,
    coalesce(status_code, 'UNKNOWN') as status_code,
    coalesce(max(status_name), 'Unknown') as status_name,
    case
        when status_code = 'CAN' then 'Cancelled'
        when status_code in ('LAN', 'ACT') then 'Completed'
        else 'Not yet completed'
    end as status_category
from statuses_clean
group by status_code
