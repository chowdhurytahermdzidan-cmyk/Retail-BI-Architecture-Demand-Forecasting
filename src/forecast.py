"""Chronological one-day-ahead aggregate retail sales forecasting.

Run: python src/forecast.py --input data/sample_daily_sales.csv --output-dir results
"""
from __future__ import annotations

import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FEATURES = ["DayOfWeek", "SalesYesterday", "SalesLastWeek", "AvgPrior7Days"]


def load_data(input_path: Path) -> pd.DataFrame:
    data = pd.read_csv(input_path)
    if "Date" not in data.columns:
        raise ValueError("Input CSV must contain a Date column")
    if "Sum of Total" in data.columns:
        data = data.rename(columns={"Sum of Total": "DailySales"})
    if "DailySales" not in data.columns:
        raise ValueError("Input CSV must include Sum of Total or DailySales")
    data = data[["Date", "DailySales"]].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="raise").dt.normalize()
    data["DailySales"] = pd.to_numeric(data["DailySales"], errors="raise")
    if data.isna().any().any():
        raise ValueError("Input contains missing Date or sales values")
    if (data["DailySales"] < 0).any():
        raise ValueError("Input contains negative sales; review before modelling")
    if data["Date"].duplicated().any():
        raise ValueError("Date must appear exactly once; aggregate by day first")
    data = data.sort_values("Date").reset_index(drop=True)
    if len(data) >= 2 and not data["Date"].diff().dropna().eq(pd.Timedelta(days=1)).all():
        raise ValueError("Daily dates must be consecutive without gaps")
    return data


def build_features(data: pd.DataFrame) -> pd.DataFrame:
    model = data.copy()
    model["DayOfWeek"] = model["Date"].dt.dayofweek
    model["SalesYesterday"] = model["DailySales"].shift(1)
    model["SalesLastWeek"] = model["DailySales"].shift(7)
    model["AvgPrior7Days"] = model["DailySales"].shift(1).rolling(7).mean()
    return model.dropna().reset_index(drop=True)


def make_model() -> RandomForestRegressor:
    return RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=3, random_state=42)


def forecast(data: pd.DataFrame, test_days: int = 14):
    model_data = build_features(data)
    if test_days < 1 or len(model_data) <= test_days:
        raise ValueError("Need more than test_days usable rows after the seven-day lag")
    train, test = model_data.iloc[:-test_days], model_data.iloc[-test_days:].copy()
    rf = make_model().fit(train[FEATURES], train["DailySales"])
    test["RandomForest"] = rf.predict(test[FEATURES])
    test["PreviousWeekBaseline"] = test["SalesLastWeek"]
    mae_rf = float(mean_absolute_error(test["DailySales"], test["RandomForest"]))
    mae_baseline = float(mean_absolute_error(test["DailySales"], test["PreviousWeekBaseline"]))
    fitted = make_model().fit(model_data[FEATURES], model_data["DailySales"])
    next_date = data["Date"].max() + pd.Timedelta(days=1)
    future = pd.DataFrame([{
        "DayOfWeek": next_date.dayofweek,
        "SalesYesterday": data["DailySales"].iloc[-1],
        "SalesLastWeek": data["DailySales"].iloc[-7],
        "AvgPrior7Days": data["DailySales"].iloc[-7:].mean(),
    }])[FEATURES]
    one_day_pred = float(fitted.predict(future)[0])
    return test, mae_rf, mae_baseline, next_date, one_day_pred, len(train)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/sample_daily_sales.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--test-days", type=int, default=14)
    args = parser.parse_args()
    series = load_data(args.input)
    test, rf_mae, baseline_mae, next_date, next_pred, train_count = forecast(series, args.test_days)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    test[["Date", "DailySales", "RandomForest", "PreviousWeekBaseline"]].to_csv(args.output_dir / "holdout_predictions.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(test["Date"], test["DailySales"], marker="o", label="Actual daily sales")
    ax.plot(test["Date"], test["RandomForest"], marker="o", label="Random forest")
    ax.plot(test["Date"], test["PreviousWeekBaseline"], linestyle="--", label="Previous-week baseline")
    ax.set(xlabel="Date", ylabel="Daily sales ($)", title="Rolling one-day-ahead forecast evaluation")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.grid(alpha=.2)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(args.output_dir / "forecast_evaluation.png", dpi=180)
    plt.close(fig)
    print(f"Daily rows: {len(series)} | Training: {train_count} | Holdout: {len(test)}")
    print(f"Random forest MAE: ${rf_mae:,.2f}")
    print(f"Previous-week baseline MAE: ${baseline_mae:,.2f}")
    print(f"MAE improvement: {(baseline_mae-rf_mae)/baseline_mae*100:.1f}%" if baseline_mae else "Baseline MAE is zero; relative comparison undefined")
    print(f"Forecast for {next_date.date()}: ${next_pred:,.2f} (no actual observation provided)")
    print(f"Results saved to: {args.output_dir}")

if __name__ == '__main__':
    main()
