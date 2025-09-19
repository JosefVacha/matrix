#!/usr/bin/env python3
"""
Offline WFO evaluation runner for MATRIX (docs-first, pandas/numpy only).
Usage:
  python scripts/training/evaluate_wfo.py \
    --dataset data/dataset_SMOKE.parquet \
    --label-name label_R_H3_pct \
    --from 2025-01-01 --to 2025-01-31 \
    --block-days 3 --gap-days 0 \
    --out-json docs/summaries/WFO_SUMMARY_SAMPLE.json \
    --out-md docs/summaries/WFO_SUMMARY_SAMPLE.md \
    --run-tag SAMPLE_3D
"""

import argparse, sys, json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def parse_args():
    p = argparse.ArgumentParser(description="Offline WFO evaluation runner for MATRIX.")
    p.add_argument("--dataset", required=True)
    p.add_argument("--label-name", required=True)
    p.add_argument("--from", dest="from_date", required=True)
    p.add_argument("--to", dest="to_date", required=True)
    p.add_argument("--block-days", type=int, required=True)
    p.add_argument("--gap-days", type=int, default=0)
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-md", required=True)
    p.add_argument("--run-tag", required=True)
    return p.parse_args()


def load_dataset(path):
    try:
        df = pd.read_parquet(path)
    except Exception:
        df = pd.read_pickle(Path(path).with_suffix(".pkl"))
    if not df.index.is_monotonic_increasing:
        raise ValueError("Index must be monotonic increasing.")
    if not (df.index.tz and str(df.index.tz) == "UTC"):
        df.index = df.index.tz_localize("UTC")
    return df


def build_blocks(df, from_date, to_date, block_days, gap_days):
    blocks = []
    dt_from = pd.Timestamp(from_date).tz_localize("UTC")
    dt_to = pd.Timestamp(to_date).tz_localize("UTC")
    cur = dt_from
    while cur < dt_to:
        test_from = cur
        test_to = cur + timedelta(days=block_days)
        train_to = test_from - pd.Timedelta(minutes=5)
        train_from = (
            df.index[df.index < train_to][0]
            if len(df.index[df.index < train_to]) > 0
            else train_to
        )
        blocks.append(
            {
                "train_from": str(train_from),
                "train_to": str(train_to),
                "test_from": str(test_from),
                "test_to": str(test_to),
            }
        )
        cur = test_to + timedelta(days=gap_days)
    return blocks


def block_metrics(df, label_col, test_from, test_to):
    block = df.loc[(df.index >= test_from) & (df.index < test_to)]
    n = len(block)
    if n == 0:
        return None
    nan_ratio = block.isna().sum().sum() / (n * len(block.columns))
    label = block[label_col]
    trigger_rate = np.mean(label > 0)
    mean_R = np.mean(label)
    hit_rate = np.mean(label > 0)
    cum_label = label.cumsum()
    dd_min = float((cum_label.cummax() - cum_label).min())
    return {
        "n": n,
        "nan_ratio": float(nan_ratio),
        "trigger_rate": float(trigger_rate),
        "mean_R": float(mean_R),
        "hit_rate": float(hit_rate),
        "dd_min": dd_min,
    }


def main():
    args = parse_args()
    df = load_dataset(args.dataset)
    label_col = args.label_name
    if label_col not in df.columns:
        print(f"Label column {label_col} not found.", file=sys.stderr)
        sys.exit(1)
    blocks_plan = build_blocks(
        df, args.from_date, args.to_date, args.block_days, args.gap_days
    )
    results = []
    for b in blocks_plan:
        m = block_metrics(df, label_col, b["test_from"], b["test_to"])
        if m is None:
            continue
        b.update(m)
        results.append(b)
    if not results:
        print("No valid blocks found.", file=sys.stderr)
        sys.exit(1)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    summary = {
        "run_tag": args.run_tag,
        "label": label_col,
        "timeframe": "5m",
        "params": {
            "block_days": args.block_days,
            "gap_days": args.gap_days,
            "from": args.from_date,
            "to": args.to_date,
        },
        "blocks": results,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)
    # Markdown table
    md = [
        "| train_from | train_to | test_from | test_to | n | nan_ratio | trigger_rate | mean_R | hit_rate | dd_min |",
        "|------------|----------|-----------|---------|---|-----------|-------------|--------|----------|--------|",
    ]
    for b in results:
        md.append(
            f"| {b['train_from']} | {b['train_to']} | {b['test_from']} | {b['test_to']} | {b['n']} | {b['nan_ratio']:.4f} | {b['trigger_rate']:.4f} | {b['mean_R']:.6f} | {b['hit_rate']:.4f} | {b['dd_min']:.6f} |"
        )
    md.append("\n**Provenance:**")
    md.append(
        f"run_tag: {args.run_tag}, label: {label_col}, params: {json.dumps(summary['params'])}"
    )
    with open(out_md, "w") as f:
        f.write("\n".join(md))
    print(f"WFO evaluation complete: {out_json} {out_md}")
    sys.exit(0)


if __name__ == "__main__":
    main()
