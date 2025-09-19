"""
calc_churn.py

Stdlib-only churn rate calculator for MATRIX REPORT or SUMMARY files.

Usage:
    python calc_churn.py --report docs/REPORTS/REPORT_<DATE>_<TAG>.md
    python calc_churn.py --summary docs/summaries/SUMMARY_<DATE>_<TAG>.md

Output:
    {"source":"REPORT","churn_rate":0.23,"entries":100,"exits_lt_cooldown":23}
    or {"churn_rate":"N/A"} if not computable

Exit codes: 0 OK (even if churn not computable), 1 on file not found/unreadable
"""
import argparse
import re
from pathlib import Path
import sys
import json

def parse_markers(path: Path) -> dict:
    markers = {}
    for line in path.read_text().splitlines():
        m = re.match(r"<!--\s*SIGNALS:([^>]*)-->", line)
        if m:
            kvs = m.group(1)
            for pair in kvs.split(';'):
                pair = pair.strip()
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    markers[k.strip()] = v.strip()
    return markers

def main():
    parser = argparse.ArgumentParser(description="Calculate churn rate from REPORT or SUMMARY.")
    parser.add_argument("--report", type=str, help="Path to REPORT_*.md")
    parser.add_argument("--summary", type=str, help="Path to SUMMARY_*.md")
    args = parser.parse_args()
    source = None
    path = None
    if args.report:
        source = "REPORT"
        path = Path(args.report)
    elif args.summary:
        source = "SUMMARY"
        path = Path(args.summary)
    else:
        print("Must provide --report or --summary")
        sys.exit(1)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    markers = parse_markers(path)
    try:
        entries = int(markers.get("entries", "0"))
        exits_lt_cooldown = int(markers.get("exits_lt_cooldown", "0"))
        churn_rate = round(exits_lt_cooldown / entries, 4) if entries > 0 else "N/A"
        out = {"source": source, "churn_rate": churn_rate, "entries": entries, "exits_lt_cooldown": exits_lt_cooldown}
    except Exception:
        out = {"churn_rate": "N/A"}
    print(json.dumps(out))
    sys.exit(0)

if __name__ == "__main__":
    main()
