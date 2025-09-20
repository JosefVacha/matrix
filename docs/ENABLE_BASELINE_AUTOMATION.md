Enable baseline auto-update (maintainer guide)

This document explains the safe, step-by-step procedure to opt-in to automated baseline updates for the smoke-run pipeline. It is intentionally conservative: enabling automation requires an explicit repo secret and a manual dispatch.

Prerequisites
- Repository admin permissions to set secrets and dispatch workflows.
- Review the smoke-run artifacts in Actions for at least 2 dry-run runs.

Safe opt-in steps
1. Run 2–3 dry-run workflows:
   - In Actions, find the `auto_update_baseline` workflow and use `Run workflow` with input `create_pr=false`.
   - Download the `smoke-artifacts` artifact and inspect:
     - `data/dataset_SMOKE.parquet` (or .pkl): check OHLCV columns, no label leakage.
     - `outputs/paper_trade_report.json`: review trades and timestamps.
     - `outputs/paper_trade_metrics.json`: confirm metrics make sense.

2. Validate dry-run results:
   - Confirm that `scripts/qa/compare_metrics_to_baseline.py` reports no unexpected regression.
   - If flaky results appear, re-run until stable; consider pinning pyarrow/fastparquet in CI.

3. Set opt-in secret:
   - Go to repository Settings → Secrets → Actions.
   - Add `ALLOW_NOTIFICATIONS` = `1` (string). This is the dual gate that prevents automatic pushes/PRs unless explicitly enabled.

4. Perform a final dry-run with PR creation enabled but push still gated:
   - Run `auto_update_baseline` with `create_pr=true`. The workflow will decide whether a baseline update is warranted and will attempt to create a PR, but `create_baseline_pr.py` requires the `--allow-push` flag and will only push when explicitly allowed.

5. Enable push (final step)
   - Once you are confident, run the `create_baseline_pr.py` helper with `--allow-push` locally or enable the workflow's push step by providing `ALLOW_NOTIFICATIONS=1` and confirming dispatch input `create_pr=true`.

Roll-back plan
- If an auto-update introduces an incorrect baseline, revert the baseline file via a PR and disable `ALLOW_NOTIFICATIONS` until the issue is resolved.

Audit and monitoring
- Keep the `workflow_lint_smoke` job enabled on PRs to surface differences early.
- The `notify_on_failure` workflow posts run failures to `NOTIFIER_WEBHOOK` if configured; otherwise it prints payloads for manual inspection.

Contact
- For questions, tag the maintainers in `CODEOWNERS` or open an issue in this repo.
