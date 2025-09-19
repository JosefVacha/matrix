## Offline mapping & simulator metrics

Synthetic simulator (`simulate_thresholds.py`) produces:
- Trigger Rate
- Long/Short split
- Churn proxy (entries exiting < cooldown)
- Avg hold bars
- ASCII sparkline of predictions

# METRICS_CHECKLIST.md

Essential metrics collection for MATRIX sandbox backtesting.

<!-- Existing content -->

## Metrics Summary & Threshold Diff Workflow

After each sandbox run, fill out `docs/REPORT_TEMPLATE.md`.
Markers (machine-readable):
  - `<!-- RUN_META: ... -->`, `<!-- SIGNALS: ... -->`, `<!-- PERF_PROXY: ... -->`, `<!-- LATENCY: ... -->`, etc.
Use `scripts/metrics/extract_metrics.py` to parse markers and generate a compact summary in `docs/summaries/` using [METRICS_SUMMARY_TEMPLATE.md](../METRICS_SUMMARY_TEMPLATE.md).
For threshold changes, use `scripts/thresholds/diff_thresholds.py` and [DIFF_REPORT_TEMPLATE.md](../DIFF_REPORT_TEMPLATE.md) to document differences and stability impact.

Essential metrics collection for MATRIX sandbox backtesting.

## Purpose
Define minimal, focused metrics that provide actionable insights during offline sandbox development.
Priority: data quality → signal behavior → performance → advanced analytics.

## Metrics Hierarchy

### 1. Data Quality (CRITICAL - always collect)
- **Missing Data %**: NaN percentage in OHLCV and features
- **Feature Coverage**: % of prediction periods with complete features
- **OHLCV Gaps**: Count of missing candles in timeframe sequence
- **Volume Anomalies**: Count of zero/extreme volume periods
- **Price Jumps**: Count of gaps > X% between consecutive candles

**Rationale**: Poor data → invalid backtests. Must validate before any signal analysis.

### 2. Signal Behavior (HIGH - core threshold tuning)
- **Signal Trigger Rate**: % of periods generating enter signals (long/short separately)
- **Signal Persistence**: Average holding period after signal trigger
- **Signal Oscillation**: Count of rapid enter→exit→enter sequences (< N bars)
- **Threshold Effectiveness**: % of signals that hit profit targets vs stops
- **Neutral Time**: % of periods in no-signal zone (between thresholds)

**Rationale**: Threshold optimization depends on signal frequency and stability patterns.

### 3. Basic Performance (MEDIUM - validate strategy viability)
- **Total Return**: Portfolio return vs buy-and-hold benchmark
- **Sharpe Ratio**: Risk-adjusted return measure
- **Max Drawdown**: Worst peak-to-trough loss
- **Win Rate**: % of profitable trades
- **Profit Factor**: Gross profit / gross loss ratio

**Rationale**: Essential performance validation, but secondary to signal quality in sandbox phase.

### 4. Risk Metrics (MEDIUM - guard rails)
- **VaR 95%**: Value at Risk (95th percentile daily loss)
- **Consecutive Losses**: Maximum streak of losing trades
- **Position Concentration**: Max % of portfolio in single trade
- **Leverage Usage**: Peak leverage reached during backtest
- **Exposure Time**: % of time with open positions

**Rationale**: Risk validation before live deployment, but not critical during threshold development.

### 5. Advanced Analytics (LOW - post-sandbox)
- **Information Ratio**: Alpha vs benchmark volatility
- **Calmar Ratio**: Return / max drawdown
- **Sortino Ratio**: Return / downside deviation
- **Kelly Criterion**: Optimal position sizing estimate
- **Feature Importance**: Which features drive best predictions

**Rationale**: Useful for optimization, but avoid over-fitting during initial development.

## Implementation Priority

### Phase 1: Essential (implement first)
```
Data Quality + Signal Behavior metrics only
- Missing data validation
- Signal trigger rates
- Basic threshold effectiveness
```

### Phase 2: Validation (add after thresholds working)
```
Basic Performance metrics
- Total return vs benchmark
- Sharpe ratio
- Max drawdown
```

### Phase 3: Risk (pre-deployment)
```
Risk Metrics for safety validation
- VaR calculation
- Drawdown analysis
- Exposure limits
```

### Phase 4: Optimization (post-sandbox)
```
Advanced Analytics for fine-tuning
- Information ratios
- Feature analysis
- Kelly sizing
```

## Collection Points

### During Backtest
- Real-time: Signal trigger counts, data quality flags
- Per-trade: Entry/exit prices, holding periods, PnL
- Daily: Portfolio value, drawdown tracking, exposure

### Post-Backtest
- Aggregate: Win rates, Sharpe calculation, threshold analysis
- Report: Summary statistics for SANDBOX_BT.md template
- Export: CSV metrics for WFO comparison across blocks

## Output Format

### Console Summary (during BT)
```
MATRIX Sandbox Metrics:
Data Quality: ✅ 98.5% coverage, 3 gaps detected
Signals: Long 12.3%, Short 8.7%, Neutral 79.0%
Performance: +15.2% vs +8.1% benchmark
Risk: -12.4% max DD, 1.45 Sharpe
```

### JSON Export (for WFO aggregation)
```json
{
  "backtest_id": "BTC_USDT_20241201_20241231",
  "data_quality": {
    "missing_data_pct": 1.5,
    "feature_coverage_pct": 98.5,
    "ohlcv_gaps": 3
  },
  "signals": {
    "long_trigger_rate": 12.3,
    "short_trigger_rate": 8.7,
    "avg_holding_period": 24.5
  },
  "performance": {
    "total_return": 15.2,
    "benchmark_return": 8.1,
    "sharpe_ratio": 1.45,
    "max_drawdown": -12.4
  }
}
```

## Integration Points

### With SANDBOX_BT.md
- Metrics feed into backtest report template
- WFO blocks aggregate metrics for comparison
- Threshold stability analysis uses signal behavior metrics

### With THRESHOLDS.md
- Grid sweep evaluates metrics across threshold ranges
- WFO evaluation ranks thresholds by composite metric score
- Stability check monitors metric consistency across blocks

### With telemetry/metrics.py
- Implement metrics buckets following this checklist
- Real-time collection during sandbox backtests
- Export functions for WFO aggregation

## Usage

1. **Start Simple**: Implement Phase 1 (Data Quality + Signal Behavior) first
2. **Validate**: Use metrics to debug threshold issues before adding complexity
3. **Iterate**: Add Phase 2-4 metrics only after core signal logic is stable
4. **Aggregate**: Use JSON export for WFO comparison across multiple backtest blocks

**Note**: Resist metric proliferation. More metrics ≠ better insights. Focus on actionable feedback that improves threshold selection and signal quality.
