# Smoke test for train_baseline.py (offline, stdlib only)
import os
import sys
import json
import pathlib
import subprocess


def main():
    dataset_path = "data/dataset_SMOKE.parquet"
    if not os.path.exists(dataset_path):
        dataset_path = "data/dataset_SMOKE.pkl"
        if not os.path.exists(dataset_path):
            # SMOKE dataset is optional in CI runs; treat missing dataset as skip (exit 0)
            print("SMOKE dataset not found. Skipping smoke test.")
            sys.exit(0)
    out_json = "docs/summaries/TRAIN_SUMMARY_SMOKE.json"
    model_tag = "M3_SMOKE_RH3"
    meta_path = f"models/{model_tag}/metadata.json"
    # Remove old outputs
    for p in [out_json, meta_path]:
        try:
            os.remove(p)
        except Exception:
            pass
    # Run training
    cmd = [
        sys.executable,
        "scripts/training/train_baseline.py",
        "--dataset",
        dataset_path,
        "--label-name",
        "label_R_H3_pct",
        "--features",
        "f_ret_1,f_ret_3,f_vol_12",
        "--train-from",
        "2025-01-01",
        "--train-to",
        "2025-01-08",
        "--model-tag",
        model_tag,
        "--out-json",
        out_json,
        "--save-model",
        f"models/{model_tag}/model.pkl",
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print("Train runner failed:", result.stderr.decode())
        sys.exit(1)
    # Check summary JSON
    try:
        with open(out_json) as f:
            summary = json.load(f)
        for k in ["run_tag", "train", "model", "metrics"]:
            assert k in summary, f"Missing key {k} in summary"
        for m in ["mae", "mse", "r2", "resid_mean", "resid_std"]:
            v = summary["metrics"].get(m)
            assert v is not None and not (
                isinstance(v, float)
                and (v != v or v == float("inf") or v == float("-inf"))
            ), f"Metric {m} invalid: {v}"
    except Exception as e:
        print(f"Summary JSON check failed: {e}")
        sys.exit(1)
    # Check registry metadata
    try:
        with open(meta_path) as f:
            meta = json.load(f)
        for k in ["model_tag", "label", "features", "train_window"]:
            assert k in meta, f"Missing key {k} in metadata"
    except Exception as e:
        print(f"Metadata check failed: {e}")
        sys.exit(1)
    print(f"TRAIN SMOKE OK: {model_tag}")
    sys.exit(0)


if __name__ == "__main__":
    main()
