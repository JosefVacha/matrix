# MATRIX Training Protocol (Offline, Docs-First)

## Data Scope
- Timeframe: 5m
- Pairlist: static (see configs/pairlist.static.json)
- Candles: local only

## Splits: Walk-Forward
| train_from | train_to | test_from | test_to |
|------------|----------|-----------|---------|
| <PH>       | <PH>     | <PH>      | <PH>    |
| <PH>       | <PH>     | <PH>      | <PH>    |
| <PH>       | <PH>     | <PH>      | <PH>    |

## Model Candidates & Params Grid (Placeholders)
- Linear (ridge-like): param alpha
- Tree (depth-limited): param max_depth, min_samples
- Mean-Reversion Benchmark: rule-based, no params

## Params Grid Example
| model_type | param_1      | param_2      |
|------------|-------------|--------------|
| linear     | alpha=0.1    | alpha=1.0    |
| tree       | max_depth=3  | min_samples=10 |
| meanrev    | n/a          | n/a          |

## Pipeline
OHLCV → features (same for train/test) → label R(Return_H) → model

### Dataset builder CLI
```
python scripts/training/build_dataset.py \
  --ohlcv docs/REPORTS/RAW/OHLCV_SAMPLE.csv \
  --timeframe 5m \
  --H 12 \
  --transform pct \
  --windows 1,3,12 \
  --out data/dataset_SAMPLE.parquet
```
Builder enforces DATASET_SCHEMA.md and writes a sidecar JSON with shape + parameters.

## Training Runner CLI

Minimal offline training runner for baseline models (linear, ridge, OLS).

### Usage
```bash
python scripts/training/train_baseline.py \
  --dataset data/dataset_SMOKE.parquet \
  --label-name label_R_H3_pct \
  --features "f_ret_1,f_ret_3,f_vol_12" \
  --train-from 2025-01-01 --train-to 2025-01-08 \
  --model-tag M3_SMOKE_RH3 \
  --out-json docs/summaries/TRAIN_SUMMARY_SMOKE.json \
  --save-model models/M3_SMOKE_RH3/model.pkl
```

### Output: Train Summary JSON
Minimal schema:
```json
{
  "run_tag": "<model-tag>",
  "label": "label_R_H3_pct",
  "features": ["f_ret_1","f_ret_3","f_vol_12"],
  "train": {"from":"YYYY-MM-DD","to":"YYYY-MM-DD","n":123},
  "model": {"type":"ridge","alpha":0.1},
  "metrics": {"mae":..., "mse":..., "r2":..., "resid_mean":..., "resid_std":...},
  "created_at": "ISO-8601"
}
```

### Registry Metadata
See MODEL_REGISTRY.md for schema and example.

## Reproducibility
- Record commit hashes: CONTRACTS, LABELS, HOOKS
- TS set name
- Pairlist ref
- Timeframe

## Outputs
- Model artifact + metadata.json (see MODEL_REGISTRY.md)

## Guardrails
- No feature changes between train/test
- Label lookahead H
- Right-aligned windows
- Drop warmup rows
- No leakage via label/feature windows
