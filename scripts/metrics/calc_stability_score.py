"""
calc_stability_score.py

Stdlib-only stability score calculator for MATRIX SUMMARY files.

Usage:
    python calc_stability_score.py --summaries docs/summaries/SUMMARY_*.md [...]

Formula (PLACEHOLDER):
- Start at 100
- penalty_trigger = abs(trigger_rate - target_band_center) / target_band_halfwidth * 25
- penalty_imbalance = max(0, (|long_rate - short_rate| - tol)) / (1 - tol) * 25
- penalty_churn = clamp(churn_rate / churn_ref, 0..1) * 25
- penalty_dd = clamp(max_dd / dd_ref, 0..1) * 25
- score = round(max(0, 100 - sum(penalties)))
- Constants: target_band_center=0.1, target_band_halfwidth=0.05, tol=0.1, churn_ref=0.3, dd_ref=0.15

Output:
    {"file":"SUMMARY_2025-09-19_run2.md","stability_score":72}
    {"aggregate_avg":70}

Exit codes: 0 OK, 1 on file not found/unreadable
"""
import argparse
import re
from pathlib import Path
import sys
import json

def parse_summary(path: Path) -> dict:
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
    return vals

def clamp(x, a, b):
    return max(a, min(b, x))

def calc_score(vals: dict) -> int:
    # PLACEHOLDER constants
    target_band_center = 0.1
    target_band_halfwidth = 0.05
    tol = 0.1
    churn_ref = 0.3
    dd_ref = 0.15
    try:
        trigger_rate = float(vals.get("trigger_rate", "0"))
        long_rate = float(vals.get("long_rate", "0"))
        short_rate = float(vals.get("short_rate", "0"))
        churn_rate = float(vals.get("churn_rate", "0"))
        max_dd = float(vals.get("max_dd", "0"))
        penalty_trigger = clamp(abs(trigger_rate - target_band_center) / target_band_halfwidth, 0, 1) * 25
        penalty_imbalance = clamp(max(0, abs(long_rate - short_rate) - tol) / (1 - tol), 0, 1) * 25
        penalty_churn = clamp(churn_rate / churn_ref, 0, 1) * 25
        penalty_dd = clamp(max_dd / dd_ref, 0, 1) * 25
        score = round(max(0, 100 - (penalty_trigger + penalty_imbalance + penalty_churn + penalty_dd)))
    except Exception:
        score = 0
    return score

def main():
    parser = argparse.ArgumentParser(description="Calculate stability score from SUMMARY files.")
    parser.add_argument("--summaries", nargs='+', required=True, help="List of SUMMARY_*.md files")
    args = parser.parse_args()
    scores = []
    for fname in args.summaries:
        path = Path(fname)
        if not path.exists():
            print(f"File not found: {path}")
            sys.exit(1)
        vals = parse_summary(path)
        score = calc_score(vals)
        print(json.dumps({"file": fname, "stability_score": score}))
        scores.append(score)
    if scores:
        avg = round(sum(scores) / len(scores))
        print(json.dumps({"aggregate_avg": avg}))
    sys.exit(0)

if __name__ == "__main__":
    main()
