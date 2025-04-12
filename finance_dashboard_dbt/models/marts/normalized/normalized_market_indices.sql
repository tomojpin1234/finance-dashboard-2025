-- models/marts/normalized/normalized_market_indices.sql


with monthly_index as (
    select
        country,
        date_trunc(date, month) as month_start,
        avg(close) as monthly_avg_close
    from {{ ref('stg_market_indices') }}
    group by country, month_start
),

with_base as (
    select
        *,
        first_value(monthly_avg_close) over (
            partition by country order by month_start
        ) as base_close
    from monthly_index
),

final as (
    select
        country,
        month_start,
        safe_divide(monthly_avg_close - base_close, base_close) as pct_from_start
    from with_base
)

select *
from final