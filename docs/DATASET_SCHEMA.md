# MATRIX Dataset Schema (Docs-First)

## OHLCV Contract (5m Timeframe)
- **Index**: datetime (UTC, tz-aware), strictly increasing, no duplicates
- **Columns**: [open, high, low, close, volume] (float64)
- **Optional**: [quote_volume] ignored
- **Gaps Policy**: mark gaps; no forward-fill over train/test borders

## Feature Matrix X
- **Prefix**: `f_`
- **Alignment**: right-aligned rolling windows
- **No Leakage**: features use only past data
- **NaN Policy**: drop after warmup
- **Minimal Columns**:
  - f_ret_1
  - f_ret_3
  - f_ret_12
  - f_hl_range
  - f_oc_range
  - f_vol_z

## Label y (R(Return_H))
- **Definition**: forward return over H bars
- **Policy**: last H rows dropped downstream

## Enforcement by builder
- Right-aligned windows for all features
- Warmup drop: first max(window, H) rows
- Trailing label NaNs dropped
- Columns: f_* + label
- UTC timezone-aware index
- Enforced by: scripts/training/build_dataset.py

### Example CLI
```
python scripts/training/build_dataset.py \
  --ohlcv docs/REPORTS/RAW/OHLCV_SAMPLE.csv \
  --timeframe 5m \
  --H 12 \
  --transform pct \
  --windows 1,3,12 \
  --out data/dataset_SAMPLE.parquet
```

## Example Table (Synthetic)
| datetime            | open   | high   | low    | close  | volume  | f_ret_1 | f_ret_3 | f_ret_12 | f_hl_range | f_oc_range | f_vol_z | label_R_H12 |
|---------------------|--------|--------|--------|--------|---------|---------|---------|----------|------------|------------|---------|-------------|
| 2025-09-19 08:00:00 | 100.00 | 101.00 | 99.50  | 100.50 | 1200.0  | 0.005   | 0.012   | 0.045    | 0.015      | 0.005      | 0.2     | 0.010       |
| 2025-09-19 08:05:00 | 100.50 | 101.20 | 100.00 | 101.00 | 1300.0  | 0.004   | 0.010   | 0.043    | 0.012      | 0.005      | 0.3     | 0.011       |
| 2025-09-19 08:10:00 | 101.00 | 101.50 | 100.80 | 101.20 | 1250.0  | 0.002   | 0.008   | 0.040    | 0.007      | 0.002      | 0.1     | 0.009       |
| 2025-09-19 08:15:00 | 101.20 | 101.60 | 100.90 | 101.10 | 1280.0  | -0.001  | 0.006   | 0.038    | 0.007      | -0.001     | 0.0     | 0.008       |
| 2025-09-19 08:20:00 | 101.10 | 101.40 | 100.70 | 101.00 | 1270.0  | -0.002  | 0.004   | 0.035    | 0.007      | -0.002     | -0.1    | 0.007       |
| 2025-09-19 08:25:00 | 101.00 | 101.30 | 100.60 | 100.80 | 1260.0  | -0.002  | 0.003   | 0.033    | 0.007      | -0.002     | -0.2    | 0.006       |
| 2025-09-19 08:30:00 | 100.80 | 101.10 | 100.50 | 100.70 | 1255.0  | -0.001  | 0.002   | 0.030    | 0.006      | -0.001     | -0.3    | 0.005       |
| 2025-09-19 08:35:00 | 100.70 | 101.00 | 100.40 | 100.60 | 1250.0  | -0.001  | 0.001   | 0.028    | 0.006      | -0.001     | -0.4    | 0.004       |
