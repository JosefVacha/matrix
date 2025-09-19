# Threshold Set Decision — 2025-09-19 (SAMPLE)

## Context
- run_tag: SAMPLE_20250919
- TS file: docs/thresholds/sets/TS_SAMPLE_A.yml
- Commit hashes: CONTRACTS.md, TS_SAMPLE_A.yml, MatrixAdapterStrategy.py

## Evidence
- [REPORT](../REPORTS/REPORT_SAMPLE_DRY.md)
- [SUMMARY](../summaries/SUMMARY_SAMPLE_DRY.md)
- [STABILITY_RECAP](../STABILITY_RECAP.md) row
- [DIFF](../diffs/DIFF_TS_SAMPLE_A_vs_B.md)
- [CHANGELOG](../thresholds/CHANGELOG.md) entry

## Stability Recap
- trigger_rate: 0.12
- long_rate: 0.51
- short_rate: 0.49
- churn: 0.08
- max_drawdown: -0.12
- (see calculators for details)

## Decision
**KEEP** — Thresholds stable, churn and drawdown within acceptable range. No major drift detected. Ready to proceed to M2.
