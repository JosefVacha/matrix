# MATRIX Stability Recap Table

Fill one row per sandbox run. Churn rate = share of entries that exit < cooldown. Qualitative entries OK for now.

| run_tag | report | ts_file | trigger_rate | long/short | churn_rate | max_dd | stability_notes |
|---------|--------|---------|--------------|------------|------------|--------|-----------------|
|         |        |         |              |            |            |        |                 |

<!-- Decision Note -->
[See TS_DECISION_20250919_SAMPLE.md](../DECISIONS/TS_DECISION_20250919_SAMPLE.md)
<!-- /Decision Note -->

## Instructions

SIM runs can be logged in the same table with `run_tag = SIM_<tag>` (clearly marked as synthetic).
- After each run, fill a new row with key metrics and notes.
- Use REPORT and SUMMARY files for values.
- You can prefill `churn_rate` and initial `stability_score` using:
	- `python scripts/metrics/calc_churn.py --report docs/REPORTS/REPORT_<DATE>_<TAG>.md`
	- `python scripts/metrics/calc_stability_score.py --summaries docs/summaries/SUMMARY_*.md [... ]`
- Churn rate: % of entries that exit before cooldown period.
- Stability notes: qualitative assessment (e.g., "stable", "oscillating", "imbalanced").
