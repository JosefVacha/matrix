"""Extract minimal metrics from paper-trade simulator report.

Usage:
    python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json
"""
import argparse
import json
from pathlib import Path


def extract(input_path: Path, output_path: Path) -> dict:
    data = json.loads(input_path.read_text())
    # Expecting the simulator to write top-level fields final_net and trades (list)
    final_net = data.get("final_net")
    trades = data.get("trades") or []
    metrics = {
        "final_net": final_net,
        "trades_count": len(trades),
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
