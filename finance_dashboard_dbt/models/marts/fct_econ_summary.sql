-- models/marts/fct_econ_summary.sql

with macro_data as (
    select
        country,
        year,
        gdp_usd,
        cpi_percent,
        unemployment_pct,  
        interest_rate,
        lag(gdp_usd) over (partition by country order by year) as prev_gdp
    from {{ ref('stg_macro_data') }}
),

macro_enriched as (
    select
        country,
        year,
        gdp_usd,
        prev_gdp,
        cpi_percent,
        unemployment_pct,
        interest_rate,
        safe_divide(gdp_usd - prev_gdp, prev_gdp) as gdp_growth_pct
    from macro_data
),

market as (
    select
        country,
        extract(year from date) as year,
        avg(pct_change) as avg_index_change_pct,
        avg(close) as index_close
    from {{ ref('stg_market_indices') }}
    group by country, year
),

final as (
    select
        m.country,
        m.year,
        m.gdp_usd,
        m.prev_gdp,
        m.gdp_growth_pct,
        m.cpi_percent,
        m.unemployment_pct,
        m.interest_rate,
        mk.avg_index_change_pct,
        mk.index_close,
        parse_date('%Y', cast(m.year as string)) as year_date
    from macro_enriched m
    left join market mk using (country, year)
)

select *
from final