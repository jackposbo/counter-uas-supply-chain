[README.md](https://github.com/user-attachments/files/35246141/README.md)
# Counter-UAS Supply Chain: Where the China Dependency Went

US reliance on China for small drone motors looks like it is falling. The countries replacing China are buying more Chinese magnets to build them. This repo holds the public trade data analysis behind that finding.

## Findings

| Finding | 2021 | 2023 | 2025 |
| --- | --- | --- | --- |
| China's share of US permanent magnet imports (value) | 73.7% | 80.0% | 72.4% |
| China's share of US lithium-ion battery imports (value) | 54.2% | 70.7% | 59.3% |
| China's share of US small DC motor imports (value) | 16.9% | 14.8% | 12.4% |
| Vietnam's share of US small DC motor imports (value) | 1.8% | 2.3% | 5.3% |
| China's magnet exports to Vietnam (tonnes) | 9,456 | 8,453 | 11,006 |
| Share of Vietnam's small DC motor exports going to the US | 21.3% | 24.6% | not yet reported |

- China's direct share of small motors fell while Vietnam's nearly tripled.
- Over 2023 to 2025, Vietnam's purchases of Chinese magnets rose 30%.
- About one in four of Vietnam's small DC motor exports goes to the US, and that share rose each year reported.

## Limits

Country totals cannot trace a specific magnet into a specific motor for a specific buyer. Vietnam uses magnets in many products that are not sold to the US. These results are consistent with the dependency moving down a tier, not proof of it. Confirming it supplier by supplier needs shipment-level supply chain mapping.

## Scripts

| Script | Source | What it pulls |
| --- | --- | --- |
| `us_imports_by_country.py` | US Census Bureau trade API | US imports of HTS 8505.11, 8507.60 and 8501.31 by country, 2021 to 2025, with country shares computed in SQL (DuckDB) |
| `china_magnet_exports.py` | UN Comtrade | China's exports of HTS 8505.11 to Vietnam and Mexico, 2021 to 2025 |
| `vietnam_motor_exports.py` | UN Comtrade | Vietnam's exports of HTS 8501.31 to the world and to the US |

## Run it

```
pip3 install pandas requests duckdb
export CENSUS_API_KEY=your_key   # free: api.census.gov/data/key_signup.html
python3 us_imports_by_country.py
python3 china_magnet_exports.py
python3 vietnam_motor_exports.py
```

The public APIs are slow and rate limited, so each script retries and waits between requests.

Jack Osborne, November 2026
