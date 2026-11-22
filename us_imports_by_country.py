"""China's share of US imports of drone-critical components, 2021-2025.

Source: US Census Bureau international trade API (no key needed for light use).
Run: export CENSUS_API_KEY=your_key && python3 us_imports_by_country.py
"""
import os
import time
import warnings
warnings.filterwarnings("ignore")
import requests
import pandas as pd
import duckdb

API = "https://api.census.gov/data/timeseries/intltrade/imports/hs"
KEY = os.environ.get("CENSUS_API_KEY", "")  # free key: api.census.gov/data/key_signup.html
CODES = {
    "850511": "Permanent magnets (metal)",
    "850760": "Lithium-ion batteries",
    "850131": "DC motors, 750 W or less",
}
YEARS = range(2021, 2026)

rows = []
for code, label in CODES.items():
    for year in YEARS:
        params = {
            "get": "CTY_CODE,CTY_NAME,GEN_VAL_YR",
            "COMM_LVL": "HS6",
            "I_COMMODITY": code,
            "time": f"{year}-12",  # December year-to-date = full-year value
            "key": KEY,
        }
        print(f"Pulling {label}, {year}...", flush=True)
        data = None
        for attempt in range(4):  # the Census API is often slow; retry with longer waits
            try:
                r = requests.get(API, params=params, timeout=120)
                if r.status_code == 204:
                    print("  no data for this year, skipping")
                    break
                if "Invalid Key" in r.text:
                    raise SystemExit("Census says the key is invalid. Wait 30-60 min after activating, then rerun.")
                data = r.json()
                break
            except requests.exceptions.RequestException as e:
                print(f"  attempt {attempt + 1} failed ({type(e).__name__}), retrying...")
                time.sleep(10 * (attempt + 1))
        if data is None:
            continue
        df = pd.DataFrame(data[1:], columns=data[0])
        df["hts"], df["component"], df["year"] = code, label, year
        rows.append(df)

imports = pd.concat(rows)
imports["value_usd"] = pd.to_numeric(imports["GEN_VAL_YR"], errors="coerce")

# SQL step: China's share, plus the third countries where assembly can hide Chinese inputs
shares = duckdb.sql("""
    WITH totals AS (
        SELECT component, year, value_usd AS total
        FROM imports WHERE CTY_NAME = 'TOTAL FOR ALL COUNTRIES'
    )
    SELECT i.component, i.year, i.CTY_NAME AS country,
           ROUND(100 * i.value_usd / t.total, 1) AS share_pct
    FROM imports i JOIN totals t USING (component, year)
    WHERE i.CTY_NAME IN ('CHINA', 'VIETNAM', 'MEXICO', 'THAILAND', 'MALAYSIA')
    ORDER BY i.component, i.year, share_pct DESC
""").df()

print(shares.to_string(index=False))
shares.to_csv("cuas_import_shares.csv", index=False)
