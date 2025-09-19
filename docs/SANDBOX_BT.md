# MATRIX Sandbox Backtest Plan

This document defines the **OFFLINE-ONLY** sandbox backtest protocol for MATRIX strategy development. No live trading, no data downloads, no API keys.

## Scope and Constraints

### Timeframe and Assets
- **Primary timeframe**: 5m (5-minute candles)
- **Asset selection**: Static pairlist from `configs/pairlist.static.json`
- **No dynamic pairlist changes** during backtest runs
- **Period**: Fixed placeholder range `<FROM_YYYY-MM-DD>` to `<TO_YYYY-MM-DD>`

### Data Source Requirements
- **Local candles only** - assume data already present in local storage
- **No network access** during backtest execution
- **No real-time feeds** or exchange connections
- Data format: Standard Freqtrade OHLCV format with datetime index

### Safety Guardrails
- **Configuration**: Use `configs/backtest.sandbox.example.json` template
- **Output location**: Local files only, no external uploads
- **Reproducibility**: Static pairlist ensures consistent asset selection
- **Isolation**: Completely offline environment

## Backtest Protocol

### Walk-Forward Optimization Blocks
1. **Training Period**: Minimum 30 days per block (configurable)
2. **Test Period**: 7 days per block (configurable)
3. **Progression**: Chronological, no overlapping periods
4. **Gap**: Optional gap between train/test periods
5. **Feature Pipeline**: Identical for training and testing phases

### Model Training Workflow
```
For each WFO block:
1. Extract training period OHLCV
2. Generate features using hooks (no leakage)
3. Generate labels using lookahead methodology
4. Train model on features/labels
5. Save model artifacts with metadata
6. Proceed to test period
```

### Testing Workflow
```
For each test period:
1. Load model artifacts from training
2. Generate features for test period
3. Generate predictions using trained model
4. Convert predictions to signals using thresholds
5. Record signal statistics and performance metrics
6. Log latency and data quality metrics
```

### Version Control
- **Contract Tracking**: Record commit hash of `docs/CONTRACTS.md` and `docs/LABELS.md`
- **Hook Versions**: Track versions of feature/label generation functions
- **Configuration**: Include full config snapshot in run metadata
- **Reproducibility**: Same commit + same config = same results

## Output Report Template

### Run Metadata
```
Backtest Run Report
==================
Date: YYYY-MM-DD HH:MM:SS
Commit Hash: <git_commit_hash>
Contracts Version: <contracts_md5>
Labels Version: <labels_md5>
Config File: backtest.sandbox.json
```

### Data Coverage Summary
```
Data Coverage
=============
Period: <FROM_YYYY-MM-DD> to <TO_YYYY-MM-DD>
Timeframe: 5m
Assets: <N> pairs from static pairlist
Total Candles: <N>
Missing Data: <N> gaps (list major gaps)
Quality Score: <percentage>
```

### Walk-Forward Block Summary
```
WFO Blocks
==========
Total Blocks: <N>
Training Period: <N> days each
Test Period: <N> days each
Block Success: <N>/<N> completed successfully
Failed Blocks: <list_if_any>

Block Details:
- Block 1: Train 2024-01-01 to 2024-01-30, Test 2024-01-31 to 2024-02-07
- Block 2: Train 2024-01-08 to 2024-02-06, Test 2024-02-07 to 2024-02-14
- [etc...]
```

### Signals Summary
```
Signal Generation
================
Total Signals: <N>
- Long Entry: <N> (<percentage>)
- Long Exit: <N> (<percentage>)
- Short Entry: <N> (<percentage>)
- Short Exit: <N> (<percentage>)

Signal Rate: <signals_per_day> per day
Hold Time: Average <N> candles, Median <N> candles
Long/Short Ratio: <ratio>
```

### Performance Metrics (Offline Proxy)
```
Performance Summary
==================
Total Trades: <N>
Win Rate: <percentage>
Average Trade Return: <percentage>
Best Trade: <percentage>
Worst Trade: <percentage>
Max Drawdown: <percentage>
Exposure: <percentage> of time in market
```

### System Performance
```
Latency Notes
=============
Avg Inference Time: <N>ms per bar
Max Inference Time: <N>ms per bar
Feature Generation: <N>ms per bar
Total Pipeline: <N>ms per bar
Target: <1000ms for 5m timeframe (guidance)
```

### Data Quality Metrics
```
Data Quality
============
NaN Ratio After Features: <percentage>
Feature Drift: <metric_if_available>
Label Distribution: Mean <N>, Std <N>, Skew <N>
Outliers Detected: <N> (<percentage>)
```

### Recommendations
```
Next Steps
==========
1. [Automated suggestions based on results]
2. [Threshold adjustment recommendations]
3. [Data quality improvements needed]
4. [Model performance notes]
5. [Configuration adjustments]
```

## Usage Instructions

### Prerequisites
1. Local OHLCV data available in Freqtrade format
2. MATRIX hooks implemented (feature/label generation)
3. Baseline model selected and configured
4. Static pairlist configured in `configs/pairlist.static.json`

### Execution Steps
1. Copy `configs/backtest.sandbox.example.json` to `configs/backtest.sandbox.json`
2. Edit `backtest.sandbox.json` with specific date ranges and parameters
3. Ensure all dependencies installed and environment configured
4. Run backtest using configured parameters
5. Review generated report and metrics
6. Iterate on thresholds and configuration as needed

### Important Notes
- **Never commit `backtest.sandbox.json`** (should be gitignored)
- **Always use static pairlist** for reproducibility
- **Keep detailed logs** of all configuration changes
- **Document any manual interventions** or modifications
- **Validate results** against expected behavior patterns

---

**Remember**: This is a sandbox environment for strategy development only. No live trading, no real money at risk.