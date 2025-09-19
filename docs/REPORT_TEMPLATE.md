# MATRIX Sandbox Backtest Report

**Report for First Offline Sandbox Run**

*Fill this template after completing your first MATRIX sandbox backtest.*

---

## Run Metadata
<!-- RUN_META: commit=<hash>; timeframe=5m; timerange=<from-to>; pairlist_ref=<file> -->

### Execution Details
- **Run Date**: ________________
- **Run Duration**: ________________ (start time → end time)
- **Executed By**: ________________
- **Environment**: ________________ (FreqTrade version, Python version, OS)

### Version Control
- **MATRIX Commit Hash**: ________________
- **FreqTrade Version**: ________________  
- **Configuration Files**:
  - `backtest.sandbox.json` checksum: ________________
  - `pairlist.static.json` checksum: ________________
  - `MatrixStrategy.py` last modified: ________________

### Backtest Configuration
- **Exchange**: ________________ (e.g., binance)
- **Timeframe**: ________________ (e.g., 5m)
- **Time Range**: ________________ (e.g., 2024-12-01 to 2024-12-07)
- **Pairs Tested**: ________________ (e.g., BTC/USDT, ETH/USDT)
- **Total Candles**: ________________ (across all pairs)

---

## Data Coverage Assessment

### Data Quality Summary
- **Missing Data Percentage**: ______% (NaN/gaps in OHLCV)
- **Feature Coverage**: ______% (periods with complete features)
- **OHLCV Gaps Detected**: ______ missing candles
- **Volume Anomalies**: ______ zero/extreme volume periods
- **Price Jumps**: ______ gaps >X% between consecutive candles

### Pair-by-Pair Coverage
| Pair | Total Candles | Missing | Coverage % | Notes |
|------|---------------|---------|------------|-------|
| BTC/USDT | ______ | ______ | ______% | ________________ |
| ETH/USDT | ______ | ______ | ______% | ________________ |
| ______ | ______ | ______ | ______% | ________________ |

### Data Quality Issues
- **Critical Issues**: ________________
- **Minor Warnings**: ________________
- **Recommendations**: ________________

---

## Signals Summary
<!-- SIGNALS: trigger_rate=...; long_rate=...; short_rate=...; hold_time_median=...; entries=...; exits_lt_cooldown=... -->

### Signal Behavior
- **Long Entry Trigger Rate**: ______% (percentage of periods with long signals)
- **Short Entry Trigger Rate**: ______% (percentage of periods with short signals)  
- **Neutral Time**: ______% (periods with no signals)
- **Average Holding Period**: ______ bars (average time between entry and exit)
- **Signal Oscillations**: ______ rapid enter→exit→enter sequences detected

### Threshold Effectiveness (Placeholder Values)
- **UP_THRESHOLD Used**: ______ (from MatrixStrategy placeholder)
- **DOWN_THRESHOLD Used**: ______ (from MatrixStrategy placeholder)
- **HYSTERESIS Buffer**: ______ (oscillation prevention)
- **COOLDOWN Period**: ______ bars (minimum between signal changes)

### Signal Distribution
| Signal Type | Count | Percentage | Average Duration |
|-------------|-------|------------|------------------|
| Long Entry | ______ | ______% | ______ bars |
| Long Exit | ______ | ______% | ______ bars |
| Short Entry | ______ | ______% | ______ bars |
| Short Exit | ______ | ______% | ______ bars |

---

## Performance Overview
<!-- PERF_PROXY: avg_trade_ret=...; win_rate=...; exposure=...; max_dd=... -->

### Basic Performance Metrics
- **Total Return**: ______% (portfolio return over period)
- **Buy & Hold Benchmark**: ______% (comparison baseline)
- **Sharpe Ratio**: ______ (risk-adjusted return)
- **Maximum Drawdown**: ______% (worst peak-to-trough loss)
- **Win Rate**: ______% (percentage of profitable trades)
- **Profit Factor**: ______ (gross profit / gross loss)

### Trade Statistics
- **Total Trades**: ______ (number of completed round trips)
- **Winning Trades**: ______ (count and percentage)
- **Losing Trades**: ______ (count and percentage)
- **Average Trade Duration**: ______ bars
- **Best Trade**: ______% return
- **Worst Trade**: ______% return

### Risk Metrics (if available)
- **VaR 95%**: ______% (Value at Risk, 95th percentile daily loss)
- **Consecutive Losses**: ______ (maximum losing streak)
- **Position Concentration**: ______% (max portfolio % in single trade)
- **Exposure Time**: ______% (time with open positions)

---

## Latency and Performance Notes
<!-- LATENCY: inference_ms_p50=...; p90=... -->

