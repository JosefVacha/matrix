# MATRIX Sandbox Pre-Check

Pre-run validation checklist for the first offline sandbox backtest.

## Purpose
Systematic verification before running any backtest to ensure reproducible, safe execution.
**Complete ALL checkboxes before proceeding.**

## Data Validation

### Local Data Files
- [ ] **Data folder exists**: `data/` directory is present
- [ ] **Exchange folder**: `data/binance/` (or chosen exchange) exists  
- [ ] **Timeframe folder**: `data/binance/5m/` exists for primary timeframe
- [ ] **Required pairs**: All pairs from `configs/pairlist.static.json` have corresponding data files
- [ ] **File naming**: Data files follow `{PAIR}-{timeframe}.json` or `.feather` format
- [ ] **File format**: JSON arrays or valid feather files (not corrupted)

### Data Coverage Verification
- [ ] **Timerange coverage**: Local data spans entire `timerange` in backtest config
- [ ] **No gaps**: No missing candles in critical time periods
- [ ] **Volume data**: Non-zero volume in majority of candles  
- [ ] **OHLCV integrity**: All 6 columns present (timestamp, open, high, low, close, volume)
- [ ] **Timestamp order**: Data is chronologically sorted
- [ ] **Pair format**: Pairs use underscore format (`BTC_USDT`, not `BTCUSDT` or `BTC/USDT`)

## Configuration Alignment

### Static Pairlist Synchronization  
- [ ] **Pairlist file exists**: `configs/pairlist.static.json` is present
- [ ] **Pairs match data**: Every pair in pairlist has corresponding data file
- [ ] **No dynamic lists**: Configuration uses `StaticPairList` method only
- [ ] **Pair format consistency**: Pairlist format matches data file naming

### Backtest Configuration
- [ ] **Config template copied**: `configs/backtest.sandbox.example.json` copied to `backtest.sandbox.json` (gitignored)
- [ ] **Timerange set**: `timerange` parameter matches available data coverage
- [ ] **Timeframe alignment**: `timeframe` matches data folder structure  
- [ ] **No live settings**: All live trading features disabled (dry_run: true, etc.)
- [ ] **Static pairlist referenced**: Config points to `pairlist.static.json`

## MATRIX Pipeline Readiness

### Contracts and Documentation  
- [ ] **Commit hash recorded**: Current commit hash noted for reproducibility
- [ ] **CONTRACTS.md reviewed**: Pipeline contracts understood and current
- [ ] **LABELS.md reviewed**: Label generation approach confirmed
- [ ] **THRESHOLDS.md available**: Threshold methodology documented for post-run analysis

### Code State Verification
- [ ] **Strategy skeleton**: `strategies/MatrixStrategy.py` exists with placeholder thresholds
- [ ] **Core module**: `src/matrix/strategy/core.py` has threshold TODOs documented
- [ ] **Telemetry stubs**: `src/matrix/telemetry/metrics.py` has metrics collection functions
- [ ] **No live credentials**: No API keys, exchange credentials, or live trading configurations

## Metrics and Reporting Setup

### Metrics Collection Framework
- [ ] **METRICS_CHECKLIST.md reviewed**: Phase 1 (Essential) metrics identified
- [ ] **Telemetry enabled**: Metrics collection functions available (even if stubbed)
- [ ] **Console output**: Basic summary output configured for backtest feedback
- [ ] **JSON export ready**: Metrics export functions prepared for WFO aggregation

### Report Template Preparation
- [ ] **REPORT_TEMPLATE.md exists**: Report structure ready for filling
- [ ] **Report sections understood**: Know what data to collect during/after run
- [ ] **Commit tracking ready**: Plan to record commit hashes and configuration versions
- [ ] **Next steps planned**: Clear idea of what to do with backtest results

## Safety and Risk Validation

### Offline Operation Confirmation
- [ ] **No internet required**: Backtest can run completely offline
- [ ] **No API keys present**: No exchange credentials in any configuration
- [ ] **No live trading**: All trading modes set to dry-run/simulation only
- [ ] **No downloads**: No automatic data fetching configured

### Reproducibility Setup
- [ ] **Static configuration**: All randomness eliminated or seeded
- [ ] **Version control**: Current state committed to git before run
- [ ] **Environment documented**: Python/FreqTrade versions noted
- [ ] **Data snapshots**: Data files backed up or version controlled

## WFO Block Preparation

### Walk-Forward Setup (if applicable)
- [ ] **WFO_CHECKLIST.md reviewed**: Walk-forward methodology understood
- [ ] **Block boundaries planned**: Train/test split periods identified
- [ ] **Rolling window sizes**: Training and testing period lengths determined
- [ ] **Minimum data requirements**: Sufficient data for meaningful WFO analysis

### Threshold Grid Preparation  
- [ ] **THRESHOLDS.md methodology**: 3-step optimization process understood
- [ ] **Initial grid ranges**: UP_THRESHOLD and DOWN_THRESHOLD ranges planned
- [ ] **Hysteresis values**: Buffer ranges for oscillation prevention identified
- [ ] **Cooldown periods**: Signal frequency control parameters estimated

## Pre-Run Command Verification

### VS Code Tasks Ready
- [ ] **Task `data-check` available**: Can verify data placement
- [ ] **Task `precheck` available**: This checklist accessible via VS Code
- [ ] **Task `bt-sandbox-fill` available**: Config preparation workflow ready
- [ ] **Task `bt-sandbox-run` available**: Manual run instructions clear
- [ ] **Task `bt-sandbox-report` available**: Post-run reporting workflow ready

### Manual Execution Plan
- [ ] **FreqTrade CLI available**: Local FreqTrade installation ready for manual commands
- [ ] **Command structure planned**: Know exact CLI command to run for backtest
- [ ] **Output capture planned**: Know how to save and analyze backtest output
- [ ] **Error handling planned**: What to do if backtest fails or produces errors

## Final Verification

### Documentation State
- [ ] **All prerequisite docs read**: SANDBOX_BT.md, THRESHOLDS.md, METRICS_CHECKLIST.md
- [ ] **Understanding confirmed**: Clear on what the first run should achieve
- [ ] **Expectations set**: Know this is exploratory/validation run, not optimization

### Execution Readiness
- [ ] **Time allocated**: Sufficient time for run + initial analysis
- [ ] **Environment prepared**: Clean workspace, minimal distractions
- [ ] **Backup plan**: Know what to do if run fails or produces unexpected results

## Sign-Off

**Pre-Check Completed By**: ________________  
**Date**: ________________  
**Commit Hash**: ________________  
**Data Coverage**: ________________ (e.g., "BTC_USDT + ETH_USDT, 2024-12-01 to 2024-12-07, 5m")

---

## Next Steps After All Boxes Checked

1. **Run VS Code task**: `bt-sandbox-fill` (copy and customize config)
2. **Execute backtest**: Use manual FreqTrade CLI command (outside VS Code)
3. **Collect results**: Fill `docs/REPORT_TEMPLATE.md` with findings
4. **Document issues**: Note any gaps, errors, or unexpected behaviors
5. **Plan iteration**: Use results to refine thresholds, data, or methodology

**Remember**: This is a learning run. Perfect results are not expected. Focus on pipeline validation and data quality assessment.