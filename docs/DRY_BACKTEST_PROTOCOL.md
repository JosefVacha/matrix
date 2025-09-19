# DRY Backtest Protocol (Offline Only)

## Preconditions
- Local Freqtrade install (no API keys, no downloads)
- Local candles (static data only)
- Static pairlist (see configs/pairlist.static.json)
- No API keys in config

## Steps
1. Copy `configs/backtest.sandbox.example.json` → `configs/backtest.dry.json` (keep .gitignored)
2. Pick a threshold set `TS_*.yml` from `docs/thresholds/sets/` and print values via `scripts/thresholds/print_thresholds.py`
3. Inject thresholds into `MatrixAdapterStrategy` (see docstring for location); keep changes local
4. Run Freqtrade dry-run/backtest via CLI:
   ```bash
   freqtrade backtesting --config configs/backtest.dry.json --strategy MatrixAdapterStrategy
   ```
5. Fill `docs/REPORTS/REPORT_<DATE>_DRY.md` (use template + markers)
6. Generate SUMMARY and optional DIFF; update STABILITY_RECAP row

## Guardrails
- Use static pairlist only
- Same feature pipeline for train/test
- Record commit hashes for CONTRACTS, LABELS, TS

## References
- CONTRACTS.md (Strategy I/O)
- THRESHOLDS_SETS.md (Thresholds format)
- REPORT_TEMPLATE.md, METRICS_SUMMARY_TEMPLATE.md
