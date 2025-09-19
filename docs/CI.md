## Continuous Integration — Smoke & Validators (offline)

What this workflow runs
- validators job (stdlib-only):
  - H-consistency check: `scripts/qa/check_H_consistency.py`.
  - Model metadata schema validation: `scripts/qa/validate_model_metadata.py` against `docs/schemas/model_metadata.schema.json`.
- smoke job (optional): runs `tests/test_train_baseline.py` if the file exists.

When it runs
- On Pull Requests targeting `main` and on pushes to `main`.

Offline policy
- No network or package downloads are required by default. The workflow uses only Python from the Actions runner and scripts that rely on the standard library. If a job requires external packages in future, update this doc and the workflow with cached, pinned installers.

How to read job logs
- Jobs are named `validators` and `smoke` and run for Python 3.11 and 3.12 (matrix).
- Key steps are printed as separate steps in the Actions UI; failure will show the failing step and the script stderr.
- For validators:
  - `H-consistency (stdlib)` runs first; exit code 0 = OK.
  - `Model registry metadata validate (stdlib)` runs example validation (if present) and then known model metadata files (e.g., `models/BASELINE_LIN_H3/metadata.json`) if present. A non-zero exit code indicates a schema violation.

Notes and follow-ups
- To enable a broader smoke that requires pandas/numpy, update the workflow with an explicit install step and a pinned dependency list. Keep the default fast validators stdlib-first.
