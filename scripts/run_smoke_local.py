#!/usr/bin/env python3
"""Lightweight local runner for smoke/dev verification.

Flow:
 - ensure dataset exists (call generator)
 - call trainer if pandas available, otherwise run a lightweight, stdlib-only training summary
 - write summary JSON and registry metadata under models/<model_tag>/metadata.json

This runner is intended for fast local iteration without requiring full dev deps.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import datetime


def call_generator(path: str, start: str, end: str):
    # import and call the generator function from scripts.qa
    try:
        from scripts.qa.generate_smoke_dataset import generate

        out = generate(path, start, end)
        return out
    except Exception:
        # If import fails, try module mode
        import subprocess

        cmd = [sys.executable, "-m", "scripts.qa.generate_smoke_dataset"]
        subprocess.check_call(cmd)
        return pathlib.Path(path)


def stdlib_summarize(
    pkl_path: pathlib.Path,
    model_tag: str,
    label_name: str,
    start: str,
    end: str,
    out_json: pathlib.Path,
):
    import pickle
    import statistics

    with pkl_path.open("rb") as fh:
        rows = pickle.load(fh)

    # rows: list of dicts with keys including label_name
    labels = [r[label_name] for r in rows if label_name in r]
    if len(labels) == 0:
        print("No labels found in fallback dataset", file=sys.stderr)
        sys.exit(1)

    # simple metrics
    # Instead compute simple stats on label itself as a placeholder
    mean = statistics.mean(labels)
    mae = statistics.mean([abs(v - mean) for v in labels])
    mse = statistics.mean([(v - mean) ** 2 for v in labels])
    # r2 not meaningful here
    metrics = {"mae": mae, "mse": mse, "r2": None, "resid_mean": 0.0, "resid_std": 0.0}

    summary = {
        "run_tag": model_tag,
        "label": label_name,
        "features": [k for k in rows[0].keys() if k.startswith("f_")],
        "train": {"from": start, "to": end, "n": len(rows)},
        "model": {"type": "fallback", "note": "stdlib summary"},
        "metrics": metrics,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w") as fh:
        json.dump(summary, fh, indent=2)

    # write minimal metadata
    meta_dir = pathlib.Path("models") / model_tag
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "model_tag": model_tag,
        "created_at": summary["created_at"],
        "label": label_name,
        "features": summary["features"],
        "train_window": summary["train"],
        "algo": {"name": "fallback"},
        "artifacts": {"summary": str(out_json)},
        "provenance": {"dataset_path": str(pkl_path), "commit": None},
    }
    with (meta_dir / "metadata.json").open("w") as fh:
        json.dump(meta, fh, indent=2)

    print(f"Wrote summary to {out_json} and metadata to {meta_dir / 'metadata.json'}")


def main():
    parser = argparse.ArgumentParser(description="Local smoke runner")
    parser.add_argument("--dataset", default="data/dataset_SMOKE.parquet")
    parser.add_argument("--label-name", default="label_R_H3_pct")
    parser.add_argument("--train-from", default="2025-01-01")
    parser.add_argument("--train-to", default="2025-01-08")
    parser.add_argument("--model-tag", default="LOCAL_SMOKE")
    parser.add_argument("--out-json", default="outputs/smoke_summary.json")
    parser.add_argument(
        "--no-save-model",
        action="store_true",
        help="Do not attempt to save model artifact",
    )
    args = parser.parse_args()

    dataset_path = pathlib.Path(args.dataset)
    # ensure dataset exists (generator will create pkl fallback if needed)
    out = call_generator(str(dataset_path), args.train_from, args.train_to)
    out_path = pathlib.Path(out)

    # If pandas is available, attempt to call the official trainer; else use stdlib summary
    try:
        # If pandas is present, call the trainer subprocess to preserve behavior
        __import__("pandas")
        import subprocess

        cmd = [
            sys.executable,
            "scripts/training/train_baseline.py",
            "--dataset",
            str(out_path),
            "--label-name",
            args.label_name,
            "--train-from",
            args.train_from,
            "--train-to",
            args.train_to,
            "--model-tag",
            args.model_tag,
            "--out-json",
            args.out_json,
        ]
        # do not pass --save-model unless explicitly allowed
        print("Invoking trainer:", " ".join(cmd))
        subprocess.check_call(cmd)
        print(f"Trainer completed, summary at {args.out_json}")
    except Exception:
        # fallback path
        pkl = out_path.with_suffix(".pkl") if out_path.suffix != ".pkl" else out_path
        stdlib_summarize(
            pkl,
            args.model_tag,
            args.label_name,
            args.train_from,
            args.train_to,
            pathlib.Path(args.out_json),
        )


if __name__ == "__main__":
    main()
