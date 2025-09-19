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
