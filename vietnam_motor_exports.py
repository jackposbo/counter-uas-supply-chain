"""How much of Vietnam's small DC motor exports go to the US, 2021-2025.

Source: UN Comtrade public API (no key needed). Vietnam is the reporter.
HTS 8501.31 = DC motors and generators, output 750 W or less.
Run: python3 vietnam_motor_exports.py
"""
import time
import warnings
warnings.filterwarnings("ignore")
import requests
import pandas as pd

URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
PARTNERS = {"0": "World", "842": "United States"}

def pull(partner_code, year):
    params = {
        "reporterCode": "704",  # Vietnam
        "partnerCode": partner_code,
        "flowCode": "X",        # exports
        "cmdCode": "850131",    # small DC motors
        "period": str(year),
    }
    for attempt in range(4):
        try:
            data = requests.get(URL, params=params, timeout=120).json().get("data", [])
            if data:
                return data[0].get("primaryValue")
            print(f"  empty answer, waiting and retrying ({attempt + 1}/4)...")
        except Exception as e:
            print(f"  attempt {attempt + 1} failed ({type(e).__name__}), retrying...")
        time.sleep(15 * (attempt + 1))
    return None

rows = []
for year in range(2021, 2026):
    values = {}
    for code, name in PARTNERS.items():
        print(f"Pulling Vietnam motor exports to {name}, {year}...", flush=True)
        values[name] = pull(code, year)
        time.sleep(8)  # the public API limits how fast you can ask
    world, us = values["World"], values["United States"]
    share = round(100 * us / world, 1) if world and us else None
    rows.append({"year": year, "to_world_usd": world, "to_us_usd": us, "us_share_pct": share})

df = pd.DataFrame(rows)
print()
print(df.to_string(index=False))
df.to_csv("vietnam_motor_exports.csv", index=False)
