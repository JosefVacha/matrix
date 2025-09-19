## PR Ritual

Before merging any threshold change:
- Fill out `.github/pull_request_template.md`.
- Run markers validator: `python scripts/metrics/validate_report_markers.py --report docs/REPORTS/REPORT_<DATE>_<TAG>.md`
- Run threshold set validator: `python scripts/thresholds/validate_threshold_set.py --file docs/thresholds/sets/TS_<DATE>_<TAG>.yml`
- Link REPORT, SUMMARY, and chosen TS set in PR.
# MATRIX Threshold Sets & Audit Trail

## Versioning & Audit
- All threshold sets are stored in `docs/thresholds/sets/TS_*.yml`.
- Each change must be documented here with rationale and stability notes.

## Threshold Set Diffing & Audit Trail
Use `scripts/thresholds/diff_thresholds.py` to compare any two threshold sets in `docs/thresholds/sets/`:
	`python scripts/thresholds/diff_thresholds.py --a docs/thresholds/sets/TS_A.yml --b docs/thresholds/sets/TS_B.yml --out docs/diffs/DIFF_TS_A_vs_B.md`
Output Markdown diff report to `docs/diffs/DIFF_TS_<A>_vs_<B>.md` using the [DIFF_REPORT_TEMPLATE.md](../DIFF_REPORT_TEMPLATE.md).
Document all major changes and rationale in this file for auditability.

## Example Entry
- **2025-01-01:** Created TS_20250101_BASE.yml (baseline thresholds)
- **2025-02-01:** Updated TS_20250201_GRID.yml (grid sweep)
- **2025-02-02:** Diff run: DIFF_TS_20250101_BASE_vs_20250201_GRID.md (see summary below)

---

## Change Log
| Date       | Set Name                | Change Type | Notes |
|------------|-------------------------|-------------|-------|
| 2025-01-01 | TS_20250101_BASE.yml    | Baseline    | Initial offline thresholds |
| 2025-02-01 | TS_20250201_GRID.yml    | Grid Sweep  | Parameter sweep for WFO |
| 2025-02-02 | DIFF_TS_20250101_BASE_vs_20250201_GRID.md | Diff | Major changes in stoploss, minor in ROI |

---

## Stability Notes
- <Add stability scoring and rationale for each threshold change>
