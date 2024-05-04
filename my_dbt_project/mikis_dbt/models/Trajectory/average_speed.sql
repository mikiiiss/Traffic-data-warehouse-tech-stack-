{{ config(materialized='view') }}

with avg_speed_at_each_time as (
    select 
        time, 
        avg(speed) as average_speed
    from {{ ref('speed_on_trajectory') }}   
    group by time
    order by average_speed DESC
)

select *
from avg_speed_at_each_time