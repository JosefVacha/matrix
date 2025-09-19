# STABILITY_SCORE.md

## MATRIX Threshold Stability Score (Qualitative)

### Components (weights TBD)

1. **Trigger Rate Consistency**
   - Measures how stable the long/short signal rates are across WFO blocks
   - Penalize large deviations from block to block
2. **Long/Short Balance Penalty**
   - Penalize excessive imbalance between long and short signals
   - Target: difference ≤ threshold (e.g., ±10%)
3. **Churn/Flip-Flop Penalty**
   - Penalize frequent entries/exits within less than the cooldown period
   - Indicates unstable or noisy signal logic
4. **Drawdown Proxy Penalty**
   - Use max drawdown or consecutive losses as a proxy for risk
   - Penalize high drawdown or long losing streaks

### Scoring
- **Range**: 0–100 (higher = more stable)
- **Formula**: Qualitative, not coded yet. Use weighted sum of above components (weights to be determined empirically).
- **Interpretation**:
  - 90–100: Highly stable, robust across blocks
  - 70–89: Acceptable stability, minor issues
  - 50–69: Marginal, needs improvement
  - <50: Unstable, not recommended

### TODO
- Define exact formulas and weights after more sandbox runs
- Automate extraction of metrics for scoring
- Document scoring rationale in REPORT_TEMPLATE.md