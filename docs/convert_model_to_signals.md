# Convert a trained model to simulator signals

This document explains how to export predictions from a trained model (FreqAI or other) and prepare them for the simulator in this repo. The goal is a small, deterministic bridge: given a time-indexed smoke dataset and a matching prediction vector, the simulator will consume the predictions to produce reproducible paper-trade runs.

Contract (predictions file)
- Format: CSV or Parquet with columns: `date`,`pair`,`prediction`
  - `date` must match the timezone-aware index used in `data/dataset_SMOKE.parquet` (ISO 8601). If your model produces predictions aligned to candle start, keep the same convention.
  - `pair` must be the trading pair string used in the smoke dataset (e.g., `BTC/USDT`).
  - `prediction` is a numeric value (float). Positive values indicate bullish signal strength, negative values indicate bearish signal strength. The simulator adapter maps this numeric value into buy/sell actions using the adapter rules.

Alignment and lookahead
- Ensure predictions are aligned without future leakage. If your label uses a lookahead (e.g., target = close price after N candles), the exported prediction must be shifted so that it corresponds to the candle where the signal would be available in production.
- Walk-forward training and test splits should be used for evaluation. Never export predictions that used future data for the same timestamp.

Example: export from a FreqAI model
1. Use the repository helper to export predictions aligned to the smoke dataset index:

```
python3 scripts/training/export_for_simulator.py \
  --model-path models/MY_MODEL --dataset data/dataset_SMOKE.parquet \
  --output outputs/predictions_for_sim.csv
```

2. Check schema (simple validation):

```
python3 -c "import pandas as pd; df=pd.read_csv('outputs/predictions_for_sim.csv'); print(df.head()); print(df.isnull().sum())"
```

Adapter expectations
- The adapter expects a numeric `prediction` column and applies hysteresis + cooldown logic to reduce flip-flopping. See `src/matrix/strategy/mapping.py` for the mapping rules.
- To reproduce the same results in CI, keep randomness disabled in feature pipelines and in any stochastic model components (seed RNGs if necessary).

Troubleshooting
- If the simulator reports missing dates or mismatched lengths, verify `date` timezone and that `pair` values exactly match the smoke dataset's pairlist.
- If the produced signals appear too noisy, consider smoothing predictions (moving average) before export or adjust adapter thresholds.

Notes
- This repo intentionally provides a small offline simulator to produce stable, reproducible smoke runs suitable for CI. For full backtesting, retraining and live-model serving use the official Freqtrade/FreqAI tooling.
---
title: Convert a trained FreqAI model to simulator signals
---

This short how-to shows safe, offline ways to convert a trained model into a predictions file suitable for the paper-trading simulator (`predictions.csv`). The goal is a deterministic, index-aligned CSV that the simulator can consume.

Paths supported:
- Use a saved model artifact (pickle / sklearn / torch / tf saved format) and a small wrapper to produce predictions for the smoke dataset index.
- Use a precomputed `predictions.csv` produced by your training or evaluation pipeline and reindex it to the smoke dataset.

Minimal requirements for `predictions.csv`:
- Columns: `datetime` (ISO8601) and `prediction` (float). `datetime` must match the index granularity of `data/dataset_SMOKE.parquet`.
- No future leakage: predictions must be generated using only historical features available at each timestamp.

Example 1 — From a saved sklearn-like pickle (offline)

1. Prepare the smoke dataset index:

   - Load `data/dataset_SMOKE.parquet` and extract the index or datetime column your simulator expects.

2. Load your trained model artifact locally (no keys, no network):

   - Use `joblib.load('models/my_model.pkl')` or similar.

3. Generate features for each index row using the same feature-engineering code used at training time.

4. Call `model.predict_proba(X)[:, 1]` or `model.predict(X)` depending on your model output. Save to `predictions.csv` with columns `datetime,prediction`.

Example 2 — Reindex a precomputed predictions CSV

1. If you already have `predictions_raw.csv` (datetime,prediction) from training/validation runs, reindex it to the smoke dataset:

   - Load `predictions_raw.csv` and `data/dataset_SMOKE.parquet`.
   - Merge or reindex the predictions to the smoke dataset timestamps; fill missing predictions with a safe default (e.g., 0.0).

2. Output `predictions.csv` with the canonical index and `prediction` column.

Security & reproducibility notes
- Do not include any secrets or remote keys in these scripts. All operations must be local.
- Record the model version, feature code commit hash, and the smoke-dataset checksum in the run log so results are reproducible.

Next steps
- Use `scripts/training/export_for_simulator.py --help` for an example CLI that implements these patterns.
