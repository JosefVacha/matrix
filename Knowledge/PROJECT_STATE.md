# MATRIX - Project State

## Current Project Status / Aktuální stav projektu
**Last Updated / Datum poslední aktualizace:** 19 September 2025
**Recent changes:** committed QA guardrails, smoke dataset generator, and replaced pyarrow with fastparquet in `requirements-dev.txt` to avoid heavy wheel builds in CI.
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

## Short-term notes
- Dev dependency change: `pyarrow` -> `fastparquet` in `requirements-dev.txt` (CI-friendly).
- Current CI: validators pass but smoke job earlier failed due to missing SMOKE dataset; generator added and CI re-triggered. Monitor latest run.

### 2025-09-20 - CI / dev-deps follow-up
- Pinned `fastparquet` to `2024.11.0` in `requirements-dev.txt` after CI reported unavailable wheel for `2024.12.0`.
- Added minimal runtime install step (`python -m pip install pandas numpy`) to the `smoke` job in `.github/workflows/smoke-validators.yml` so `scripts/qa/generate_smoke_dataset.py` can run before full dev deps are installed.
- Rationale: avoid heavy native builds in CI (pyarrow) and prevent generator failing due to missing numpy/pandas.

CZ: Krátký záznam: připnuto `fastparquet>=2024.4.0,<2025.0`, přidán krok instalace `pandas` a `numpy` v `smoke` jobu. Sledujte následující CI runy a po jejich úspěchu aktualizujte PR popis a mergněte.
