# MATRIX Roadmap

## Milestones

### M0 (now): Offline Sandbox Foundations
- **Goals:**
  - Build offline sandbox for reproducible threshold/signal workflow
  - Implement summaries, diffs, validators, synthetic simulator, reference mapping
- **Deliverables:**
  - TS_*.yml versioning, diff, rollback
  - Pure Python mapping function
  - Synthetic simulator + summary
  - Governance docs (ADRs, contributing, standards)
- **Exit Criteria:**
  - All workflows run offline, deterministic
  - Mapping function unit-tested
  - SIM summary and recap table populated
- **Risks:**
  - Overfitting to synthetic data
  - Manual errors in threshold selection

### M1: Freqtrade-Compatible Strategy (Offline)
  - Integrate mapping logic into Freqtrade strategy skeleton
  - Run first reproducible backtest (offline)
  - Strategy wiring (no live trading)
  - Backtest protocol docs
  - Strategy runs with static data, produces summary
  - Freqtrade API changes
  - Data leakage in mapping
  - Adapter skeleton (src/matrix/adapter/freqtrade_strategy_adapter.py)
  - DRY backtest protocol doc (docs/DRY_BACKTEST_PROTOCOL.md)
  - Example config (configs/strategy.adapter.example.json)
  - Test skeletons (tests/test_adapter_contracts.py)
  - Risks: mismatch between mapping.py docstrings and adapter behavior → run “contract review” before DRY run
  - Exit criteria: first reproducible DRY BT using MatrixAdapterStrategy + REPORT + SUMMARY + STABILITY_RECAP row + ingest Freqtrade reports into SUMMARY + update STABILITY_RECAP.md
  - DRY runbook (docs/RUNBOOK_DRY.md) and rehearsal helper (scripts/runbook/dry_run_rehearsal.py)
  - Thresholds changelog (docs/thresholds/CHANGELOG.md, scripts/thresholds/changelog_from_diffs.py)
  - Exit criteria box: see RUNBOOK_DRY.md and STABILITY_RECAP.md row
  - [x] Milestone M1 exit criteria met — see [TS_DECISION_20250919_SAMPLE.md](docs/DECISIONS/TS_DECISION_20250919_SAMPLE.md)

### M2: Minimal FreqAI Features, Labels, and Training Protocol
**Goals:**
  - Implement minimal, real feature set and label semantics (offline, docs-first)
  - Document training protocol (walk-forward splits, baseline model spec, reproducibility)
  - Establish model registry and metadata structure
  - Offline evaluation and summary
**Deliverables:**
  - FreqAI hooks with documented feature/label contracts
  - TRAINING_PROTOCOL.md and config placeholders
  - Model registry docs and file layout
  - WFO evaluation summary template
**Exit Criteria:**
  - One trained model artifact + metadata
  - WFO evaluation summary + decision note
  - All steps reproducible offline
**Risks:**
  - Feature/label drift between train/test
  - Leakage via label/feature windows
  - Incomplete metadata or audit trail

### M3: Telemetry & Semi-Automatic Summaries
**Goals:**
  - Add telemetry plumbing
  - Automate summary/diff generation
  - Compare threshold sets
**Deliverables:**
  - Telemetry hooks
  - Automated metrics extraction
  - Threshold diff reports
**Exit Criteria:**
  - Summaries/diffs generated with one command
**Risks:**
  - Incomplete metrics coverage
  - Drift in feature definitions