### Pipeline Performance
<!-- WFO: blocks=[(train_from,train_to,test_from,test_to), ...] -->
- **Feature Generation**: ______ ms average per bar
- **Model Inference**: ______ ms average per prediction  
- **Signal Generation**: ______ ms average per bar
- **Total Latency**: ______ ms per bar (target: ~1000ms for 5m timeframe)

### Bottlenecks Identified
- **Slowest Component**: ________________
- **Performance Issues**: ________________
- **Optimization Opportunities**: ________________

---

## WFO Blocks Analysis

### Walk-Forward Setup (if applicable)
- **WFO Blocks Executed**: ______ (number of train/test splits)
- **Training Period Length**: ______ days per block
- **Testing Period Length**: ______ days per block
- **Overlap/Gap**: ______ days between blocks

### WFO Results Summary
| Block | Train Period | Test Period | Thresholds Used | Performance | Notes |
|-------|--------------|-------------|-----------------|-------------|-------|
| 1 | ______ | ______ | UP:______ DN:______ | ______% | ________________ |
| 2 | ______ | ______ | UP:______ DN:______ | ______% | ________________ |
| 3 | ______ | ______ | UP:______ DN:______ | ______% | ________________ |

### Stability Assessment
- **Threshold Consistency**: ________________
- **Performance Variance**: ________________
- **Best Stable Thresholds**: UP:______ DN:______ HYST:______

---

## Issues and Observations

### Technical Issues Encountered
1. **Data Issues**: ________________
2. **Configuration Problems**: ________________
3. **Pipeline Failures**: ________________
4. **Performance Bottlenecks**: ________________

### Unexpected Behaviors
1. **Signal Patterns**: ________________
2. **Performance Anomalies**: ________________
3. **Data Quality Surprises**: ________________

### Validation Concerns
1. **Contract Violations**: ________________
2. **Assumption Violations**: ________________
3. **Methodology Questions**: ________________

---

## Lessons Learned

### What Worked Well
- ________________
- ________________
- ________________

### What Needs Improvement
- ________________
- ________________
- ________________

### Surprising Discoveries
- ________________
- ________________
- ________________

---

## Decisions and Next Steps

### Immediate Actions Required
1. **Data Quality**: ________________
2. **Configuration Adjustments**: ________________
3. **Threshold Refinements**: ________________
4. **Pipeline Fixes**: ________________

### Threshold Optimization Plan
- **Grid Sweep Ranges**: UP [______:______], DN [______:______]
- **Hysteresis Testing**: [______:______]
- **Cooldown Optimization**: [______:______] bars
- **WFO Validation**: ______ blocks planned

### Metrics Implementation Priority
- **Phase 1 (Essential)**: ________________
- **Phase 2 (Validation)**: ________________
- **Phase 3 (Risk)**: ________________

### Long-term Improvements
1. **Feature Engineering**: ________________
2. **Model Selection**: ________________
3. **Risk Management**: ________________
4. **Performance Optimization**: ________________

---

## Appendix

### Configuration Snapshots
```json
// Key config sections used in this run
{
  "timerange": "________________",
  "timeframe": "________________", 
  "pairlist": [________________],
  "strategy": "MatrixStrategy",
  "// thresholds": "placeholder values - see strategy file"
}
```

### Command History
```bash
# Commands used for this backtest run
freqtrade backtesting --config configs/backtest.sandbox.json --strategy MatrixStrategy [...]
```

### Output Samples
```
// Paste key sections of backtest output here
[BACKTEST OUTPUT SAMPLE]
```

### Files Generated
- **Backtest results**: ________________
- **Log files**: ________________
- **Metrics exports**: ________________
- **Charts/plots**: ________________

---

**Report Completed**: ________________ (date)  
**Review Status**: [ ] Draft [ ] Reviewed [ ] Final  
**Next Review Date**: ________________

---

## Follow-up Actions

- [ ] **Share results** with team/stakeholders
- [ ] **Update PROJECT_STATE.md** with findings
- [ ] **Plan next iteration** based on lessons learned
- [ ] **Archive run artifacts** for future reference
- [ ] **Update documentation** based on new insights

---

## Thresholds Extraction (post-run)

**Purpose**: Extract data-driven threshold proposals from sandbox backtest results using systematic analysis of prediction distributions and signal behavior patterns.

### Prediction Distribution Analysis

**Distribution Statistics** (fill from backtest output or model predictions):
- **Mean**: ______ (average prediction value)
- **Standard Deviation**: ______ (prediction volatility/spread)
- **Median**: ______ (middle value, robust to outliers)
- **Percentiles**:
  - P10: ______ (10th percentile - lower tail)
  - P25: ______ (25th percentile - lower quartile)
  - P50: ______ (50th percentile - median)
  - P75: ______ (75th percentile - upper quartile)
  - P90: ______ (90th percentile - upper tail)

