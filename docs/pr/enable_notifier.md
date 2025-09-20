# Draft PR: Enable Notifier (Checklist)

This is a draft PR template that maintainers can use when they decide to enable the notifier for automated baseline proposals.

Title: chore(ci): enable notifier for baseline proposals (experimental)

Body:
- Purpose: enable CI to push proposed baseline updates automatically when metrics improve.
- Safety: notifier is safe-by-default and requires `ALLOW_NOTIFICATIONS=1` to perform remote writes.
- Artifacts: the workflow will upload `outputs/paper_trade_metrics.json` and `outputs/paper_trade_report.json` on run.

Checklist (maintainers must verify):
- [ ] At least one dry-run was executed and reviewed
- [ ] `ALLOW_NOTIFICATIONS` secret has been added (value `1`) for the repository
- [ ] `SLACK_WEBHOOK` (optional) is present and verified
- [ ] `GITHUB_TOKEN` usage reviewed (Actions default token is used)
- [ ] A small test run with `allow_push=true` has been observed and the resulting PR was manually checked and merged

Notes:
- To disable automation immediately, delete `ALLOW_NOTIFICATIONS` or set it to `0`.
