# MATRIX “First Numbers” Protocol

## Inputs
- **REPORT**: Use PRED_DIST and SIGNALS sections (see markers)
- **THRESHOLDS.md**: Decision rules and rationale

## Steps
1. **Pick Initial UP/DN**
   - Use tails of prediction distribution (PRED_DIST) to set UP/DN so trigger rate matches target band (see SIGNALS).
   - Document rationale in TS_*.yml meta.
2. **Set Hysteresis & Cooldown**
   - Hysteresis ≥ one-bar noise proxy (estimate from price/feature volatility).
   - Cooldown ≈ median hold time (ceil from SIGNALS marker).
3. **Record Threshold Set**
   - Save as TS_*.yml with provenance (commit, timerange, model_tag).
4. **Plan Second Run & Stability Score**
   - Use new thresholds for next sandbox run.
   - Compute qualitative Stability Score (churn, imbalance, drawdown).

## Pitfalls
- Overfitting to single block/run
- Imbalance > tolerance
- Churn > cooldown

## Audit Trail
- Link all threshold changes to REPORT and SUMMARY.
- Use PR template and validators before merging.
