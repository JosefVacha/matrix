"""
validate_report_markers.py

Stdlib-only validator for required report markers in MATRIX REPORT_*.md files.

Usage:
    python validate_report_markers.py --report docs/REPORTS/REPORT_<DATE>_<TAG>.md

Sample output:
    [OK] All required markers present: RUN_META, PRED_DIST, SIGNALS
    [FAIL] Missing markers: PRED_DIST

Exit code: 0 if all present, 1 if missing.
"""

import argparse
import re
from pathlib import Path
import sys
import textwrap

REQUIRED = ["RUN_META", "PRED_DIST", "SIGNALS"]


def scan_report(path: Path) -> dict:
    markers = {}
    for line in path.read_text().splitlines():
        m = re.match(r"<!--\s*(\w+):", line)
        if m:
            markers[m.group(1)] = True
    return markers


def validate_required(markers: dict) -> list:
    return [k for k in REQUIRED if k not in markers]


def main():
    parser = argparse.ArgumentParser(description="Validate required report markers.")
    parser.add_argument("--report", type=str, required=True, help="Path to REPORT_*.md")
    args = parser.parse_args()
    path = Path(args.report)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    markers = scan_report(path)
    missing = validate_required(markers)
    if not missing:
        print(f"[OK] All required markers present: {', '.join(REQUIRED)}")
        sys.exit(0)
    else:
        print(f"[FAIL] Missing markers: {', '.join(missing)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
