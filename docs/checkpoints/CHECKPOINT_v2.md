# CHECKPOINT v2 — 2025-09-19 14:00 (Europe/Prague)

## Context
- Offline-first framework on top of Freqtrade/FreqAI; English-first repo; no live keys.
- M2 focus: features/labels semantics, builder, WFO eval, validators, runbooks.

## Done
- Dataset builder (Parquet/PKL + smoke).
- WFO evaluation runner + JSON/MD summary + echo tasks.
- Contracts/validators: H-consistency, doc-consistency, OHLCV health, metadata.
- DRY runbook + ingest + summaries + recap wiring.

## Decisions
- Baseline metrics scope (DQ/Signal/Perf/Risk) kept simple and deterministic.
- JSON schemas stabilized (reports/summaries/WFO).
- Threshold governance remains manual with DIFF + decision notes.

## In Progress
- Pin concrete tool versions (Python/pandas/numpy/Freqtrade/FreqAI) — pending.
- CI for smoke/validators — pending.

## Next 3 Steps
1) M3.1: Minimal training runner (offline) → train baseline model on dataset, write models/<tag>/metadata.json (no .pkl tracked).
2) M3.2: Registry helpers (init_model_tag.py finalize, metadata validator, provenance).
3) M3.3: Retrain cadence policy → doc→check script stub (time/drift/perf), wire to ROADMAP exit criteria.
