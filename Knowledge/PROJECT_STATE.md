# MATRIX - Project State

## Current Project Status / Aktuální stav projektu
**Last Updated / Datum poslední aktualizace:** 19 September 2025
**Phase / Fáze:** M2 closed via CHECKPOINT v2
**Status:** 🟢 M2 milestone closed: dataset builder, WFO eval, validators, runbooks, summary wiring

## Completed Tasks / Co bylo dokončeno
- Dataset builder (Parquet/PKL + smoke)
- WFO evaluation runner + JSON/MD summary + echo tasks
- Contracts/validators: H-consistency, doc-consistency, OHLCV health, metadata
- DRY runbook + ingest + summaries + recap wiring

## Decisions
- Baseline metrics scope (DQ/Signal/Perf/Risk) kept simple and deterministic
- JSON schemas stabilized (reports/summaries/WFO)
- Threshold governance remains manual with DIFF + decision notes

## Open Items
- Pin concrete tool versions (Python/pandas/numpy/Freqtrade/FreqAI) — pending
- CI for smoke/validators — pending


## Milestone M3.1 Complete
- Training runner implemented: scripts/training/train_baseline.py (offline, deterministic)
- Registry metadata: models/<tag>/metadata.json (idempotent, contract-compliant)
- Smoke test: tests/test_train_baseline.py (validates summary + metadata)

## Lessons / Follow-ups
- Pin tool versions (Python, pandas, numpy, Freqtrade, FreqAI) — still pending for full reproducibility
- CI for smoke/validators — to be added for automated checks
- Registry helpers and retrain cadence policy are next (M3.2/M3.3)

## Next Steps
1) M3.2: Registry helpers (init_model_tag.py, metadata validator, provenance, schema)
2) M3.3: Retrain cadence policy (doc, check script, echo task)
