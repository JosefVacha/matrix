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
gh secret set AUTOMATION_GH_TOKEN --body "ghp_..." --repo $GITHUB_REPOSITORY
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