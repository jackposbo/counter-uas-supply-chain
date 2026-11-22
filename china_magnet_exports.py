"""China's permanent magnet exports to Vietnam and Mexico, 2021-2025.

Source: UN Comtrade public API (no key needed). China is the reporter.
Run: python3 china_magnet_exports.py
"""
import time
import warnings
warnings.filterwarnings("ignore")
import requests
import pandas as pd

URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
PARTNERS = {"704": "Vietnam", "484": "Mexico"}

rows = []
for code, name in PARTNERS.items():
    for year in range(2021, 2026):
        params = {
            "reporterCode": "156",  # China
            "partnerCode": code,
            "flowCode": "X",        # exports
            "cmdCode": "850511",    # metal permanent magnets
            "period": str(year),
        }
        print(f"Pulling China magnet exports to {name}, {year}...", flush=True)
        data = None
        for attempt in range(4):
            try:
                data = requests.get(URL, params=params, timeout=120).json().get("data", [])
                if data:
                    break
                # an empty answer usually means "asking too fast": wait and ask again
                print(f"  empty answer, waiting and retrying ({attempt + 1}/4)...")
            except Exception as e:
                print(f"  attempt {attempt + 1} failed ({type(e).__name__}), retrying...")
            time.sleep(15 * (attempt + 1))
        if not data:
            print("  no data yet for this year")
            continue
        for d in data:
            rows.append({"partner": name, "year": year,
                         "value_usd": d.get("primaryValue"), "kg": d.get("netWgt")})
        time.sleep(8)  # the public API limits how fast you can ask

df = pd.DataFrame(rows)
print()
print(df.to_string(index=False))
df.to_csv("china_magnet_exports.csv", index=False)
