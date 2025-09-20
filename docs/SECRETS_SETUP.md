# Secrets setup (maintainers)

This document explains the repository secrets that the guardrail notifier can use and recommended minimal scopes.

Overview
- The notifier in `scripts/qa/notify_guardrail_failure.py` prefers to use the GitHub REST API to create a lightweight issue when guardrails fail. It will fall back to the `gh` CLI if the token is not present. It can also post a short message to a Slack channel when a `SLACK_WEBHOOK` is configured.

Recommended secrets

1) GITHUB_TOKEN (default Actions token)
- Provided automatically in GitHub Actions as `secrets.GITHUB_TOKEN`. This token is sufficient for creating issues from workflow runs (when the job has `permissions: issues: write`).
- Minimal required permission: issues: write. This is granted by default for workflow jobs that set the permission.
- Usage notes: No additional manual secret required if Actions workflow grants the permission. If you want a separate automation token, create a PAT with `repo` scope (minimal: `public_repo` or `repo` depending on repo visibility) and store it as `AUTOMATION_GH_TOKEN`.

2) SLACK_WEBHOOK (optional)
- If set, notifier will post a short JSON message to the webhook URL describing the guardrail failure and a link to artifact(s).
- No special GitHub scopes required.
- Keep this secret limited to the channel used for dev alerts. Rotate periodically.

3) AUTOMATION_GH_TOKEN (optional)
- If you prefer to separate automation from the default `GITHUB_TOKEN`, create a minimal-scope GitHub Personal Access Token (PAT) and store it as `AUTOMATION_GH_TOKEN`.
- Minimal scopes: `repo:public_repo` (for public repos) or `repo` (if private). If you only need to create issues, `issues:write` is sufficient where supported by the PAT UI.

Workflow guidance
- In `.github/workflows/smoke-validators.yml`, ensure the job sets the required permission if you rely on `GITHUB_TOKEN` to create issues:
  permissions:
    issues: write
- The workflow already includes a simulate-notifier job which runs non-blocking; you can test the notifier by triggering the manual dispatch workflow added in `.github/workflows/simulate-notifier-dispatch.yml`.

Security recommendations
- Prefer the built-in `GITHUB_TOKEN` for Actions — it is rotated automatically and least privilege for the workflow.
- If you must use a PAT (`AUTOMATION_GH_TOKEN`), create a token with only the scopes you need and store it as a secret.
- Use `SLACK_WEBHOOK` only for non-sensitive channels and avoid posting full artifacts (notifier writes artifact files into `outputs/` and posts only a short summary link).

Maintainer checklist for enabling notifications
- [ ] Ensure `permissions: issues: write` is set for the validators job in the workflow.
- [ ] Add `SLACK_WEBHOOK` secret if you want Slack notifications.
- [ ] Optionally add `AUTOMATION_GH_TOKEN` if you prefer a non-Actions token for issue creation.

If you want, I can add a small workflow snippet to the README showing how to add the secrets via the GitHub UI or the `gh` CLI.