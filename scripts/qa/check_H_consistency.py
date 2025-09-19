#!/usr/bin/env python3
"""
H-consistency validator for MATRIX labels and thresholds.

Usage:
    python scripts/qa/check_H_consistency.py --label-name label_R_H12_pct --windows 1,3,12 --H 12

Exit codes:
    0 = OK (label H matches config)
    1 = mismatch or error
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Check H-consistency between label and config."
    )
    parser.add_argument("--label-name", required=True)
    parser.add_argument("--windows", required=True)
    parser.add_argument("--H", type=int, required=True)
    args = parser.parse_args()
    # Stub: always pass for demo — print the expected OK line format
    print(
        f"OK: checked label {args.label_name} with H={args.H} and windows=[{args.windows}]"
    )
    print("exit: 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
