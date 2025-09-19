#!/usr/bin/env python3
"""
Prints DRY run shell commands for human copy/paste (never executes).
Stdlib only: argparse, pathlib, textwrap, sys
"""

import argparse, pathlib, textwrap, sys


def main():
    parser = argparse.ArgumentParser(
        description="Print DRY run shell commands for human copy/paste."
    )
    parser.add_argument("--ts", required=True)
    parser.add_argument("--cfg", required=True)
    parser.add_argument("--raw", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()
    cmds = [
        f"python scripts/thresholds/print_thresholds.py --file {args.ts}",
        "# Inject into strategies/MatrixAdapterStrategy.py here",
        f"# freqtrade backtesting --config {args.cfg} --strategy MatrixAdapterStrategy",
        f"python scripts/metrics/ingest_freqtrade_report.py --input {args.raw} --report {args.report} --summary {args.summary}",
        f"python scripts/metrics/merge_summaries.py --inputs {args.summary} --out docs/STABILITY_RECAP.md",
    ]
    print("\nDRY Run Rehearsal (copy/paste these commands):\n")
    for c in cmds:
        print(c)
    sys.exit(0)


if __name__ == "__main__":
    main()
