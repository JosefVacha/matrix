# MATRIX Threshold Selection Workflow

This document defines the systematic methodology for converting model predictions into trading signals through threshold optimization. The process uses a 3-step approach focused on robustness and stability.

## Overview

**Goal**: Convert continuous predictions (e.g., return forecasts) into discrete trading signals (long/short/neutral) using optimized thresholds.

**Approach**: Grid-based optimization with walk-forward validation, prioritizing stability over peak performance.

**Output**: Threshold parameters for UP/DOWN entry, hysteresis bands, and cooldown periods.

## Step 1: Grid Sweep Definition

### Basic Grid Structure
Define a symmetric grid around zero for regression-based predictions (mode='R' from `generate_labels()`):

```
Threshold Parameters:
- UP_THRESHOLD: Minimum prediction value to trigger long entry
- DOWN_THRESHOLD: Maximum prediction value to trigger short entry (typically negative)
- HYSTERESIS: Buffer zone to prevent oscillation
- COOLDOWN: Minimum bars between signal changes
```

### Grid Design Principles
- **Symmetric around zero**: If UP=+X, then DOWN=-X (for return-based predictions)
- **Conservative starting points**: Begin with wider thresholds, narrow down if stable
- **Reasonable step sizes**: Allow sufficient granularity without overfitting
- **Limited grid size**: Avoid excessive computation and overfitting risk

### Example Grid Framework (NO SPECIFIC VALUES)
```
Base Thresholds:
- Primary range: [small, medium, large] relative to prediction distribution
- Hysteresis ratios: [none, small, medium] as percentage of base threshold
- Cooldown periods: [short, medium, long] in number of bars

Grid Points:
- UP/DOWN pairs: Generate symmetric pairs around zero
- Hysteresis variants: For each UP/DOWN pair, test hysteresis levels
- Cooldown combinations: For promising UP/DOWN/hysteresis, test cooldown periods
```

### Hysteresis Logic
```
Entry Conditions:
- Long Entry: prediction > UP_THRESHOLD
- Short Entry: prediction < DOWN_THRESHOLD

Exit Conditions (with hysteresis):
- Long Exit: prediction < (UP_THRESHOLD - HYSTERESIS)
- Short Exit: prediction > (DOWN_THRESHOLD + HYSTERESIS)

Neutral Zone:
- No new signals when: (DOWN_THRESHOLD + HYSTERESIS) < prediction < (UP_THRESHOLD - HYSTERESIS)
```

### Cooldown Implementation
```
Signal Timing Rules:
- After any signal (entry or exit), wait COOLDOWN bars before next signal
- Prevents excessive trading in volatile periods
- Accumulate prediction "pressure" during cooldown
- Resume signaling after cooldown expires
```

## Step 2: Walk-Forward Optimization Evaluation

### Evaluation Framework
For each grid point, evaluate performance across all WFO blocks:

```
For each threshold combination:
    For each WFO block:
        1. Apply thresholds to test period predictions
        2. Generate signals using threshold logic
        3. Calculate performance metrics
        4. Record stability indicators
    Aggregate results across blocks
    Rank by composite score
```

### Primary Metrics (Robust Focus)
1. **Hit Rate**: Percentage of profitable trades
2. **Average Trade Return**: Mean return per trade (before fees)
3. **Drawdown Guard**: Maximum consecutive losing streak length
4. **Exposure Balance**: Time in market vs. neutral periods

### Secondary Metrics (Stability Assessment)
1. **Cross-Block Consistency**: Standard deviation of hit rate across WFO blocks
2. **Signal Rate Stability**: Consistency of trading frequency across periods
3. **Return Distribution**: Skewness and tail risk measures
4. **Market Regime Robustness**: Performance across different market conditions

### Composite Scoring Method
```
Threshold Score = Weighted Average of:
- Hit Rate (weight: high) - primary signal quality indicator
- Avg Trade Return (weight: high) - profitability assessment
- Drawdown Guard (weight: medium) - risk management
- Cross-Block Stability (weight: high) - robustness priority
- Signal Rate (weight: low) - activity level preference
```

### Ranking and Selection Criteria
1. **Minimum Performance Gates**: Threshold combinations must pass basic quality filters
2. **Stability Priority**: Prefer consistent performance over peak single-block results
3. **Risk-Adjusted Returns**: Consider drawdown and volatility in ranking
4. **Practical Constraints**: Ensure reasonable signal frequency and market exposure

## Step 3: Stability Check and Final Selection

### Stability Analysis
Before finalizing threshold selection, perform comprehensive stability assessment:

```
Stability Validation:
1. Performance Variance: Low standard deviation across WFO blocks
2. Regime Independence: Consistent behavior in different market conditions
3. Time Stability: No significant performance degradation over time
4. Parameter Sensitivity: Robust to small threshold adjustments
5. Signal Quality: Consistent signal characteristics across periods
```

### Multi-Block Validation
```
For top-ranked threshold combinations:
1. Detailed block-by-block analysis
2. Performance distribution visualization
3. Outlier block investigation
4. Market condition correlation analysis
5. Signal timing pattern analysis
```

