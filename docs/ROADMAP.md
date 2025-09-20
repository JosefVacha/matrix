```markdown
# MATRIX Roadmap — complete plan toward paper trading and production readiness

This roadmap expands the existing milestones and lays out a clear path from the current offline sandbox to paper trading (simulation) using FreqAI for model-driven signals and finally to a safe, documented production workflow.

## Overarching phases
- Phase 0 — Offline foundations & QA (current)
- Phase 1 — Strategy adapter & reproducible backtest (Freqtrade-compatible, offline only)
- Phase 2 — Training and evaluation (FreqAI hooks, WFO, model registry)
- Phase 3 — Paper trading (simulator + exchange-sim layer, no real orders)
- Phase 4 — Controlled live testing (small position sizes, monitoring, kill-switch)

---

## Phase 0 — Offline foundations & QA (M0)
- Goals: deterministic offline experiments, robust guardrails, developer hygiene.
- Deliverables: guardrail runner, unit tests, smoke dataset, docs, maintainers guide.
- Exit criteria: validators pass locally and in CI; reproducible smoke runs.

## Phase 1 — Strategy adapter & reproducible backtest (M1)
- Goals: adapter that converts model predictions to Freqtrade-style signals, reproducible dry backtests.
- Deliverables:
  - Adapter skeleton (MatrixAdapterStrategy) and contract tests
  - DRY backtest protocol and runbook
  - Example config and static pairlist
- Exit criteria: dry backtest produces SUMMARY + REPORT and ingests into stability recap.

## Phase 2 — Training, registry, and WFO (M2)
- Goals: minimal feature set, labels, and training pipeline; model registry & metadata.
- Deliverables:
  - FreqAI-compatible feature hooks and label logic
  - Training runner with walk-forward split, metrics output, and WFO summary
  - Model registry with validation scripts and metadata schema
- Exit criteria: one trained model evaluated via WFO and committed to registry.

## Phase 3 — Paper trading (M3)
- Goals: run a realistic paper-trading simulation that consumes OHLCV data and model predictions (or rule-based signals) and simulates order execution, fees, slippage, and P&L.
- Deliverables:
  - Safe paper-trading simulator (scripts/trading/paper_trading_sim.py)
  - Standardized dataset format (OHLCV with datetime index) and example dataset `data/dataset_SMOKE.parquet`
  - Metrics & reports (equity curve, drawdown, trade list, per-trade P&L)
  - Integration with FreqAI predictions: document how to use a trained model to generate signals for the simulator
  - Tests and smoke-run example
- Exit criteria:
  - Paper-trading run reproduces expected results against the smoke dataset
  - Reports generated and artifacts uploaded for review

## Phase 4 — Controlled live testing (M4)
- Goals: move from paper to controlled live testing with manual approvals and strict limits.
- Deliverables:
  - Risk rules, kill-switch, telemetry (latency, hit-rate), and notifications
  - Small-size live testing plan (no market orders > X% of free capital)
  - Audit logs & monitoring
- Exit criteria: maintained P&L, acceptable risk metrics, and documented process for scaling to larger sizes.

---

## Immediate roadmap items (next 30 days)
1. Finalize the paper-trading simulator and example run (this PR)
2. Create a short how-to for converting a trained FreqAI model to simulator signals
3. Add a CI smoke job that runs the paper-trading simulator with a tiny dataset to catch regressions
4. Prepare a playbook for maintainers to enable notifications and monitor failures

## How this maps to repository artifacts
- `scripts/qa/check_copilot_guardrails.py` — guardrails
- `scripts/qa/notify_guardrail_failure.py` — notifier (safe-by-default)
- `scripts/training/*` & `scripts/registry/*` — training & registry helpers
- `scripts/trading/paper_trading_sim.py` — paper trading simulator (new)
- `data/dataset_SMOKE.parquet` — canonical smoke dataset (existing)
- `Makefile` targets: `make paper-trade-sim`, `make run-guardrails`, `make simulate-notifier`

## Notes on safety and reproducibility
- Paper-trade simulator is offline-only and writes artifacts; by default it will not connect to exchanges or post notifications.
- The notifier requires explicit enablement (flags + `ALLOW_NOTIFICATIONS=1`) to perform remote actions.

---

If you approve, I'll add the safe paper-trading simulator script and a Makefile target and run a smoke paper-trade using `data/dataset_SMOKE.parquet`.

```
