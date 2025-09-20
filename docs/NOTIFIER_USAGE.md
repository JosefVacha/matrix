# Notifier & Baseline PR usage

This document explains how to safely enable the notifier and the automated baseline PR flow.

Important safety notes
- The notifier and baseline PR automation are gated behind the `ALLOW_NOTIFICATIONS` flag and require a valid `GITHUB_TOKEN` in the environment or repository secrets.
- Do NOT enable `ALLOW_NOTIFICATIONS` in a public fork or unreviewed branch. Only repository maintainers should enable it.

Short checklist to enable automatic baseline PRs in CI
1. Add a repository secret `GITHUB_TOKEN` (already present in GitHub Actions runners) and `ALLOW_NOTIFICATIONS` with value `1` when you are ready to allow pushes from CI.
2. Optionally set `DEFAULT_PR_REVIEWERS` and `DEFAULT_PR_LABELS` repository secrets to suggest reviewers/labels.
3. Verify that the `ci/baselines/paper_trade_metrics_baseline.json` file is present and correct.
4. Run the smoke CI workflow manually (`Actions -> Smoke backtest -> Run workflow`) and inspect the dry-run output of `scripts/qa/create_baseline_pr.py` in the logs.
5. If dry-run output looks good, enable `ALLOW_NOTIFICATIONS=1` and re-run the workflow to allow the script to push and create the PR.

Local dry-run example

```bash
# run smoke locally (create dataset, run sim, extract metrics)
python3 scripts/qa/generate_smoke_dataset.py --path data/dataset_SMOKE.parquet --days 30
python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json
python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json
python3 scripts/qa/create_baseline_pr.py
```

To perform the push and create the PR locally (requires GITHUB_TOKEN and ALLOW_NOTIFICATIONS=1):

```bash
export GITHUB_TOKEN=ghp_xxx
export ALLOW_NOTIFICATIONS=1
python3 scripts/qa/create_baseline_pr.py --allow-push
```

Rollback and safety
- If a baseline PR was created accidentally, maintainers can revert the baseline file in `ci/baselines/` and re-run the workflow after setting `ALLOW_NOTIFICATIONS=0`.

Contact and ownership
- Owner: repository maintainers (see `CONTRIBUTING.md` or project owners list)
# Notifier usage and safe enablement

This document explains how to safely enable remote notifications (GitHub issues, Slack, etc.) from CI or local scripts. Remote actions are intentionally gated and require explicit repository-level opt-in.

Why the gate
- Notifications and GitHub PR/issue creation are side-effects. By default the notifier writes artifacts only. Remote actions require both a CLI flag and an env var to avoid accidental posts from forks or accidental runs.

Maintainer playbook — safe enablement (step-by-step)

1) Decide scope
- Single-run (manual) — preferred for first verification: enable notifications only for a single manual workflow dispatch and inspect the produced artifact/PR.
- Repository-wide automation — enable only after manual verification and maintainer consensus.

2) Prepare repository secrets (maintainer)
- `ALLOW_NOTIFICATIONS` = `1` (string) — guard switch: required for any remote action to proceed. Default should be absent or `0`.
- `SLACK_WEBHOOK` (optional) — only if Slack posting is desired. Use a dedicated, rotatable webhook for a review channel.
- `GITHUB_TOKEN` — typically rely on the Actions-provided token. If a bot token is needed, store it here and document the token's scope.

3) Dry-run locally and in CI (mandatory)
- Local dry-run (no network):

```bash
python3 scripts/qa/notify_guardrail_failure.py \
  --input-file outputs/guardrail_failure-YYYYMMDD-HHMMSS.json \
  --dry-run
```

- Dry-run in CI: trigger the workflow but keep `--dry-run` or leave `ALLOW_NOTIFICATIONS` unset so no remote actions occur. Inspect the produced artifact and logs.

4) Manual single-run enable (verification)
- On a secure machine or under a maintainer account do:

```bash
export ALLOW_NOTIFICATIONS=1
export SLACK_WEBHOOK='https://hooks.slack.com/services/..'   # optional
export GITHUB_TOKEN='__EXAMPLE_GITHUB_TOKEN__'
export GITHUB_REPOSITORY='owner/repo'
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-YYYYMMDD-HHMMSS.json --enable-issues --enable-slack
```

- Inspect the created issue/PR payload, ensure the content and labels are correct, and that the target repository actor is correct.

5) Approve repository-wide automation (optional)
- After at least one successful manual verification, a maintainer may set `ALLOW_NOTIFICATIONS=1` as a repository secret and remove `--dry-run` from the workflow invocation.
- Recommended: enable automation for a narrow workflow only (e.g., `auto_update_baseline.yml`) and keep the flag `--enable-issues`/`--enable-slack` controlled by a workflow input to be toggled per dispatch.

6) Post‑enable verification and monitoring
- Keep the first few runs under close review. Inspect the produced artifacts in `outputs/ci-artifacts` and the created remote objects (issues/PRs) for correctness.
- Check audit logs (GitHub Actions run log + token usage) and Slack channel confirmation messages.

Rollback plan
- Remove or set `ALLOW_NOTIFICATIONS` secret to `0` in repository settings to immediately disable remote actions.

Required fields & flags (summary)
- CLI flags:
  - `--input-file PATH` : read precomputed guardrail JSON from PATH
  - `--enable-issues` : allow attempting to create a GitHub issue (off by default)
  - `--enable-slack` : allow attempting to post to Slack via `SLACK_WEBHOOK` (off by default)
  - `--dry-run` : do not perform any remote actions (prints what would happen)
- Environment: `ALLOW_NOTIFICATIONS=1` required for any remote action to proceed

Minimal safe examples

- Local dry-run (no network calls):

```bash
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-20250920-021225.json --dry-run
```

- Manual, controlled enable (one-off):

```bash
export ALLOW_NOTIFICATIONS=1
export SLACK_WEBHOOK='https://hooks.slack.com/services/..'
export GITHUB_TOKEN='__EXAMPLE_GITHUB_TOKEN__'
export GITHUB_REPOSITORY='owner/repo'
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-20250920-021225.json --enable-issues --enable-slack
```

Security and operational notes
- Do not set `ALLOW_NOTIFICATIONS=1` on public or untrusted runners without review.
- Do not store long-lived access tokens in code. Use repository secrets and rotate them regularly.
- Prefer the Actions-provided `GITHUB_TOKEN` where possible and restrict a bot token's scope to the minimum required actions.
- Keep notifier code small and reviewable; prefer short JSON payloads for issue bodies to simplify audits.

Where to change CI behavior
- Workflows that currently call the notifier may pass `--dry-run` by default. To enable remote actions in CI, update the workflow invocation to remove `--dry-run` and ensure `ALLOW_NOTIFICATIONS` is present as a repo secret. Example snippet (workflow dispatch input recommended):

```yaml
# ... in your workflow step
run: |
  python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure.json --enable-issues --enable-slack
env:
  ALLOW_NOTIFICATIONS: ${{ secrets.ALLOW_NOTIFICATIONS }}
  SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Checklist before flipping to automation
- At least one manual verification run completed and reviewed
- Baseline tolerances documented and agreed
- Secrets added and reviewed (ALLOW_NOTIFICATIONS, optional SLACK_WEBHOOK)
- Workflow inputs configured so remote actions remain opt-in per run