### Final Selection Criteria
```
Selection Priority (in order):
1. Passes all stability gates
2. Consistent positive hit rate across blocks
3. Reasonable signal frequency (not too sparse/frequent)
4. Low cross-block performance variance
5. Good risk-adjusted returns
6. Intuitive parameter values (easier to explain/adjust)
```

### Documentation Requirements
```
Selected Threshold Documentation:
- Final UP/DOWN threshold values
- Hysteresis and cooldown parameters
- Performance summary across WFO blocks
- Stability analysis results
- Alternative threshold sets for comparison
- Market condition performance breakdown
- Signal characteristics summary
```

## Implementation Notes

### Code Integration Points
- See `src/matrix/strategy/core.py` for threshold implementation TODOs
- Reference `docs/LABELS.md` for prediction semantics
- Use `docs/METRICS_CHECKLIST.md` for evaluation metrics
- Follow `docs/SANDBOX_BT.md` for testing protocol

### Configuration Management
```
Threshold Configuration Structure:
{
    "up_threshold": <float>,
    "down_threshold": <float>,
    "hysteresis": <float>,
    "cooldown_bars": <int>,
    "validation_date": "YYYY-MM-DD",
    "wfo_blocks_tested": <int>,
    "stability_score": <float>
}
```

### Continuous Improvement
1. **Regular Re-optimization**: Re-run threshold optimization periodically
2. **Market Adaptation**: Adjust thresholds for changing market regimes
3. **Performance Monitoring**: Track actual vs. backtested performance
4. **Parameter Drift**: Monitor threshold effectiveness over time

## Quality Assurance

### Validation Checklist
- [ ] Grid design covers reasonable parameter space
- [ ] WFO evaluation follows temporal integrity rules
- [ ] Stability analysis includes multiple dimensions
- [ ] Selected thresholds pass all quality gates
- [ ] Documentation includes full methodology
- [ ] Results are reproducible with same data/config

### Common Pitfalls to Avoid
1. **Overfitting**: Too narrow grid or excessive optimization
2. **Look-ahead bias**: Using future information in threshold selection
3. **Single-block bias**: Optimizing for best single period instead of stability
4. **Ignoring transaction costs**: Not accounting for fees and slippage
5. **Unrealistic expectations**: Expecting perfect prediction-to-signal conversion

## Decision Rules

### Systematic Threshold Selection Criteria

**For data-driven threshold determination from sandbox backtest results:**

### Distribution-Based Selection
- **UP/DOWN Positioning**: Choose thresholds near distribution tails where trigger rate falls inside target band
- **Percentile Anchoring**: Prefer threshold positions at meaningful percentiles (P10, P25, P75, P90) for interpretability
- **Tail Optimization**: Focus on prediction extremes that indicate higher confidence signals
- **Central Tendency Avoidance**: Avoid thresholds too close to mean/median where signal quality is weakest

### Signal Rate Optimization  
- **Target Band Compliance**: Ensure long/short trigger rates fall within desired frequency range
- **Imbalance Control**: Enforce long/short signal imbalance ≤ maximum tolerance (e.g., ±10%)
- **Activity Balance**: Maintain reasonable signal frequency - not too sparse (under-trading) or frequent (over-trading)
- **Neutral Time Respect**: Preserve sufficient no-signal periods for market observation and model confidence

### Hysteresis and Timing Rules
- **Noise Buffer**: Apply hysteresis ≥ one bar worth of typical prediction noise to avoid signal flip-flop
- **Oscillation Prevention**: Size hysteresis based on observed rapid entry→exit→entry patterns in sandbox results
- **Exit Logic**: Use (threshold ± hysteresis) for exit signals to create stable entry/exit bands
- **Qualitative Sizing**: Prefer empirically-derived hysteresis over theoretical calculations

### Cooldown Determination
- **Hold Time Based**: Set cooldown to ceil(median holding period) from sandbox backtest report  
- **Natural Development**: Allow sufficient time for positions to develop before re-evaluation
- **Volatility Adaptation**: Consider extending cooldown in high-volatility periods (qualitative adjustment)
- **Minimum Constraint**: Enforce minimum 1-bar cooldown regardless of median hold time

### Stability Priority
- **Cross-Block Consistency**: Prefer threshold settings stable across multiple WFO blocks over peak single-block performance
- **Regime Robustness**: Choose thresholds that work across different market conditions present in data
- **Parameter Sensitivity**: Select threshold values that are robust to small adjustments (avoid knife-edge optimization)
- **Future Generalization**: Prioritize settings likely to work on unseen data over perfect historical fit

### Implementation Guidelines
- **Documentation First**: Record all threshold decisions with data-driven rationale in REPORT_TEMPLATE.md
- **Iterative Refinement**: Use initial thresholds as starting point for subsequent optimization cycles
- **Conservative Bias**: When uncertain between options, choose more conservative (less frequent trading) thresholds
- **Validation Requirement**: Test proposed thresholds in second sandbox run before production consideration

---

**Note**: This document provides the methodology framework. Specific threshold values should be determined through empirical testing following this workflow and decision rules. See docs/REPORT_TEMPLATE.md "Thresholds Extraction" section for data-driven proposal format.