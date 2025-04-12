import os
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yfinance as yf

INDEX_SYMBOLS = {
    "US": "^GSPC",  # S&P 500
    "DE": "^GDAXI",  # DAX
    "JP": "^N225",  # Nikkei 225
    "PL": "^WIG20",  # Poland
    "FR": "^FCHI",  # CAC 40
    "GB": "^FTSE",  # FTSE 100
    "IT": "FTSEMIB.MI",  # FTSE MIB (Italy)
    "CN": "000001.SS",  # SSE Composite Index (China)
    "IN": "^BSESN",  # BSE Sensex (India)
    "BR": "^BVSP",  # Bovespa (Brazil)
    "CA": "^GSPTSE",  # S&P/TSX (Canada)
    "AU": "^AXJO",  # ASX 200 (Australia)
}

# Date range (can be changed later)
START_DATE = "2000-01-01"
END_DATE = datetime.today().date()

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


def fetch_index_data(country_code: str, symbol: str, start=START_DATE, end=END_DATE):
    print(f"Fetching index data for {country_code} ({symbol})...")
    df = yf.download(symbol, start=start, end=end)

    # 🧹 Flatten MultiIndex columns
    df.columns = [
        col if isinstance(col, str) else "_".join(filter(None, col))
        for col in df.columns
    ]

    df.reset_index(inplace=True)
    df["country"] = country_code

    # Dynamically get the correct 'Close' column
    close_col = next((col for col in df.columns if col.startswith("Close")), None)
    if close_col is None:
        raise ValueError(f"Close column not found for {symbol}")

    df = df[["Date", close_col, "country"]]
    df.rename(columns={close_col: "Close"}, inplace=True)

    return df


def save_to_parquet(df: pd.DataFrame, output_path: str):
    df["Date"] = pd.to_datetime(df["Date"])
    df["Date"] = df["Date"].astype("int64") // 1000  # microseconds
    df.columns = [str(col).replace(" ", "_") for col in df.columns]

    table = pa.Table.from_pandas(df)
    pq.write_table(table, output_path)

    print(f"✅ Saved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    all_data = []
    for country, symbol in INDEX_SYMBOLS.items():
        df = fetch_index_data(country, symbol)
        all_data.append(df)

    result_df = pd.concat(all_data, ignore_index=True)
    save_to_parquet(result_df, os.path.join(RAW_DATA_DIR, "market_indices.parquet"))
