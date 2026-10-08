"""Generate an original, deterministic synthetic fixture for demonstrating the forecasting code.

These values are NOT a transformed copy of the university dataset.
"""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
dates = pd.date_range('2022-01-01', periods=89, freq='D')
t = np.arange(len(dates))
weekly = 430 * np.sin(2 * np.pi * t / 7)
trend = 8 * t
noise = rng.normal(0, 650, len(dates))
values = np.maximum(700, 3250 + weekly + trend + noise)
frame = pd.DataFrame({'Date': dates.strftime('%Y-%m-%d'), 'Sum of Total': np.round(values, 2)})
out = Path(__file__).resolve().parents[1] / 'data' / 'sample_daily_sales.csv'
frame.to_csv(out, index=False)
print(f'Saved synthetic demo data to {out} ({len(frame)} days).')
