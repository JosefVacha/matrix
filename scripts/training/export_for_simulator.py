"""Export deterministic predictions for the simulator (single CLI).

This lightweight exporter reads `data/latest.parquet` (or .pkl) and writes
`outputs/predictions.csv` with columns date,pair,prediction. It is offline-only
and deterministic for smoke tests.
"""

from __future__ import annotations

import argparse
import pathlib
import csv
import random

import pandas as pd


def _load_dataset(path: str):
    p = pathlib.Path(path)
    if p.suffix == ".parquet":
        return pd.read_parquet(p)
    if p.suffix == ".pkl":
        return pd.read_pickle(p)
    try:
        return pd.read_parquet(p)
    except Exception:
        return pd.read_pickle(p)


def export_predictions(
    dataset_path: str = "data/latest.parquet", output: str = "outputs/predictions.csv"
) -> pathlib.Path:
    p = pathlib.Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)

    data = _load_dataset(dataset_path)

    rows = []
    if hasattr(data, "index"):
        idx = data.index
        if "f_ret_1" in data.columns:
            for dt, val in zip(idx, data["f_ret_1"]):
                pred = float(val) * 0.5
                rows.append((pd_to_iso(dt), "BTC/USD", pred))
        else:
            random.seed(42)
            for dt in idx:
                rows.append((pd_to_iso(dt), "BTC/USD", random.gauss(0, 1)))
    else:
        random.seed(42)
        for r in data:
            d = r.get("date") if isinstance(r, dict) else str(r)
            pred = (
                float(r.get("f_ret_1", 0)) * 0.5
                if isinstance(r, dict) and "f_ret_1" in r
                else random.gauss(0, 1)
            )
            rows.append((d, "BTC/USD", pred))

    with open(p, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["date", "pair", "prediction"])
        for r in rows:
            writer.writerow(r)

    return p


def pd_to_iso(val):
    try:
        return val.isoformat()
    except Exception:
        return str(val)


def _cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/latest.parquet")
    parser.add_argument("--output", default="outputs/predictions.csv")
    args = parser.parse_args()
    out = export_predictions(dataset_path=args.dataset, output=args.output)
    print(f"Wrote predictions: {out}")


if __name__ == "__main__":
    _cli()
