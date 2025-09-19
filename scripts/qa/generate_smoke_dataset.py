"""Generate a tiny SMOKE dataset for CI smoke tests.

Writes data/dataset_SMOKE.parquet with the minimal columns expected by
scripts/training/train_baseline.py: a monotonic datetime index, several
features starting with `f_` and a label column `label_R_H3`.

This script is lightweight and depends only on pandas and numpy (installed
via requirements-dev.txt in CI).
"""
import pathlib
import datetime
import numpy as np
import pandas as pd


def generate(path: str = "data/dataset_SMOKE.parquet") -> pathlib.Path:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Create 20 rows of minute-spaced timestamps starting at UTC now - 20 minutes
    now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
    idx = pd.to_datetime([now - datetime.timedelta(minutes=i) for i in range(20)][::-1])

    # Synthetic features
    np.random.seed(42)
    data = {
        "f_ret_1": np.random.normal(0, 1, size=len(idx)),
        "f_ret_3": np.random.normal(0, 1, size=len(idx)),
        "f_vol_12": np.abs(np.random.normal(1, 0.5, size=len(idx))),
    }

    # Simple label derived from f_ret_1 (float)
    data["label_R_H3"] = data["f_ret_1"] * 0.5 + 0.1

    df = pd.DataFrame(data, index=idx)
    # Ensure index name is datetime-like and monotonic increasing
    df.index.name = "date"
    assert df.index.is_monotonic_increasing

    # Prefer parquet, but fall back to pickle if pyarrow/fastparquet not available
    try:
        df.to_parquet(p)
        return p
    except Exception:
        # Fallback to pickle (.pkl)
        pkl = p.with_suffix(".pkl")
        df.to_pickle(pkl)
        return pkl


if __name__ == "__main__":
    out = generate()
    print(f"Generated SMOKE dataset at: {out}")
