# Maintainer checklist — enabling notifier & baseline PRs

This checklist helps repository maintainers safely enable notifications and review automated baseline PRs.

Before enabling notifications
- Ensure the `ci/baselines/paper_trade_metrics_baseline.json` file exists and is reviewed.
- Confirm that the smoke-run CI (Actions → Smoke backtest) runs cleanly on the target branch.
- Add `GITHUB_TOKEN` and set `ALLOW_NOTIFICATIONS` to `1` only in the protected repository (not in forks).

Enabling the flow
1. Add or verify the following repository secrets:
   - `GITHUB_TOKEN` (automatically available in Actions; required for API writes)
   - `ALLOW_NOTIFICATIONS` = `1` (enables pushes from CI)
   - Optional: `DEFAULT_PR_REVIEWERS` and `DEFAULT_PR_LABELS`
2. Manually trigger the `Smoke backtest` workflow and inspect the logs for the `create_baseline_pr.py` dry-run output.
3. If dry-run is acceptable, re-run the workflow with secrets in place; the job will attempt to push and create a PR.

Reviewing baseline PRs
- Check the PR body: it contains old/new final_net, delta, and workflow run link.
- Confirm that artifacts are attached to the workflow run (Outputs tab) and that metrics are correct.
- If everything is OK, merge the PR to update `ci/baselines/paper_trade_metrics_baseline.json`.

Rollback
- If an accidental baseline update occurs, revert `ci/baselines/paper_trade_metrics_baseline.json` and set `ALLOW_NOTIFICATIONS=0` until the flow is reviewed.

Monitoring scheduled runs and safe rollout
- Start with dry-runs only: use the workflow dispatch UI to run the `Auto-update baseline` workflow with `create_pr=false` and inspect artifacts.
- After 2-3 successful dry-runs (no unexpected metric regressions), test a manual dispatch with `create_pr=true` while keeping `ALLOW_NOTIFICATIONS` empty — this will log the PR creation attempt but skip the push.
- Only set repository secret `ALLOW_NOTIFICATIONS=1` when you are ready to allow automated PR creation. Prefer enabling this during a maintenance window and with an on-call reviewer assigned.

Secrets and repository settings checklist
- `GITHUB_TOKEN`: default Action token (ensure it has repo write permissions in org/policy if required).
- `ALLOW_NOTIFICATIONS`: set to `1` to enable pushes/PR creation from the workflow. Keep this unset or `0` for dry-run-only operation.
- Optional secrets supported by the PR creator script: `DEFAULT_PR_REVIEWERS`, `DEFAULT_PR_LABELS`.

Troubleshooting
- If the scheduled run fails to generate artifacts, open the Actions run and download `auto-update-artifacts` to inspect `paper_trade_report.json` and `paper_trade_metrics.json`.
- If the `should_update_baseline.py` output looks wrong, run it locally against `outputs/paper_trade_metrics.json` to reproduce and debug.
