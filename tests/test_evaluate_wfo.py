#!/usr/bin/env python3
"""
Smoke test for offline WFO evaluation runner.
Usage: python -m tests.test_evaluate_wfo
"""

import subprocess
import sys
import json
from pathlib import Path


def main():
    dataset = Path("data/dataset_SMOKE.parquet")
    if not dataset.exists():
        dataset = Path("data/dataset_SMOKE.pkl")
    if not dataset.exists():
        print("Missing dataset_SMOKE. Run ds-build-smoke first.")
        sys.exit(1)
    out_json = Path("docs/summaries/WFO_SUMMARY_SMOKE.json")
    out_md = Path("docs/summaries/WFO_SUMMARY_SMOKE.md")
    cmd = [
        sys.executable,
        "scripts/training/evaluate_wfo.py",
        "--dataset",
        str(dataset),
        "--label-name",
        "label_R_H3_pct",
        "--from",
        "2025-01-01",
        "--to",
        "2025-01-10",
        "--block-days",
        "2",
        "--gap-days",
        "0",
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
        "--run-tag",
        "SMOKE_2D",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("WFO runner failed:", result.stderr)
        sys.exit(1)
    if not out_json.exists():
        print("Missing output JSON.")
        sys.exit(1)
    with open(out_json) as f:
        data = json.load(f)
    for k in ["run_tag", "label", "params", "blocks"]:
        if k not in data:
            print(f"Missing key: {k}")
            sys.exit(1)
    if not data["blocks"] or len(data["blocks"]) == 0:
        print("No blocks in output.")
        sys.exit(1)
    for b in data["blocks"]:
        for k in ["train_from", "train_to", "test_from", "test_to", "n", "mean_R"]:
            if k not in b:
                print(f"Missing block key: {k}")
                sys.exit(1)
            if b[k] is None or (isinstance(b[k], float) and not (b[k] == b[k])):
                print(f"Non-finite value for {k}")
                sys.exit(1)
    if not out_md.exists():
        print("Missing output MD.")
        sys.exit(1)
    with open(out_md) as f:
        header = f.readline()
    expected_cols = [
        "train_from",
        "train_to",
        "test_from",
        "test_to",
        "n",
        "nan_ratio",
        "trigger_rate",
        "mean_R",
        "hit_rate",
        "dd_min",
    ]
    if not all(col in header for col in expected_cols):
        print("MD header missing expected columns.")
        sys.exit(1)
    print(f"WFO SMOKE OK: {out_json}")
    sys.exit(0)


if __name__ == "__main__":
    main()
