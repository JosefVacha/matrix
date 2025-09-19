# DRY Backtest Runbook (Canonical Flow)

## Inputs
- Static pairlist: `configs/pairlist.static.json`
- Config: `configs/backtest.dry.json` (copied from example)
- Thresholds: chosen `docs/thresholds/sets/TS_*.yml`

## Steps
1. **Select thresholds**
   - Run: `python scripts/thresholds/validate_threshold_set.py --file <TS>`
   - Print: `python scripts/thresholds/print_thresholds.py --file <TS>`
2. **Inject thresholds**
   - Edit: `strategies/MatrixAdapterStrategy.py` (local only)
3. **Run Freqtrade DRY/backtest (manual)**
   - CLI: `freqtrade backtesting --config configs/backtest.dry.json --strategy MatrixAdapterStrategy`
   - See [FREQTRADE_OUTPUTS.md](../FREQTRADE_OUTPUTS.md) for output formats
4. **Save outputs**
   - Copy/paste JSON/CSV/txt to `docs/REPORTS/RAW/`
5. **Ingest outputs**
   - Run: `python scripts/metrics/ingest_freqtrade_report.py --input <RAW> --report <REPORT> --summary <SUMMARY>`
6. **Merge summaries**
   - Run: `python scripts/metrics/merge_summaries.py --inputs <SUMMARY> --out docs/STABILITY_RECAP.md`
7. **(Optional) Compute churn & stability**
   - Run: `python scripts/metrics/calc_churn.py --report <REPORT>`
   - Run: `python scripts/metrics/calc_stability_score.py --summaries <SUMMARY>`

## Exit Criteria (tick all before PR)
- [ ] All steps above completed for one DRY cycle
- [ ] REPORT and SUMMARY files created and filled
- [ ] STABILITY_RECAP.md updated with new row
- [ ] Thresholds changelog updated if DIFF detected
- [ ] Validators green (no missing markers, valid thresholds)

## Common Pitfalls
- Time range mismatch between config and outputs
- Pairlist mismatch (must match static pairlist)
- Missing markers in REPORT/SUMMARY
- Thresholds not injected or not matching TS file
