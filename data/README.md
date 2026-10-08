# Data availability and format

The transaction-level source workbook was supplied for university coursework and has **not** been included here because public redistribution permission is not established.

Included: `sample_daily_sales.csv`, **independently generated synthetic data** from `scripts/generate_sample_data.py`. It is only a demonstration fixture; it cannot reproduce the original assessment's sales totals or model scores.

## Expected input CSV

| Column | Type | Meaning |
|---|---|---|
| `Date` | ISO-like date | Each successive calendar day, e.g. `2022-01-01` |
| `Sum of Total` / `DailySales` | numeric | Combined sales across the three branches for that day |

The pipeline rejects missing dates, duplicate dates, missing/non-numeric sales, negative sales, and fewer than 22 days of records (at least eight training rows plus fourteen test rows). It uses `--test-days 14` by default.

If you have permission to use the original daily-total export locally, supply its CSV path via `--input`. **Do not commit that source data to GitHub without explicit permission.**
