# PR Maintainer Guide — Guardrails & Notifier

This short guide helps maintainers review PRs that touch guardrails, simulate notifier runs, and configure repository secrets.

1) Trigger the simulate-notifier workflow

- The repository includes a non-blocking job `simulate-notifier` in `.github/workflows/smoke-validators.yml` that runs only on the `chore/qa-guardrails` branch.
- There's also a manual workflow dispatch at `.github/workflows/simulate-notifier-dispatch.yml` you can trigger from the Actions UI.

To trigger manually via `gh` CLI:

```bash
# trigger a manual workflow (replace <owner>/<repo> and workflow id as needed)
gh workflow run simulate-notifier-dispatch.yml --repo $GITHUB_REPOSITORY
```

Or from the Actions UI:
- Open the `Actions` tab → choose `simulate-notifier-dispatch` → `Run workflow` → submit.

2) Add repository secrets (if you want notifications)

- GITHUB_TOKEN is provided automatically for Actions. Ensure the validators job sets `permissions: issues: write` (already set).
- OPTIONAL: Add `SLACK_WEBHOOK` as a secret to post short notifications to Slack.
- OPTIONAL: Create `AUTOMATION_GH_TOKEN` (PAT) with minimal scopes if you don't want to use `GITHUB_TOKEN`.

Via GitHub UI: Settings → Secrets → Actions → New repository secret.

Via `gh` CLI (example):

```bash
# add slack webhook secret
gh secret set SLACK_WEBHOOK --body "https://hooks.slack.com/services/ABC/DEF/GHI" --repo $GITHUB_REPOSITORY

# add automation token
gh secret set AUTOMATION_GH_TOKEN --body "__PASTE_YOUR_PAT_HERE__" --repo $GITHUB_REPOSITORY
```

3) Run guardrails locally

```bash
python3 scripts/qa/check_copilot_guardrails.py --json --output-file outputs/guardrail_check.json
cat outputs/guardrail_check.json
```

4) Triage outputs

- Artifacts are uploaded by workflows (simulate-notifier) as `guardrail-outputs` and include `outputs/` with notifier artifacts (if any).
- If notifier created an issue, it will be visible in the repo Issues list.

5) Quick checklist for approving changes

- Ensure `copilot-instructions.md` still contains the mandatory two-line preface and the Czech mandatory sentence.
- Ensure `Knowledge/REPLY_TEMPLATES.md` contains the Czech template reference.
- Run guardrail locally and confirm `language_ok: true` before merging.

If you'd like, I can add a tiny GitHub Actions badge or a scripted `Makefile` target to make local guardrail runs even easier.

## Auto-notify policy (recommended)

By default, automatic notifications are disabled. This repository follows a conservative policy:

- The notifier will always write a local artifact, but will not create issues or post to Slack unless explicitly allowed.
- To enable remote notifications in CI, a maintainer must:
	1. Add the required secrets (`SLACK_WEBHOOK`, and/or `AUTOMATION_GH_TOKEN`) in the repository settings.
	2. Set `ALLOW_NOTIFICATIONS=1` in the job environment (or as a repository secret) — this acts as a second guardrail.
	3. Ensure the job has `permissions: issues: write` if you want to use the built-in `GITHUB_TOKEN`.

Automation & ALLOW_NOTIFICATIONS

If a workflow may perform remote writes (create branches, push changes, open PRs or issues), it is gated by the
`ALLOW_NOTIFICATIONS` safety flag. This flag must be set to `1` in the workflow environment for the workflow to perform
network writes; otherwise the workflow runs in dry-run mode and will only output the proposed changes.

Usage example (manual dispatch):

	- In the Actions workflow dispatch or when running locally, set `ALLOW_NOTIFICATIONS=1` to allow remote writes.
	- Prefer to review the dry-run output before enabling `ALLOW_NOTIFICATIONS` for the first run.

This reduces accidental pushes from CI runs and makes baseline updates explicit and auditable.

This two-step approach (explicit flags + ALLOW_NOTIFICATIONS) reduces the risk of accidental notifications from local runs or forks. See `docs/NOTIFIER_USAGE.md` for usage examples and safety notes.


## Pre-commit (recommended)

We recommend installing `pre-commit` locally so contributors get automatic formatting and linting.

Install:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pre-commit
pre-commit install
# optional: run on all files once
pre-commit run --all-files
```

The repository includes a `.pre-commit-config.yaml` with `black`, `isort`, `flake8` and a few basic hooks.
