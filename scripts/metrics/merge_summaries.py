"""
merge_summaries.py

Merge metrics summaries into STABILITY_RECAP.md for offline checks and reporting.

Usage:
    python merge_summaries.py --inputs docs/summaries/SUMMARY_*.md --out docs/STABILITY_RECAP.md

This is a small, deterministic implementation used by unit tests; no external deps.
"""

import argparse
from pathlib import Path
import re


def parse_summary(path: Path):
    vals = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"<!--\s*SIGNALS:([^>]*)-->", line)
        if m:
            kvs = m.group(1)
            for pair in kvs.split(";"):
                pair = pair.strip()
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    vals[k.strip()] = v.strip()
        m2 = re.match(r"<!--\s*PERF_PROXY:([^>]*)-->", line)
        if m2:
            kvs = m2.group(1)
            for pair in kvs.split(";"):
                pair = pair.strip()
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    vals[k.strip()] = v.strip()
        # Also parse simple 'key: value' lines produced by extractors
        m3 = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m3:
            k, v = m3.groups()
            vals[k.strip()] = v.strip()
    # Churn rate (if present in summary body)
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith("churn rate:"):
            vals["churn_rate"] = line.split(":", 1)[1].strip()
    return vals


def main():
    parser = argparse.ArgumentParser(
        description="Merge metrics summaries into stability recap table."
    )
    parser.add_argument(
        "--inputs", nargs="+", help="List of SUMMARY_*.md files", required=True
    )
    parser.add_argument(
        "--out", type=str, required=True, help="Path to STABILITY_RECAP.md"
    )
    args = parser.parse_args()
    results = []
    for fname in args.inputs:
        path = Path(fname)
        if not path.exists():
            print(f"File not found: {path}")
            continue
        vals = parse_summary(path)
        results.append({"file": fname, **vals})
    out_path = Path(args.out)
    # Render a minimal stability recap markdown with one entry per summary
    lines = []
    for r in results:
        lines.append(f"file: {r.get('file')}")
        # include some common fields if present
        for k in (
            "trigger_rate",
            "long_rate",
            "short_rate",
            "churn_rate",
            "max_drawdown",
            "run_tag",
        ):
            if k in r:
                lines.append(f"{k}: {r[k]}")
        lines.append("")
    out_text = "\n".join(lines)
    out_path.write_text(out_text, encoding="utf-8")
    print(f"Wrote recap to {out_path}")


if __name__ == "__main__":
    main()
