# PR Review Checklist — Guardrails, Baseline & Smoke-run

This short checklist helps maintainers review the draft PR that adds QA guardrails, the paper-trade simulator, baseline automation, and notifier playbook.

1) Quick links
  - Draft PR: https://github.com/JosefVacha/matrix/pull/10
  - Branch: chore/qa-guardrails-notifier-ready

2) High-level review items
  - Ensure the guardrail runner (`scripts/qa/check_copilot_guardrails.py`) still runs and reports PASS locally.
  - Verify simulator artifacts are deterministic and include `equity` + per-trade `pnl`:
    - `outputs/paper_trade_report.json`
    - `outputs/paper_trade_report_trades.csv`
    - `outputs/paper_trade_metrics.json`
  - Confirm `ci/baselines/paper_trade_metrics_baseline.json` seeded values are reasonable and documented.
  - Confirm notifier automation is safe-by-default: dry-run default, and remote writes require `--allow-push` + repo secret `ALLOW_NOTIFICATIONS=1`.

3) Local validation commands (run these in the repo root inside the venv)

```bash
# 1) Run guardrails
python3 scripts/qa/check_copilot_guardrails.py

# 2) Run smoke simulator (writes outputs/paper_trade_report.json)
python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json

# 3) Extract metrics
python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json

# 4) Compare to baseline (dry-run)
python3 scripts/qa/compare_metrics_to_baseline.py --metrics '{"final_net":0.05,"max_drawdown":0.10}'

# 5) Run improvement check (returns exit 0 when improvement detected)
python3 scripts/qa/check_for_baseline_improvement.py --metrics '{"final_net": 0.01}'
```

4) Approval criteria (suggested)
  - All local checks pass and produce artifacts matching those in the PR (or explain the change in the PR body)
  - Baseline change is justified (delta and run link present in PR body)
  - Secrets and automation remain gated (do NOT remove dry-run defaults)
  - At least one reviewer approves before merging any `allow_push`-enabled workflow changes

5) If enabling notifications
  - Add `ALLOW_NOTIFICATIONS` repo secret with value `1` only after at least one dry-run is reviewed
  - Re-run the dispatched workflow with `allow_push=true` and `allow_notifications=true` for a single verified run

6) Notes for maintainers
  - The PR is intentionally conservative: dry-run by default and requires explicit repo secret to allow remote writes.
  - If you want me to run the propose-baseline workflow dry-run and collect artifacts, tell me and I will prepare/execute the dispatch command.
