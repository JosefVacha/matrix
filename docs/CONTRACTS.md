# MATRIX I/O Contracts

Definition of mandatory inputs and outputs between MATRIX modules. All contracts are **BINDING** - violations will cause pipeline failure.

## OHLCV Contract (sensor → feature)

### MUST
- DataFrame with columns `[open, high, low, close, volume]` + datetime index
- Datetime index without gaps (continuous time series)
- All values of numeric type (float64/int64)
- **FORBIDDEN to overwrite basic OHLCV columns** - features into separate namespace

### SHOULD  
- Index sorted chronologically (oldest → newest)
- No duplicate timestamps
- Reasonable data frequency (5m, 15m, 1h, 4h, 1d)

## Features Contract (feature → model)

### MUST
- `make_features(df)` → `features_df` with **same datetime index** as input
- **No forward-fill from future** - features for time t contain no info from t+1, t+2, ...
- **Mandatory log NaN count** after feature engineering via telemetry
- Features in separate namespace (prefix `feat_`, `ta_`, etc.)

### SHOULD
- Robust scaling (median/IQR) resistant to outliers  
- Consistent feature naming across runs
- Feature documentation in metadata

## Labels Contract (feature → model)

### MUST  
- Labels with **same datetime index** as features
- **Defined by lookahead** - label for time t created from t+lookahead
- **No temporal leakage** - label t not used in features t
- Numeric type suitable for regression/classification

### SHOULD
- Documentation of lookahead period in metadata
- Handle edge cases (end of dataset)
- Label distribution validation

## FreqAI Hooks Contract (hooks → bridge)

### MUST
- `generate_features(df_ohlcv)` → DataFrame with same index as input, no leakage
- `generate_labels(df_ohlcv, mode, **kwargs)` → Series with same index, uses lookahead
- `feature_columns()` → list[str] matching generate_features() output columns
- `label_name()` → str matching generate_labels() output Series name
- All hooks preserve index alignment and prevent temporal leakage

### SHOULD
- Hooks log telemetry for NaN ratios and computation time
- Feature/label generation consistent across training and inference
- Robust error handling and validation
- See docs/LABELS.md for label semantics

## Model Artifacts Contract (train → predict)

### MUST
- Main model as `model.pkl` (pickle/joblib serializable)
- **Optionally** `metadata.json` with feature list and training interval
- Consistent structure across model types

### SHOULD
- Metadata contains: feature names, train period, model type, performance metrics
- Compatibility with FreqAI model loading
- Version tracking for model evolution

## Predict Contract (model → strategy)

### MUST
- `predict(model, features_tail)` → Series/DataFrame with prediction for last rows
- **Target speed <1s for 5m timeframe** (guidance, not hard SLA)
- Same output format as during training

### SHOULD
- Graceful handling of missing features
- Confidence intervals/uncertainty estimates
- Batch prediction for efficiency

## Strategy I/O Contract (predict → signal)

### MUST
- `to_signals(preds, context)` → DataFrame with columns `['enter_long', 'exit_long', 'enter_short', 'exit_short']`
- **Preserve original OHLCV columns** - do not overwrite
- Boolean type for signal columns
- Deterministic behavior (same inputs = same outputs)

### SHOULD
- Documentation of signal logic/thresholds
- Context contains current position/balance info
- Timestamp alignment with input data

## Risk I/O Contract (signal → execution)

### MUST
- `size_and_risk(signal, context)` → Dict `{stake, sl, tp/roi}`
- **No exchange interaction** - computation only
- Valid numeric values or None
- Respect max risk per trade

### SHOULD
- Portfolio heat calculation
- Volatility-based sizing
- Dynamic risk adjustment

## Telemetry Contracts (all modules)

### MUST
- **Log hooks** for critical metrics:
  - `log_latency_ms(stage, value)` - inference latency  
  - `log_nan_ratio(stage, value)` - % NaN after features
  - `log_feature_drift(stat)` - simple drift indicator
- Thread-safe logging
- Structured log format

### SHOULD
- Configurable log levels
- Performance impact minimization
- Monitoring dashboards integration

## Contract Validation

For each contract, tests exist in `tests/test_contracts.py` verifying:
- Correct I/O structure
- Type safety
- Temporal integrity
- Performance characteristics

**WARNING:** Contract violations = FAIL - pipeline stops with error message.