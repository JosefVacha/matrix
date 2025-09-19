#!/usr/bin/env python3
"""
Prepare offline dataset for MATRIX training (docs-first, stdlib-only).

CLI:
  python scripts/training/prepare_dataset.py --ohlcv <path> --from <date> --to <date> --out <dataset.json>

This script documents how to assemble (X, y) from OHLCV using hooks.
No pandas import; returns only shapes/sizes.
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Prepare offline dataset for MATRIX training."
    )
    parser.add_argument("--ohlcv", required=True)
    parser.add_argument("--from", dest="from_date", required=True)
    parser.add_argument("--to", dest="to_date", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    # Stub: Document shapes only
    dataset = {
        "n_rows_after_warmup": 500,
        "n_features": 6,
        "label_name": "label_R_12_log",
        "dropped_warmup": 12,
    }
    with open(args.out, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Wrote dataset summary to {args.out}")
    sys.exit(0)


if __name__ == "__main__":
    main()
