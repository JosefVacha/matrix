"""Generate a tiny SMOKE dataset for CI smoke tests.

This generator prefers to use pandas/fastparquet/pyarrow when available
to write a Parquet file (`data/dataset_SMOKE.parquet`). If pandas/numpy
are not installed in the environment (for example in minimal CI runners),
the script falls back to a pure-stdlib implementation that writes a
pickle file (`data/dataset_SMOKE.pkl`). The produced file contains the
minimal columns expected by `scripts/training/train_baseline.py`:
  - f_ret_1, f_ret_3, f_vol_12, label_R_H3, label_R_H3_pct
and a monotonic date index named `date`.

The fallback keeps the same public API: `generate(path, start, end) -> Path`.
"""

from __future__ import annotations

import datetime
import pathlib
import pickle
import random
from typing import List, Dict


def _stdlib_generate_rows(start: str, end: str) -> List[Dict]:
    start_d = datetime.date.fromisoformat(start)
    end_d = datetime.date.fromisoformat(end)
    days = (end_d - start_d).days + 1
    random.seed(42)
    rows: List[Dict] = []
    for i in range(days):
        d = start_d + datetime.timedelta(days=i)
        # simple synthetic features
        f_ret_1 = random.gauss(0, 1)
        f_ret_3 = random.gauss(0, 1)
        f_vol_12 = abs(random.gauss(1, 0.5))
        label = f_ret_1 * 0.5 + 0.1
        rows.append(
            {
                "date": d.isoformat(),
                "f_ret_1": f_ret_1,
                "f_ret_3": f_ret_3,
                "f_vol_12": f_vol_12,
                "label_R_H3": label,
                "label_R_H3_pct": label,
            }
        )
    return rows


def generate(
    path: str = "data/dataset_SMOKE.parquet",
    start: str = "2025-01-01",
    end: str = "2025-01-08",
) -> pathlib.Path:
    """Generate a tiny SMOKE dataset.

    Tries the pandas route first; if pandas isn't available, uses stdlib
    and writes a pickle file with a list-of-dicts. Returns the Path to
    the written file.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Prefer using pandas (if available) to keep parity with existing code
    try:
        import numpy as np  # type: ignore
        import pandas as pd  # type: ignore

        idx = pd.date_range(start=start, end=end, freq="D")
        np.random.seed(42)
        data = {
            "f_ret_1": np.random.normal(0, 1, size=len(idx)),
            "f_ret_3": np.random.normal(0, 1, size=len(idx)),
            "f_vol_12": np.abs(np.random.normal(1, 0.5, size=len(idx))),
        }
        data["label_R_H3"] = data["f_ret_1"] * 0.5 + 0.1
        data["label_R_H3_pct"] = data["f_ret_1"] * 0.5 + 0.1
        df = pd.DataFrame(data, index=idx)
        df.index.name = "date"
        assert df.index.is_monotonic_increasing
        # Try parquet first, fallback to pickle via pandas
        try:
            df.to_parquet(p)
            return p
        except Exception:
            pkl = p.with_suffix(".pkl")
            df.to_pickle(pkl)
            return pkl

    except Exception:
        # Stdlib fallback: write a pickled list-of-dicts (date isoformat strings)
        rows = _stdlib_generate_rows(start, end)
        pkl = p.with_suffix(".pkl")
        with pkl.open("wb") as fh:
            pickle.dump(rows, fh)
        return pkl


if __name__ == "__main__":
    out = generate()
    print(f"Generated SMOKE dataset at: {out}")
