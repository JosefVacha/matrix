Title: chore: update paper-trade baseline (seed with observed metrics)

Summary

This PR seeds the existing paper-trade baseline with the metrics produced by the validated smoke run. The baseline previously included placeholder zeros for trade-level statistics and `null` for `max_drawdown`. To make CI comparisons deterministic and actionable, this PR updates `ci/baselines/paper_trade_metrics_baseline.json` with the observed values.

Files changed

- `ci/baselines/paper_trade_metrics_baseline.json` — replaced placeholder trade P&L stats and `max_drawdown` with observed values.
- `docs/NOTIFIER_USAGE.md` — expanded maintainer playbook for safe enablement of remote notifications.
- `Knowledge/RUNBOOK.md` — added "Baseline & Notifier Playbook" section with step-by-step verification and rollback.

Rationale

- The smoke-run extractor now reliably emits `trade_pnl_*` and `max_drawdown`. Seeding the baseline prevents CI failures due to missing baseline fields and enables future regression detection.
- Notifier docs and RUNBOOK additions provide a safe, auditable process for maintainers to enable remote notifications.

How tested

- Local smoke run was executed and metrics were produced `outputs/paper_trade_metrics.json`.
- Unit tests: `pytest` run — all tests passed locally.
- Guardrail checks: `scripts/qa/check_copilot_guardrails.py` — PASS.

Checklist for reviewers

- [ ] Validate updated baseline values are acceptable as the seed values.
- [ ] Confirm documentation changes reflect your operational preferences.
- [ ] Optionally run the smoke-run locally using the commands in `Knowledge/RUNBOOK.md` to validate.

Notes

If maintainers prefer to keep `max_drawdown` out of the baseline until more smoke runs are collected, I can revert that value to `null` and only include the trade-level stats.
