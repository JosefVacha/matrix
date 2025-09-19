# Label R(Return_H) Semantics

Formula:
- Percent return: $R_{t,H}^{pct} = \frac{close_{t+H}}{close_t} - 1$
- Log return: $R_{t,H}^{log} = \log\left(\frac{close_{t+H}}{close_t}\right)$

Alignment:
- Label for time $t$ uses close at $t$ and $t+H$ (lookahead)
- Last $H$ rows become NaN and are dropped downstream
# MATRIX Label Generation Semantics

This document defines the semantics and methodology for label generation in MATRIX.
The `generate_labels()` function in `src/matrix/freqai/hooks.py` is the single source of truth for all label generation logic.

## Label Types and Modes

### Mode: 'R' (Return-based Labels)
**Default mode** - generates return-based labels using forward-looking horizon.

```python
# Example: 24-candle forward return
label = (close[t+24] - close[t]) / close[t]
```

**Parameters:**
- `horizon`: Number of candles to look ahead (default: 24)
- `method`: Calculation method ('simple', 'log', 'normalize')

**Use Cases:**
- Regression models predicting price movement magnitude
- Continuous target variable for supervised learning
- Risk-adjusted return predictions

### Mode: 'C' (Classification Labels)
**Discrete classification** - converts returns into categorical bins.

```python
# Example: 3-class classification (down, neutral, up)
if return > threshold_high:
    label = 2  # Up
elif return < threshold_low:
    label = 0  # Down
else:
    label = 1  # Neutral
```

**Parameters:**
- `threshold_high`: Upper threshold for "up" class
- `threshold_low`: Lower threshold for "down" class
- `num_classes`: Number of classification bins

### Mode: 'V' (Volatility Labels)
**Volatility prediction** - labels based on future price volatility.

```python
# Example: realized volatility over horizon
volatility = std(returns[t:t+horizon]) * sqrt(horizon)
```

**Parameters:**
- `horizon`: Period for volatility calculation
- `annualize`: Whether to annualize volatility

## Temporal Integrity Requirements

### Lookahead Methodology
- **CRITICAL:** Labels use ONLY future information relative to their timestamp
- Label for time `t` calculated from `t+1` to `t+horizon`
- No information from time `t` included in label calculation

### Walk-Forward Compliance
- Labels respect train/test split boundaries
- No future information leaks into training period
- Validation during WFO (Walk-Forward Optimization)

### Edge Case Handling
- End-of-dataset: Labels set to NaN when insufficient future data
- Market gaps: Handle missing data in lookahead window
- Holiday/weekend adjustments for different assets

## Implementation Notes

### Index Alignment
```python
# Labels MUST have same index as input OHLCV
assert labels.index.equals(df_ohlcv.index)
```

### Label Naming Convention
- Return labels: `"return_{horizon}c"` (e.g., "return_24c")
- Classification labels: `"class_{horizon}c_{num_classes}way"`
- Volatility labels: `"vol_{horizon}c"`

### Quality Assurance
- Label distribution validation (avoid extreme skew)
- NaN ratio monitoring (expected at dataset end)
- Temporal consistency checks

## Configuration Examples

### Short-term Returns (5m timeframe)
```python
generate_labels(df, mode='R', horizon=12, method='simple')  # 1-hour ahead
```

### Medium-term Classification (1h timeframe)
```python
generate_labels(df, mode='C', horizon=24, threshold_high=0.02, threshold_low=-0.02)  # 1-day ahead
```

### Volatility Prediction
```python
generate_labels(df, mode='V', horizon=48, annualize=True)  # 2-day volatility
```

## Validation and Testing

### Unit Tests
- Label calculation correctness
- Index alignment verification
- Temporal integrity validation
- Edge case handling

### Walk-Forward Tests
- No leakage in train/test splits
- Consistent label generation across periods
- Performance tracking over time

## Performance Considerations

### Computation Efficiency
- Vectorized operations preferred over loops
- Caching for repeated calculations
- Memory-efficient rolling window operations

### Quality Metrics
- Label distribution stability over time
- Predictability assessment (baseline models)
- Correlation with market regime changes

---

**Note:** This document should be updated whenever label generation logic changes in `src/matrix/freqai/hooks.py`.
