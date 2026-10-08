# Forecast methodology, results, and limitations

## Objective

Predict the **next day's total tax-inclusive sales across all three stores**, not demand by SKU or inventory requirements.

## Data and feature design

The analysis used 89 daily totals dated **1 January–30 March 2022**. A supervised learning table removed the first seven dates because lag features were not yet available. Features were:

1. Day of week (0–6)
2. Yesterday's sales (`t-1`)
3. Sales from seven days earlier (`t-7`)
4. Mean sales over the previous seven days (`t-7` through `t-1`)

All lag features are shifted backwards, preventing use of same-day sales as an input. An important nuance: the 14-day holdout evaluates a **rolling one-day-ahead** task using previously **observed** sales for lag inputs, not an unassisted 14-day multi-step forecast.

## Train/test validation

- First 68 usable dated rows: training period, 8 January–16 March 2022.
- Last 14 usable rows: chronological test period, 17–30 March 2022.
- Model: `RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=3, random_state=42)`.
- Baseline: use sales from the same weekday a week earlier.
- Metric: mean absolute error (MAE) in dollars.

The original daily-sales CSV was checked separately against the supplied notebook; it produces **MAE $1,345.58** for Random Forest and **$1,813.09** for the baseline, a **25.8%** reduction on this holdout. After the evaluation, refitting on all 82 usable rows predicted **$3,589.16** for 31 March 2022. The dataset does not contain that day's actual total, so the forecast cannot be verified.

## Why results should be interpreted cautiously

- Only **14 test days** and **three months of history**. Results may not generalise.
- Errors are sizeable relative to daily sales and the model misses sharp peaks/dips.
- Missing drivers include promotions, holidays, weather, SKU prices and stock levels.
- The model estimates **sales value**, not physical stock demand or units needed.
- Lag inputs for each holdout day rely on recently observed sales. This is appropriate for a one-step rolling forecast, but not equivalent to forecasting all 14 days at once.
- This is an academic case study, not a production forecasting service.

## Reproducing the model

Run `python src/forecast.py --input YOUR_DAILY_TOTALS.csv --output-dir results` with a daily CSV containing `Date` and `Sum of Total`, without missing dates or duplicate date rows. The included synthetic sample is for functional demonstration, not original metric reproduction.
