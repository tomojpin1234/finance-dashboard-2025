-- models/staging/stg_market_indices.sql

with source as (
    select
        country,
        -- temporarily removing guard to test data flow
        timestamp_micros(cast(date / 1000 as int64)) as date,
        close
    from {{ source('finance_dashboard', 'market_indices') }}
),

cleaned as (
    select
        country,
        date,
        extract(year from date) as year,
        close,
        lag(close) over (partition by country order by date) as prev_close
    from source
    where date is not null
),

enriched as (
    select
        country,
        date,
        year,
        close,
        prev_close,
        safe_divide(close - prev_close, prev_close) as pct_change
    from cleaned
)

select *
from enriched