# Example failure case (missing marker):
# Remove or comment out <!-- PRED_DIST: ... --> to simulate missing marker.
# Validator output: [FAIL] Missing markers: PRED_DIST
# MATRIX Sandbox Backtest Report

**Report for Sample Run**

---

## Run Metadata
<!-- RUN_META: commit=abc123; timeframe=5m; timerange=2025-09-01 to 2025-09-07; pairlist_ref=pairlist.static.json -->

### Execution Details
- **Run Date**: 2025-09-19
- **Run Duration**: 1h
- **Executed By**: tester
- **Environment**: FreqTrade 2025.9, Python 3.10, Linux

### Version Control
- **MATRIX Commit Hash**: abc123
- **FreqTrade Version**: 2025.9
- **Configuration Files**:
  - `backtest.sandbox.json` checksum: 123456
  - `pairlist.static.json` checksum: 654321
  - `MatrixStrategy.py` last modified: 2025-09-18

### Backtest Configuration
- **Exchange**: binance
- **Timeframe**: 5m
- **Time Range**: 2025-09-01 to 2025-09-07
- **Pairs Tested**: BTC/USDT, ETH/USDT
- **Total Candles**: 2016

---

## Signals Summary
<!-- SIGNALS: trigger_rate=0.12; long_rate=0.08; short_rate=0.04; hold_time_median=15 -->

### Signal Behavior
- **Long Entry Trigger Rate**: 8%
- **Short Entry Trigger Rate**: 4%
- **Neutral Time**: 88%
- **Average Holding Period**: 15 bars
- **Signal Oscillations**: 2

---

## Performance Overview
<!-- PERF_PROXY: avg_trade_ret=0.7; win_rate=0.55; exposure=0.32; max_dd=0.09 -->

### Basic Performance Metrics
- **Total Return**: 7%
- **Buy & Hold Benchmark**: 5%
- **Sharpe Ratio**: 1.2
- **Maximum Drawdown**: 9%
- **Win Rate**: 55%
- **Profit Factor**: 1.8

---

## Latency and Performance Notes
<!-- LATENCY: inference_ms_p50=800; p90=1200 -->

### Pipeline Performance
- **Feature Generation**: 50 ms
- **Model Inference**: 800 ms
- **Signal Generation**: 20 ms
- **Total Latency**: 870 ms
