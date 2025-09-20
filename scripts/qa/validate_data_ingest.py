"""Validate a generated data file for basic invariants.

Checks:
- File exists
- If parquet/pickle -> loads to pandas DataFrame or list-of-dicts
- No NaNs in OHLCV-like columns (f_ret_1,f_ret_3,f_vol_12)
- Index is monotonic (for DataFrame)
"""
from __future__ import annotations

import argparse
import pathlib
import pickle



def validate(path: str) -> bool:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{p} does not exist")

    try:
        import pandas as pd  # type: ignore

        if p.suffix == ".parquet":
            df = pd.read_parquet(p)
        elif p.suffix == ".pkl":
            df = pd.read_pickle(p)
        else:
            # try parquet, then pickle
            try:
                df = pd.read_parquet(p)
            except Exception:
                df = pd.read_pickle(p)

        # Basic invariants
        required = ["f_ret_1", "f_ret_3", "f_vol_12"]
        for r in required:
            if r not in df.columns:
                raise ValueError(f"Missing required column: {r}")
            if df[r].isnull().any():
                raise ValueError(f"NaN detected in column: {r}")

        if not df.index.is_monotonic_increasing:
            raise ValueError("Index is not monotonic increasing")

        return True

    except Exception:
        # fallback to stdlib pickle list-of-dicts
        with p.open("rb") as fh:
            data = pickle.load(fh)
        if not isinstance(data, list):
            raise ValueError("Expected list of rows in pickle fallback")
        for row in data:
            for r in ["f_ret_1", "f_ret_3", "f_vol_12"]:
                if r not in row:
                    raise ValueError(f"Missing required key in row: {r}")
        return True


def _cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default="data/latest.parquet")
    args = parser.parse_args()
    ok = validate(args.path)
    print("OK" if ok else "FAIL")


if __name__ == "__main__":
    _cli()
