# Notifier and failure artifact guide

This short guide explains how to safely enable and test the guardrail notifier that runs on CI failure.

Overview
- When guardrails fail, CI runs `scripts/qa/notify_guardrail_failure.py` (best-effort). The script writes `outputs/guardrail_failure-<ts>.json` and will attempt to create a GitHub issue (via REST) or post to Slack (webhook) if configured.

Security-first configuration
- GitHub issue creation:
  - The workflow passes `GITHUB_TOKEN` and `GITHUB_REPOSITORY` to the notifier step.
  - By default `GITHUB_TOKEN` from Actions is suitable for the repo; if you prefer a dedicated token, create one with minimal scope (issues: create only) and add it as a secret (e.g. `AUTOMATION_TOKEN`).
  - If using a custom token, update the workflow env to pass it under `GITHUB_TOKEN` or modify the notifier to read a different secret name.

- Slack notifications:
  - Add the incoming webhook URL as the repo secret `SLACK_WEBHOOK` if you want Slack messages.
  - The notifier will try to POST a short message with the artifact link; the webhook is optional.

How to enable (recommended safe steps)
1) In GitHub repo settings → Secrets → Actions, add `SLACK_WEBHOOK` (optional).
2) Review the notifier code (`scripts/qa/notify_guardrail_failure.py`) and confirm the issue creation pathway uses minimal scopes.
3) Run CI on the PR branch and inspect the `validators` job — if it fails, the notifier will create `outputs/guardrail_failure-<ts>.json` and attempt notifications.

How to interpret the artifact
- The artifact JSON contains keys such as `missing_critical`, `missing_conditionals`, `preface_ok`, `language_ok`, `ok`, and `code_fence`/`cli_export` validator outputs.
- Common triage steps:
  1) Download the artifact from the failed job logs or workspace `outputs/`.
 2) Open the JSON and inspect `missing_critical` and `language_ok` first — these explain immediate policy failures.
 3) If `code_fence` or `cli_export` have non-zero codes, inspect their `output` text for validator errors.

Testing locally
- Run the guardrail checker locally to reproduce:

  python3 scripts/qa/check_copilot_guardrails.py --json

- Simulate a failure and run the notifier locally (writes artifact):

  python3 scripts/qa/notify_guardrail_failure.py --input-file tests/fixtures/failing_guardrail.json

  (Create `tests/fixtures/failing_guardrail.json` with a minimal failing structure if needed.)

Rollback and safety
- The notifier is best-effort and non-destructive. It will not modify repo files; it only writes artifacts and posts to external endpoints when configured.

Questions or changes
- If you want me to update the workflow to use a different secret name, add a sample `workflow` snippet to this guide, or create a PR that updates the settings page, tell me which option and I'll implement it.
