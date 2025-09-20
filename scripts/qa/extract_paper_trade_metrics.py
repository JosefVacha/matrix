"""Extract minimal metrics from paper-trade simulator report.

Usage:
    python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json
"""

import argparse
import json
from pathlib import Path
from statistics import mean, median, pstdev
from typing import List


def extract(input_path: Path, output_path: Path) -> dict:
    data = json.loads(input_path.read_text())
    # Expecting the simulator to write top-level fields final_net and trades (list)
    final_net = data.get("final_net")
    trades = data.get("trades") or []
    # Per-trade P&L (expect each trade to have 'pnl' numeric field)
    pnls = [t.get("pnl") for t in trades]
    # keep only numeric pnls (filter out None)
    pnls_numeric: List[float] = [float(x) for x in pnls if x is not None]

    # Equity series optional: simulator may include equity curve 'equity' list
    equity = data.get("equity")

    # Max drawdown computation and drawdown series if equity series provided
    max_drawdown = None
    drawdown_summary = None
    if equity:
        peak = equity[0]
        max_dd = 0.0
        dd_series = []
        for v in equity:
            if v > peak:
                peak = v
            dd = (peak - v) / peak if peak != 0 else 0.0
            dd_series.append(dd)
            if dd > max_dd:
                max_dd = dd
        max_drawdown = max_dd
        # simple summary: min/median/max of drawdown series
        try:
            from statistics import median as _median

            drawdown_summary = {
                "dd_min": min(dd_series),
                "dd_median": _median(dd_series),
                "dd_max": max(dd_series),
            }
        except Exception:
            drawdown_summary = None

    # Per-trade pnl detailed stats
    trade_stats = None
    if pnls_numeric:
        trade_stats = {
            "count": len(pnls_numeric),
            "mean": mean(pnls_numeric),
            "median": median(pnls_numeric),
            "std_pop": pstdev(pnls_numeric) if len(pnls_numeric) > 1 else 0.0,
            "min": min(pnls_numeric),
            "max": max(pnls_numeric),
        }

    metrics = {
        "final_net": final_net,
        "trades_count": len(trades),
        "trade_pnl": trade_stats,
        "max_drawdown": max_drawdown,
        "drawdown_summary": drawdown_summary,
    }
    output_path.write_text(json.dumps(metrics, indent=2))
    return metrics


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    inp = Path(args.input)
    out = Path(args.output)
    if not inp.exists():
        raise SystemExit(f"Input file not found: {inp}")
    metrics = extract(inp, out)
    print("Wrote metrics:", out)
    print(metrics)


if __name__ == "__main__":
    main()
