#!/usr/bin/env python3
"""
Check retrain cadence policy (offline, stdlib-only)
Usage:
  python scripts/qa/check_retrain_cadence.py --last-train 2025-09-10 --min-days 7 --max-days 30 --drift none --summaries-dir docs/summaries/
"""

import argparse
import sys
import json
import datetime
import os


def main():
    parser = argparse.ArgumentParser(description="Check retrain cadence policy")
    parser.add_argument("--last-train", required=True)
    parser.add_argument("--min-days", type=int, required=True)
    parser.add_argument("--max-days", type=int, required=True)
    parser.add_argument("--drift", choices=["none", "low", "high"], required=True)
    parser.add_argument("--summaries-dir", required=True)
    args = parser.parse_args()
    try:
        last_train = datetime.datetime.strptime(args.last_train, "%Y-%m-%d")
    except Exception:
        print(json.dumps({"pass": False, "reason": "Invalid last_train date"}))
        sys.exit(1)
    today = datetime.datetime.utcnow()
    days_since = (today - last_train).days
    # Logic
    if days_since > args.max_days:
        print(
            json.dumps(
                {
                    "pass": False,
                    "reason": f"Days since last train ({days_since}) > max_days ({args.max_days})",
                }
            )
        )
        sys.exit(1)
    if args.drift == "high" and days_since > args.min_days:
        print(
            json.dumps(
                {
                    "pass": False,
                    "reason": f"Drift high and days since last train ({days_since}) > min_days ({args.min_days})",
                }
            )
        )
        sys.exit(1)
    print(
        json.dumps(
            {
                "pass": True,
                "reason": f"Cadence OK: days_since={days_since}, drift={args.drift}",
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
