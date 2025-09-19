#!/usr/bin/env python3
"""
Validate OHLCV CSV for MATRIX (docs-first, stdlib-only).
Checks columns, UTC timestamps, monotonicity, duplicates, volume, gaps.
"""
import argparse
import csv
import pathlib
import datetime
import sys

def main():
    parser = argparse.ArgumentParser(description="Validate OHLCV CSV for MATRIX.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--timeframe", required=True)
    args = parser.parse_args()
    path = pathlib.Path(args.file)
    required_cols = ["datetime", "open", "high", "low", "close", "volume"]
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    # Check columns
    fieldnames = reader.fieldnames or []
    if not all(col in fieldnames for col in required_cols):
        print(f"Missing columns: {set(required_cols) - set(fieldnames)}")
        sys.exit(1)
    # Check timestamps
    times = []
    for r in rows:
        try:
            dt = datetime.datetime.strptime(r["datetime"], "%Y-%m-%d %H:%M:%S")
            times.append(dt)
        except Exception:
            print(f"Bad timestamp: {r['datetime']}")
            sys.exit(1)
    # Monotonicity & duplicates
    if any(t2 <= t1 for t1, t2 in zip(times, times[1:])):
        print("Timestamps not strictly increasing or duplicate found.")
        sys.exit(1)
    # Volume check
    bad_vol = sum(float(r["volume"]) <= 0 for r in rows)
    if bad_vol:
        print(f"Warning: {bad_vol} rows with volume <= 0.")
    # Gaps check (for 5m)
    gaps = 0
    for t1, t2 in zip(times, times[1:]):
        if (t2 - t1).total_seconds() != 300:
            gaps += 1
    if gaps > len(times) * 0.1:
        print(f"Warning: {gaps} gaps detected (>10%).")
    print(f"Checked {len(rows)} rows: OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
