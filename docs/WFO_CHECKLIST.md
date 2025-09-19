# Walk-Forward Optimization (WFO) Checklist

Checklist for reproducible and valid walk-forward backtests. **All points must be met** before considering results valid.

## 🕒 Temporal Integrity

- [ ] **Fixed train/test time blocks without overlap** - train period never contains data from test period
- [ ] **Chronologically forward** - each next WFO step starts after the previous one (timeline: train1 → test1 → train2 → test2 → ...)
- [ ] **No dynamic pairlist changes during backtest** - identical pairlist for entire BT run
- [ ] **Consistent timeframe** - same TF for train and test (5m, 15m, 1h, etc.)

## 🔬 Feature & Label Integrity

- [ ] **Same feature pipeline for train and test** - identical transformations, scaling, feature selection
- [ ] **Label created from future relative to t, but not used in training features t** - e.g. label t created from t+24h, but features t contain only t-N to t
- [ ] **No temporal leakage in features** - features for time t do not contain information from t+1 or later
- [ ] **Consistent feature namespace** - same names and types of features across all WFO steps

## 📊 Validation & Metrics  

- [ ] **Evaluate metrics on test block** - main performance metrics from separate test periods
- [ ] **Train metrics informational only** - train accuracy/loss only for debugging, not for final evaluation
- [ ] **Log inference latency on last window** - measure predict() speed on test period (orientational)
- [ ] **Document thresholds/parameters** - record all params used for signal generation

## 🔄 Reproducibility

- [ ] **Save contract version (hash/commit) to report** - reference to exact version of CONTRACTS.md used in BT
- [ ] **Static pairlist** - use `configs/pairlist.static.json` or similar fixed list
- [ ] **Seed/random state control** - fixed random seeds for ML models (where applicable)
- [ ] **Environment snapshot** - record library/dependency versions

## 🛡️ Guardrails

- [ ] **Minimal train period** - sufficiently long train period for statistical significance (min 30 days recommended)
- [ ] **Balanced test periods** - consistent test period length across WFO steps  
- [ ] **NaN handling** - document policy for missing data and % NaN after feature engineering
- [ ] **Market regime awareness** - awareness of market conditions impact on results

## 🚫 Forbidden Practices

- [ ] **NO future data in features** - absolute ban on forward-looking bias
- [ ] **NO train-test contamination** - no "thoughts" about test period during train phase  
- [ ] **NO parameter tuning on test results** - hyperparams tuned only on train/validation, not test
- [ ] **NO selective reporting** - report all WFO steps, not just "good" ones

## ✅ Completion Check

- [ ] **All above points checked and met**
- [ ] **Backtest report contains WFO metadata** (train/test periods, contract versions, used parameters)
- [ ] **Results peer-reviewed** or double-checked by another team member
- [ ] **Archive final setup** for future reference/reproduction

---

**WARNING:** Failure to meet any point in this checklist means **invalid backtest**. Results cannot be used for production decisions.

**Performance disclaimer:** Walk-forward optimization provides realistic performance estimates, but past performance is not a guarantee of future results.