**Distribution Characteristics**:
- **Skewness**: ______ (positive/negative/symmetric)
- **Range**: [______:______] (min to max predictions)
- **Typical Noise Level**: ______ (estimated from adjacent-period differences)

### Signal Trigger Rate Analysis

**Target Band Definition**:
- **Trigger Rate Target**: <PLACEHOLDER_low%>–<PLACEHOLDER_high%> (desired signal frequency)
- **Long/Short Balance Target**: <PLACEHOLDER_max_diff%> max imbalance (e.g., ±10%)
- **Neutral Time Target**: ______% (minimum time without signals)

**Current Trigger Rates** (from sandbox run):
- **Actual Long Rate**: ______% (from Signal Behavior section above)
- **Actual Short Rate**: ______% (from Signal Behavior section above)  
- **Current Imbalance**: ______% (long - short difference)
- **Assessment**: Within/Above/Below target band

### Proposed Thresholds

**Based on Distribution + Target Rates**:
- **UP_THRESHOLD**: <TBD_from_report> (for long entry signals)
- **DOWN_THRESHOLD**: <TBD_from_report> (for short entry signals)
- **HYSTERESIS**: <TBD> (buffer for exit signals)
- **COOLDOWN**: <TBD> bars (minimum between signal changes)

### Threshold Selection Rationale

**Data-Driven Justification** (3-5 bullets referencing sandbox results):
1. **UP threshold positioning**: ________________ (e.g., "Set at P75 to achieve ~25% long trigger rate within target band")
2. **DOWN threshold positioning**: ________________ (e.g., "Set at P25 to balance long/short signals within ±10% imbalance")
3. **Hysteresis sizing**: ________________ (e.g., "Set to 2x typical noise level to prevent oscillations observed in ___% of signals")
4. **Cooldown determination**: ________________ (e.g., "Set to ceil(median hold time) = ___ bars to prevent premature re-entry")
5. **Stability consideration**: ________________ (e.g., "Values stable across ___ WFO blocks with <___% variance")

### Threshold Validation Checks

**Quality Assurance**:
- [ ] **Trigger rates within band**: Long and short rates fall within target range
- [ ] **Imbalance acceptable**: Long/short difference ≤ max tolerance
- [ ] **Hysteresis sufficient**: Buffer prevents rapid oscillations
- [ ] **Cooldown reasonable**: Allows natural position development
- [ ] **Distribution alignment**: Thresholds positioned at meaningful percentiles
- [ ] **WFO consistency**: Values work across multiple time periods (if applicable)

### Implementation Notes

**Next Steps**:
1. **Review & Approve**: Have team review proposed thresholds against THRESHOLDS.md decision rules
2. **Document Decision**: Create threshold proposal PR with rationale and validation
3. **Plan Implementation**: Schedule second sandbox run with proposed values
4. **Monitor Performance**: Track effectiveness in next backtest iteration

**Assumptions & Limitations**:
- **Data period**: Thresholds based on ______ days of data (may not cover all market conditions)
- **Model stability**: Assumes prediction distribution remains relatively stable
- **Target rates**: Target trigger rates are estimates and may need adjustment
- **Market regime**: Current data may not represent all market conditions

**Future Refinements**:
- **Regime-specific thresholds**: Consider different thresholds for bull/bear/sideways markets
- **Dynamic adjustment**: Explore adaptive thresholds based on recent volatility
- **Confidence intervals**: Add prediction confidence as threshold modifier
- **Multi-timeframe**: Consider higher timeframe context for threshold adjustment

---

## Chosen Threshold Set (for second run)

- **Threshold Set File**: [TS_YYYYMMDD_TEMPLATE.yml](docs/thresholds/sets/TS_YYYYMMDD_TEMPLATE.yml) (replace with actual file for real run)
<!-- THRESHOLDS_SET: file=TS_...yml; up=...; dn=...; hysteresis=...; cooldown=... -->
- **Commit Hashes Used**:
  - Code: ________________
  - Config: ________________
  - Thresholds: ________________
- **Selection Rationale**: Reference distribution analysis and decision rules from previous report

## Stability Score (qualitative)

- **Score**: ______ / 100 (see STABILITY_SCORE.md for scoring components)
- **Notes**:
  - Trigger rate consistency: ________________
  - Long/short balance: ________________
  - Churn/flip-flop: ________________
  - Drawdown proxy: ________________
- **Reference**: See [STABILITY_SCORE.md](docs/STABILITY_SCORE.md) for scoring methodology