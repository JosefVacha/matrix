#!/usr/bin/env python3
"""Decide whether the current paper-trade metrics improve the baseline.

Prints to stdout two lines:
  should_pr=true|false
  current_final=<float>

Exit code 0 always.
"""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tol", type=float, default=0.0, help="relative improvement fraction required")
    args = p.parse_args()

    base = Path("ci/baselines/paper_trade_metrics_baseline.json")
    cur = Path("outputs/paper_trade_metrics.json")
    if not cur.exists():
        print("should_pr=false")
        print("current_final=0.0")
        return 0

    c = json.loads(cur.read_text())
    current_final = float(c.get("final_net", 0.0))

    if not base.exists():
        should = True
    else:
        b = json.loads(base.read_text())
        baseline_final = float(b.get("final_net", 0.0))
        should = current_final > baseline_final * (1.0 + args.tol)

    print(f"should_pr={'true' if should else 'false'}")
    print(f"current_final={current_final}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
