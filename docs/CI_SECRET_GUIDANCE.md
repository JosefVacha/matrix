CI secrets guidance

This repository uses GitHub Actions. Follow these minimal guidelines for secrets:

- Prefer the Actions-provided `GITHUB_TOKEN` for repository-scoped automation. It is short-lived and rotated automatically.
- If you need a PAT for automation (e.g., `AUTOMATION_GH_TOKEN`), create a token with the least privilege required. For public repositories, prefer `public_repo` scope; for private repos, restrict scopes as narrowly as possible.
- Never hard-code secrets in code, configs, or docs. Use repository secrets (Settings → Secrets & variables → Actions) and reference them using `${{ secrets.NAME }}` in workflows.
- Use `ALLOW_NOTIFICATIONS=1` as a gate for workflows that perform network writes (creating PRs/issues). The default behavior is dry-run to avoid accidental writes.
- Auditing: periodically review repository secrets and rotate tokens at least quarterly or immediately if an exposure is suspected.

CI job requirements

- The `smoke` and `validators` jobs should set `permissions: issues: write` only if they need to create issues. Prefer running detectors/reporters without issues permission.
- Pre-commit / detect-secrets should run on PRs and fail if new secrets are introduced.

Mitigation steps if a secret is found in git history

1. Immediately rotate the exposed credential.
2. Remove the secret from history using `git filter-repo` or BFG and force-push to main branches (coordinate with other contributors).
3. Revoke and recreate any tokens/keys associated, and audit usage logs for suspicious activity.

Local developer quick-start

- Use the Makefile targets to run checks locally:
	- `make precommit` — run configured pre-commit hooks
	- `make detect-secrets-scan` — run a detect-secrets scan using the repository baseline if present

- To set up a quick virtualenv for development:
	- `make venv`
