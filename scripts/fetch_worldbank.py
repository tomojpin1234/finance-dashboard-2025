import os
from typing import Dict, List

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests

# Directory to save raw data
RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Indicators to fetch
INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_usd",  # GDP (current US$)
    "FP.CPI.TOTL.ZG": "cpi_percent",  # Inflation (CPI %)
    "SL.UEM.TOTL.ZS": "unemployment_pct",  # Unemployment (% of labor force)
    "FR.INR.RINR": "interest_rate",  # Interest rates
}

# Countries by ISO2 code
COUNTRIES = {
    "US": "United States",
    "DE": "Germany",
    "PL": "Poland",
    "JP": "Japan",
    "FR": "France",
    "GB": "United Kingdom",
    "IT": "Italy",
    "CN": "China",
    "IN": "India",
    "BR": "Brazil",
    "CA": "Canada",
    "AU": "Australia",
}


def fetch_indicator_data(country: str, indicator: str) -> pd.DataFrame:
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for {country}, {indicator}")

    json_data = response.json()
    if len(json_data) < 2 or not isinstance(json_data[1], list):
        raise Exception(f"No data found for {country}, {indicator}")

    records = [
        {"year": int(item["date"]), "value": item["value"]}
        for item in json_data[1]
        if item["value"] is not None
    ]

    df = pd.DataFrame(records)
    df["country"] = country
    df["indicator"] = indicator
    return df


def fetch_all_data(
    countries: Dict[str, str], indicators: Dict[str, str]
) -> pd.DataFrame:
    all_dfs = []
    for country_code in countries:
        for indicator_code in indicators:
            print(
                f"Fetching {indicators[indicator_code]} for {countries[country_code]}..."
            )
            df = fetch_indicator_data(country_code, indicator_code)
            all_dfs.append(df)
    return pd.concat(all_dfs, ignore_index=True)


def save_to_parquet(df: pd.DataFrame, path: str):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)
    print(f"Saved {len(df)} records to {path}")


if __name__ == "__main__":
    df = fetch_all_data(COUNTRIES, INDICATORS)
    save_to_parquet(df, os.path.join(RAW_DATA_DIR, "macro_data.parquet"))
