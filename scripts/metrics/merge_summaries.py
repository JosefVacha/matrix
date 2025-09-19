"""
merge_summaries.py

Stub for merging metrics summaries into STABILITY_RECAP.md.

Usage:
    python merge_summaries.py --inputs docs/summaries/SUMMARY_*.md --out docs/STABILITY_RECAP.md

Future: Will extract trigger_rate, long/short, churn_rate, max_dd, stability_notes from summaries.
"""
import argparse
from pathlib import Path


import re
import json

def parse_summary(path):
    vals = {}
    for line in path.read_text().splitlines():
        m = re.match(r"<!--\s*SIGNALS:([^>]*)-->", line)
        if m:
            kvs = m.group(1)
            for pair in kvs.split(';'):
                pair = pair.strip()
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    vals[k.strip()] = v.strip()
        m2 = re.match(r"<!--\s*PERF_PROXY:([^>]*)-->", line)
        if m2:
            kvs = m2.group(1)
            for pair in kvs.split(';'):
                pair = pair.strip()
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    vals[k.strip()] = v.strip()
    # Churn rate (if present in summary)
    for line in path.read_text().splitlines():
        if line.lower().startswith('churn rate:'):
            vals['churn_rate'] = line.split(':',1)[1].strip()
    return vals

def main():
    parser = argparse.ArgumentParser(description="Merge metrics summaries into stability recap table.")
    parser.add_argument("--inputs", nargs='+', help="List of SUMMARY_*.md files")
    parser.add_argument("--out", type=str, required=True, help="Path to STABILITY_RECAP.md")
    args = parser.parse_args()
    results = []
    for fname in args.inputs:
        from pathlib import Path
        path = Path(fname)
        if not path.exists():
            print(f"File not found: {path}")
            continue
        vals = parse_summary(path)
        results.append({"file": fname, **vals})
    print(json.dumps(results, indent=2))
    # TODO: Write back into STABILITY_RECAP.md

if __name__ == "__main__":
    main()
