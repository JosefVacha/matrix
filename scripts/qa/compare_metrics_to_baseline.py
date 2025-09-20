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
    p.add_argument(
        "--metrics",
        type=str,
        default=None,
        help=(
            'JSON string mapping metric->relative_tolerance, e.g. \'{"final_net": 0.05, "max_drawdown": 0.1}\''
        ),
    )
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

    # Default metric set
    if args.metrics:
        try:
            metric_tols = json.loads(args.metrics)
        except Exception as e:
            print("Invalid --metrics JSON:", e)
            return 4
    else:
        metric_tols = {"final_net": 0.05}

    regressions = []
    for metric, tol in metric_tols.items():
        bval = b.get(metric)
        cval = c.get(metric)
        print(f"metric={metric} baseline={bval} current={cval} tol={tol}")
        if bval is None:
            print(f"Baseline missing metric {metric}; skipping")
            continue
        if cval is None:
            print(f"Current metrics missing {metric}; failing")
            regressions.append((metric, "missing_current"))
            continue

        try:
            bnum = float(bval)
            cnum = float(cval)
        except Exception:
            print(f"Non-numeric metric {metric}; skipping")
            continue

        # Direction: for most metrics higher is better (final_net). For drawdown, lower is better.
        if metric.lower().endswith("drawdown") or metric.lower().startswith(
            "max_drawdown"
        ):
            # drawdown: regression if current > baseline * (1 + tol)
            allowed = bnum * (1.0 + float(tol))
            if cnum > allowed:
                regressions.append((metric, cnum, allowed))
        else:
            # higher is better: regression if current < baseline * (1 - tol)
            allowed = bnum * (1.0 - float(tol))
            if cnum < allowed:
                regressions.append((metric, cnum, allowed))

    if regressions:
        print("Regressions detected:")
        for r in regressions:
            print(r)
        return 3

    print("No regression within tolerances")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
