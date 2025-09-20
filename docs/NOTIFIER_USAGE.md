# Notifier usage and safety

The notifier script `scripts/qa/notify_guardrail_failure.py` is intentionally conservative. It always writes a local artifact and only performs remote actions when explicitly allowed.

Flags:
- `--input-file PATH` : read precomputed guardrail JSON from PATH
- `--enable-issues` : allow attempting to create a GitHub issue (off by default)
- `--enable-slack` : allow attempting to post to Slack via `SLACK_WEBHOOK` (off by default)
- `--dry-run` : do not perform any remote actions (prints what would happen)

Environment:
- `ALLOW_NOTIFICATIONS=1` : required for any remote action to proceed (must be set in the environment)
- `GITHUB_TOKEN` and `GITHUB_REPOSITORY` : used by REST API fallback when creating issues
- `SLACK_WEBHOOK` : optional Slack webhook URL to post notifications

Safe examples:

- Local dry-run (no network calls):

```
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-20250920-021225.json --dry-run
```

- Enable issues and Slack in a controlled environment (must export ALLOW_NOTIFICATIONS=1):

```
export ALLOW_NOTIFICATIONS=1
export SLACK_WEBHOOK='https://hooks.slack.com/services/..'
export GITHUB_TOKEN='ghp_...'
export GITHUB_REPOSITORY='owner/repo'
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-20250920-021225.json --enable-issues --enable-slack
```

Notes:
- Do not set `ALLOW_NOTIFICATIONS=1` on public or untrusted runners without review.
- The script always writes a local artifact; use artifacts and `outputs/ci-artifacts` to inspect failures before enabling notifications.
