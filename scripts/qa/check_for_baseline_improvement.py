#!/usr/bin/env python3
"""Check whether current metrics improved over baseline.

Exit codes:
 - 0: improvement detected for at least one metric
 - 1: no improvement
 - 2: current metrics missing
 - 3: baseline missing
"""

import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--metrics",
        type=str,
        default='{"final_net": 0.0}',
        help='JSON mapping metric->min_relative_improvement (e.g. {"final_net": 0.01})',
    )
    args = p.parse_args()

    base = Path("ci/baselines/paper_trade_metrics_baseline.json")
    cur = Path("outputs/paper_trade_metrics.json")

    if not cur.exists():
        print("Current metrics missing")
        return 2
    if not base.exists():
        print("Baseline missing; treating as improvement")
        return 0

    c = json.loads(cur.read_text())
    b = json.loads(base.read_text())

    metric_tols = json.loads(args.metrics)
    improved_any = False
    for metric, req_rel in metric_tols.items():
        bval = b.get(metric)
        cval = c.get(metric)
        print(f"check metric={metric} baseline={bval} current={cval} req_rel={req_rel}")
        try:
            bnum = float(bval) if bval is not None else None
            cnum = float(cval)
        except Exception:
            continue

        if bnum is None:
            # baseline missing -> treated as improvement
            improved_any = True
            continue

        # For drawdown-type metrics lower is better
        if metric.lower().endswith("drawdown") or metric.lower().startswith(
            "max_drawdown"
        ):
            # improvement if current < baseline * (1 - req_rel)
            if cnum < bnum * (1.0 - float(req_rel)):
                improved_any = True
        else:
            # improvement if current > baseline * (1 + req_rel)
            if cnum > bnum * (1.0 + float(req_rel)):
                improved_any = True

    return 0 if improved_any else 1


if __name__ == "__main__":
    raise SystemExit(main())
