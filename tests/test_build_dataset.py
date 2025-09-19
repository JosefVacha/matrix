#!/usr/bin/env python3
"""
Smoke test for MATRIX dataset builder (offline, pandas/numpy only).
Usage: python -m tests.test_build_dataset
"""
import subprocess
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import os

def main():
    sample_csv = "docs/REPORTS/RAW/OHLCV_SAMPLE.csv"
    out_parquet = Path("data/dataset_SMOKE.parquet")
    out_pickle = out_parquet.with_suffix(".pkl")
    sidecar_json = out_parquet.with_suffix(".json")
    # Remove old files
    for p in [out_parquet, out_pickle, sidecar_json]:
        try:
            os.remove(p)
        except Exception:
            pass
    # Run builder
    cmd = [sys.executable, "scripts/training/build_dataset.py",
           "--ohlcv", sample_csv,
           "--timeframe", "5m",
           "--H", "3",
           "--transform", "pct",
           "--windows", "1,3",
           "--out", str(out_parquet)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Builder failed:", result.stderr)
        sys.exit(1)
    # Try to load Parquet, fallback to Pickle
    try:
        df = pd.read_parquet(out_parquet)
        artifact = out_parquet
    except Exception:
        try:
            df = pd.read_pickle(out_pickle)
            artifact = out_pickle
        except Exception:
            print("Could not load output artifact.")
            sys.exit(1)
    # Assertions
    expected_features = ["f_ret_1", "f_ret_3"]
    for feat in expected_features:
        if feat not in df.columns:
            print(f"Missing feature column: {feat}")
            sys.exit(1)
    label_col = "label_R_H3_pct"
    if label_col not in df.columns:
        print(f"Missing label column: {label_col}")
        sys.exit(1)
    if len(df) < 3:
        print("Dataset too short after warmup drop.")
        sys.exit(1)
    if df.isna().sum().sum() != 0:
        print("NaN values present after warmup drop.")
        sys.exit(1)
    if not df.index.is_monotonic_increasing:
        print("Index not monotonic increasing.")
        sys.exit(1)
    if not (df.index.tz and str(df.index.tz) == "UTC"):
        print("Index not tz-aware UTC.")
        sys.exit(1)
    # Sidecar JSON
    if not sidecar_json.exists():
        print("Missing sidecar JSON.")
        sys.exit(1)
    print(f"SMOKE OK {artifact}")
    sys.exit(0)

if __name__ == "__main__":
    main()
