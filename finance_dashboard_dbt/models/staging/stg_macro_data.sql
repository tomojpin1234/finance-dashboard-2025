-- models/staging/stg_macro_data.sql

with source as (
    select
        country,
        indicator,
        cast(year as int64) as year,
        value
    from {{ source('finance_dashboard', 'macro_data') }}
),

gdp as (
    select country, year, value as gdp_usd
    from source
    where indicator = 'NY.GDP.MKTP.CD'
),

cpi as (
    select country, year, value as cpi_percent
    from source
    where indicator = 'FP.CPI.TOTL.ZG'
),

unemployment as (
    select country, year, value as unemployment_pct
    from source
    where indicator = 'SL.UEM.TOTL.ZS'
),

interest as (
    select country, year, value as interest_rate
    from source
    where indicator = 'FR.INR.RINR'
),

final as (
    select
        gdp.country,
        gdp.year,
        gdp.gdp_usd,
        cpi.cpi_percent,
        unemployment.unemployment_pct,
        interest.interest_rate 
    from gdp
    left join cpi using (country, year)
    left join unemployment using (country, year)
    left join interest using (country, year)
)

select *
from final