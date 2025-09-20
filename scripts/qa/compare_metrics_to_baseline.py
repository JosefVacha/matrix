"""Compare paper-trade metrics to a stored baseline.

Exits with:
 - 0: no regression or baseline missing
 - 2: current metrics missing
 - 3: regression detected (final_net below allowed tolerance)

Usage:
  python3 scripts/qa/compare_metrics_to_baseline.py --tol 0.01
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tol", type=float, default=0.01, help="relative tolerance (fraction) allowed drop from baseline final_net")
    args = p.parse_args()

    base = Path("ci/baselines/paper_trade_metrics_baseline.json")
    cur = Path("outputs/paper_trade_metrics.json")

    if not base.exists():
        print("No baseline found, skipping")
        return 0

    if not cur.exists():
        print("Current metrics missing, failing")
        return 2

    b = json.loads(base.read_text())
    c = json.loads(cur.read_text())

    baseline_final = float(b.get("final_net", 0.0))
    current_final = float(c.get("final_net", 0.0))

    print("baseline final_net:", baseline_final)
    print("current  final_net:", current_final)

    allowed = baseline_final * (1.0 - args.tol)
    if current_final < allowed:
        print(f"Regression detected: final_net {current_final} < allowed {allowed} (tol={args.tol})")
        return 3

    print("No regression within tolerance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
