#!/usr/bin/env python3
"""
Build reproducible local dataset for MATRIX (offline, pandas/numpy only).
Enforces DATASET_SCHEMA.md, LABELS.md, TRAINING_PROTOCOL.md, CONTRACTS.md, hooks.py docstrings.
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

FEATURES = ["f_ret_1", "f_ret_3", "f_ret_12", "f_hl_range", "f_oc_range", "f_vol_z"]

LABEL_PATTERN = "label_R_H{H}_{transform}"


def robust_zscore(vol):
    med = np.median(vol)
    q75, q25 = np.percentile(vol, [75, 25])
    iqr = q75 - q25
    if iqr == 0:
        return np.zeros_like(vol)
    return (vol - med) / iqr


def main():
    parser = argparse.ArgumentParser(description="Build MATRIX dataset from OHLCV CSV.")
    parser.add_argument("--ohlcv", required=True)
    parser.add_argument("--timeframe", required=True)
    parser.add_argument("--H", type=int, required=True)
    parser.add_argument("--transform", choices=["pct", "log"], required=True)
    parser.add_argument("--windows", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--sidecar-json", default=None)
    args = parser.parse_args()
    windows = [int(w) for w in args.windows.split(",") if w.strip()]
    ohlcv_path = Path(args.ohlcv)
    out_path = Path(args.out)
    sidecar_path = (
        Path(args.sidecar_json) if args.sidecar_json else out_path.with_suffix(".json")
    )
    # Load CSV
    df = pd.read_csv(ohlcv_path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], utc=True)
        df.set_index("date", inplace=True)
    elif "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df.set_index("datetime", inplace=True)
    else:
        raise ValueError("CSV must have 'date' or 'datetime' column.")
    df = df.sort_index()
    if not df.index.is_monotonic_increasing:
        raise ValueError("Index must be monotonic increasing.")
    # Check required columns
    for col in ["open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # Compute features
    for w in windows:
        if w not in [1, 3, 12]:
            continue
        if args.transform == "pct":
            df[f"f_ret_{w}"] = df["close"].pct_change(w)
        else:
            df[f"f_ret_{w}"] = np.log(df["close"] / df["close"].shift(w))
    df["f_hl_range"] = (df["high"] - df["low"]) / df["close"]
    df["f_oc_range"] = (df["close"] - df["open"]) / df["open"]
    df["f_vol_z"] = robust_zscore(df["volume"].values)
    # Compute label
    H = args.H
    if args.transform == "pct":
        label = df["close"].shift(-H) / df["close"] - 1
    else:
        label = np.log(df["close"].shift(-H) / df["close"])
    label_name = LABEL_PATTERN.format(H=H, transform=args.transform)
    df[label_name] = label
    # Warmup drop
    warmup = max(max(windows), H)
    df = df.iloc[warmup:]
    df = df[:-H] if H > 0 else df
    # Select columns
    keep_cols = [f"f_ret_{w}" for w in windows if w in [1, 3, 12]] + [
        "f_hl_range",
        "f_oc_range",
        "f_vol_z",
        label_name,
    ]
    df = df[keep_cols]
    # Drop NaN
    df = df.dropna()
    # Ensure UTC tz-aware index
    if not (df.index.tz and str(df.index.tz) == "UTC"):
        df.index = df.index.tz_localize("UTC")
    # Output
    n_rows = len(df)
    started_at = datetime.utcnow().isoformat() + "Z"
    try:
        df.to_parquet(out_path)
        out_fmt = "parquet"
    except Exception:
        out_path = out_path.with_suffix(".pkl")
        df.to_pickle(out_path)
        out_fmt = "pickle"
    finished_at = datetime.utcnow().isoformat() + "Z"
    summary = {
        "n_rows": n_rows,
        "n_features": 6,
        "label_name": label_name,
        "label_H": H,
        "windows": windows,
        "dropped_warmup": warmup,
        "timeframe": args.timeframe,
        "started_at": started_at,
        "finished_at": finished_at,
        "sha_note": "binary artifacts are not tracked",
        "schema": "right-aligned",
    }
    with open(sidecar_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Built dataset: {out_path} ({out_fmt}), rows={n_rows}, label={label_name}")
    exit(0)


if __name__ == "__main__":
    main()
