# Developer quickstart — run Matrix locally (dry-run)

This short guide helps you run a minimal, reproducible local development flow for the Matrix repo.
It focuses on a fast smoke/dry-run loop so you can iterate while CI runs remotely.

## Goals
- Create a small SMOKE dataset (prefer Parquet, fallback to pickle)
- Run a safe local trainer flow (summary JSON + metadata) without touching live systems
- Run a lightweight E2E smoke test

## 1) Prepare a Python virtualenv
Use a virtual environment to avoid interfering with system Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

If you want the full developer environment (recommended for tests and Parquet support):

```bash
python -m pip install -r requirements-dev.txt
```

Note: `requirements-dev.txt` contains `pandas`, `numpy`, and `fastparquet`. Installing `pyarrow` is optional and may require additional system packages (CMake, build-essential) and is heavier on CI.

## 2) Generate a SMOKE dataset
The repo provides `scripts/qa/generate_smoke_dataset.py`. It prefers `pandas`/`numpy` and Parquet but has a stdlib fallback that writes a pickled list-of-dicts.

Quick run (uses stdlib fallback if pandas missing):

```bash
python -m scripts.qa.generate_smoke_dataset
# Default output: data/dataset_SMOKE.parquet or data/dataset_SMOKE.pkl (fallback)
```

You can pass start/end dates by editing the script or (future) via CLI flags if provided.

## 3) Run the smoke/dry-run runner
We added a lightweight runner that orchestrates dataset generation and training summary.

```bash
python3 scripts/run_smoke_local.py \
  --dataset data/dataset_SMOKE.parquet \
  --label-name label_R_H3_pct \
  --train-from 2025-01-01 \
  --train-to 2025-01-08 \
  --model-tag LOCAL_SMOKE \
  --out-json outputs/smoke_summary.json \
  --no-save-model
```

- If `pandas` is installed, the runner will invoke `scripts/training/train_baseline.py` to compute metrics and write summary JSON.
- If `pandas` isn't installed, the runner uses a stdlib summary (quick placeholder) and writes `outputs/smoke_summary.json` plus `models/<tag>/metadata.json`.

## 4) Run the integration smoke test (pytest)
Install pytest in your venv (if you installed `requirements-dev.txt` it may already be present):

```bash
python -m pip install pytest
pytest -q tests/test_e2e_smoke.py::test_e2e_smoke -q
```

If you don't want to install `pytest`, you can run the runner manually and inspect `outputs/smoke_summary.json`.

## 5) Troubleshooting
- Parquet vs Pickle:
  - The generator prefers Parquet but falls back to a pickle when Parquet engines aren't available.
  - If you need Parquet locally, install `fastparquet` (lightweight) or `pyarrow` (may require system packages).

- Installing `pyarrow` errors (native build):
  - On Linux you may need `cmake` and `build-essential`.
  - Prefer `fastparquet` when CI runners don't provide Arrow C libraries.

- `pytest` missing: install it into your venv (`python -m pip install pytest`).

## 6) Quick checklist for a fresh clone
1. git clone ...
2. python3 -m venv .venv && source .venv/bin/activate
3. python -m pip install --upgrade pip
4. python -m pip install -r requirements-dev.txt  # optional for full env
5. python -m scripts.qa.generate_smoke_dataset
6. python scripts/run_smoke_local.py --out-json outputs/smoke_summary.json

## 7) Notes and next improvements
- Consider adding a `--start/--end` CLI for `generate_smoke_dataset.py` for easier automation.
- Consider adding a small `Makefile` or `scripts/dev/run_all.sh` to automate the setup and run steps.

If you want, I can now:
- create `docs/DEV_RUN.md` (done), and
- add a `Makefile` or `scripts/dev/run_all.sh` to automate steps 1–4, or
- add explicit CLI flags to the generator for start/end dates.
