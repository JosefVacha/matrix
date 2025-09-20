# PR Review Comment (copy-paste)

This is a short comment you can paste into the draft PR to speed review and explain safety choices.

```
Summary:
- Adds a deterministic paper-trading smoke simulator (`scripts/trading/paper_trading_sim.py`) and a metrics extractor.
- Implements QA guardrails and a dry-run-first baseline proposal pipeline (`scripts/qa/create_baseline_pr.py`, `.github/workflows/propose_baseline_pr.yml`).
- Notifier and automated push/PR are safe-by-default: remote writes require both `--allow-push` and repository secret `ALLOW_NOTIFICATIONS=1`.

What I ran locally to validate:
- `python3 scripts/qa/check_copilot_guardrails.py` — PASS
- `python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json`
- `python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json`
- `python3 scripts/qa/compare_metrics_to_baseline.py --metrics '{"final_net":0.05}'` — dry-run comparator

Key review points:
1) Confirm `create_baseline_pr.py` prints the proposed payload in dry-run and refuses to push unless `ALLOW_NOTIFICATIONS=1` and `--allow-push` are provided.
2) Inspect artifacts from a CI dry-run (see `docs/CI_RUN_INSTRUCTIONS.md`) before enabling automation.
3) Consider whether you want the baseline file (`ci/baselines/paper_trade_metrics_baseline.json`) to include the new per-trade drawdown/trade stats; I left it seeded with the smoke-run values.

Suggested next steps if approved:
- Add repo secret `ALLOW_NOTIFICATIONS=1` (Settings → Secrets → Actions) to enable push-enabled runs.
- Optionally set `DEFAULT_PR_REVIEWERS` and `DEFAULT_PR_LABELS` to auto-request reviewers and apply labels when PRs are created.

If reviewers want, I can dispatch the push-enabled workflow and report back the created PR link and artifacts (I will not run it until `ALLOW_NOTIFICATIONS` is set).
```
