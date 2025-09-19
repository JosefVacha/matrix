# Baseline Models (Docs-First, Offline)

This document defines conceptual baseline models for MATRIX offline training. All models are docs-first, stdlib-only, and serve as reference points for reproducibility and auditability.

## 1. Linear Model (Ridge-like, Conceptual)
- **Features**: All f_* features standardized (mean=0, std=1; concept only).
- **Penalty**: L2 regularization (conceptual placeholder, no implementation).
- **Pros**: Interpretable, fast, robust to collinearity.
- **Cons**: Sensitive to outliers, limited nonlinearity.
- **Params**: alpha (L2 penalty, placeholder).

## 2. Tree Model (Depth-Limited)
- **Type**: Decision tree, max_depth and min_samples as placeholders.
- **Pros**: Captures nonlinearity, handles missing values.
- **Cons**: Prone to overfitting, less interpretable.
- **Params**: max_depth, min_samples (placeholders).

## 3. Mean-Reversion Benchmark
- **Rule**: Predict sign of short-horizon return (e.g., R(Return_3) > 0 → long, < 0 → short).
- **Purpose**: Establishes a floor for model performance; simple, robust.

## Model Selection Rule
- Prefer model with **stable** performance across WFO blocks (see [STABILITY_SCORE.md](STABILITY_SCORE.md)).
- Inputs: X = f_* features, y = R(Return_H). No leakage; same transforms in train/test.

## Inputs/Outputs Contract
- **Inputs (X)**: f_* features, right-aligned, standardized (concept).
- **Outputs (y)**: R(Return_H), label as defined in [LABELS.md](LABELS.md).
- **No leakage**: All transforms applied identically in train/test.

## References
- [TRAINING_PROTOCOL.md](TRAINING_PROTOCOL.md)
- [LABELS.md](LABELS.md)
- [STABILITY_SCORE.md](STABILITY_SCORE.md)
