## Guardrails: usage, JSON schema, and CI integration

This document explains the guardrail orchestration scripts and the JSON output schema produced by `scripts/qa/check_copilot_guardrails.py`.

Quick goals
- Provide a deterministic, machine-readable guardrail check for CI.
- Fail fast in CI when critical items are missing.
- Produce artifacts and optionally notify maintainers when failures occur.

CLI
- Run the guardrail checker (human):

  python3 scripts/qa/check_copilot_guardrails.py

- Machine-readable output (JSON):

  python3 scripts/qa/check_copilot_guardrails.py --json

- Notifier (writes artifact and creates a GH issue if possible):

  python3 scripts/qa/notify_guardrail_failure.py

  Or provide precomputed guardrail JSON:

  python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/guardrail_failure-2025XXXX-XXXXXX.json

JSON schema (informal)
- The guardrail runner emits a small object with keys (not all keys always present):

- `ok` (bool): overall pass/fail
- `preface_ok` (bool): whether the mandatory pre-reply preface was found in `.github/copilot-instructions.md`
- `missing_critical` (list): critical guardrail filenames or checks missing (CI must fail)
- `conditional_checked` (list): non-critical checks that ran
- `missing_conditionals` (list): conditional checks that failed (warnings)
- `code_fence` / `cli_export` (objects): outputs for specific validators with `code` and `output` fields
- `scopes_detected` (list): environment scopes inferred (e.g., `ci`)

Schema file
- A formal JSON Schema is available at `docs/schemas/guardrail_output.schema.json`.

Quick validation (optional):
- Install jsonschema: `python -m pip install jsonschema`
- Validate a saved JSON output:

  python -c "import json,sys; from jsonschema import validate,RefResolver; print('not implemented sample')"

Exit codes
- 0 — all good
- 1 — guardrail failed (artifact produced if run via notifier)
- 2 — internal error (invalid input file, JSON parse error, unexpected exception)

CI integration notes
- The repository's workflow (`.github/workflows/smoke-validators.yml`) calls the guardrail checker in the `validators` job. Critical failures cause the job to fail.
- The notifier script `scripts/qa/notify_guardrail_failure.py` is intended to be used in the CI failure path (best-effort). If `gh` CLI and `GITHUB_TOKEN` are available in the runner, the notifier will create a GitHub issue referencing the artifact.

Troubleshooting
- If the guardrail checker times out on a subscript, check the `--json` output for errors in the specific validator and re-run the validator locally.
- If `notify_guardrail_failure.py` cannot create an issue, you can create one manually:

  gh issue create --title "Guardrail check failed: repository guardrails" --body-file outputs/guardrail_failure-<ts>.json

Security
- The notifier will only create issues when `GITHUB_TOKEN` is present in the environment. No secrets are printed.

Maintenance
- Keep the `copilot-instructions.md` preface lines in sync with repository policy. The guardrail checker depends on that preface for `preface_ok`.
