<!--
Baseline update PR template
This template is used for automated or manual PRs that update baseline metrics.
Do NOT merge until reviewers confirm artifacts and metrics.
-->

## Summary

This PR updates baseline metrics (ci/baselines/paper_trade_metrics_baseline.json) following a smoke-run.

## Artifacts

- Smoke dataset: attached in workflow artifacts (`smoke-artifacts`)
- Paper trade report: `outputs/paper_trade_report.json` (artifact)
- Extracted metrics: `outputs/paper_trade_metrics.json` (artifact)

## Checklist for reviewers

- [ ] Artifacts present and downloadable from the workflow run
- [ ] Metrics change is expected and reasonable (check final_net, max_drawdown)
- [ ] No suspicious data leakage in the generated dataset (OHLCV columns unchanged)
- [ ] Confirm that the update is the result of benign drift/improvement, not a test flake
- [ ] If enabling auto-merge / baseline overwrite, confirm maintainers have set `ALLOW_NOTIFICATIONS=1`

Additional notes for maintainers:
- If you need to reproduce locally, run the `workflow_lint_smoke` job steps or execute:

```bash
python3 scripts/qa/generate_smoke_dataset.py --path data/dataset_SMOKE.parquet --start 2024-01-01 --end 2024-01-03
python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json
python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json
```
