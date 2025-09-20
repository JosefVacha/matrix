"""Generate a tiny SMOKE dataset for CI smoke tests.

This generator prefers pandas (to write Parquet). If pandas/numpy are
not available, it falls back to a stdlib pickled list-of-dicts. The
output includes minimal features expected by downstream scripts.
"""

from __future__ import annotations

import argparse
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


def generate(path: str = "data/latest.parquet", start: str = "2025-01-01", end: str = "2025-01-08") -> pathlib.Path:
    """Generate a tiny SMOKE dataset and write to `path`.

    Returns the pathlib.Path of the written file (parquet or .pkl).
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # Prefer pandas if available
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
        try:
            df.to_parquet(p)
            return p
        except Exception:
            pkl = p.with_suffix(".pkl")
            df.to_pickle(pkl)
            return pkl

    except Exception:
        rows = _stdlib_generate_rows(start, end)
        pkl = p.with_suffix(".pkl")
        with pkl.open("wb") as fh:
            pickle.dump(rows, fh)
        return pkl


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic smoke dataset")
    parser.add_argument("--path", default="data/latest.parquet", help="Output path (parquet or pickle)")
    parser.add_argument("--start", help="Start date YYYY-MM-DD", default=None)
    parser.add_argument("--end", help="End date YYYY-MM-DD", default=None)
    parser.add_argument("--days", type=int, default=14, help="Number of days to generate if start/end not provided")
    args = parser.parse_args()

    if not args.start or not args.end:
        today = datetime.date.today()
        end = today
        start = end - datetime.timedelta(days=args.days - 1)
        args.start = start.strftime("%Y-%m-%d")
        args.end = end.strftime("%Y-%m-%d")

    out = generate(path=args.path, start=args.start, end=args.end)
    print(f"Generated SMOKE dataset at: {out}")


if __name__ == "__main__":
    _cli()
