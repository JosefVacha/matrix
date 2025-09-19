"""
validate_threshold_set.py

Stdlib-only validator for required fields in MATRIX TS_*.yml threshold sets.

Usage:
    python validate_threshold_set.py --file docs/thresholds/sets/TS_<DATE>_<TAG>.yml

Checklist output:
    [OK] All required fields present.
    [FAIL] Missing: meta.commit, params.UP

Exit code: 0 if all present, 1 if missing/invalid.
"""
import argparse
import re
from pathlib import Path
import sys

REQUIRED_META = ["created_at", "commit", "timeframe", "pairlist_ref", "model_tag"]
REQUIRED_PARAMS = ["UP", "DN", "hysteresis", "cooldown", "label.mode", "label.H"]

def parse_simple_yaml(path: Path) -> dict:
    out = {"meta": {}, "params": {}}
    block = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.endswith(':') and line[:-1] in ('meta', 'params'):
            block = line[:-1]
            continue
        m = re.match(r'(\w[\w\.]*):\s*(.+)', line)
        if m and block:
            k, v = m.groups()
            out[block][k] = v
    return out

def validate_thresholds(ts: dict) -> list:
    missing = []
    for k in REQUIRED_META:
        if k not in ts["meta"]:
            missing.append(f"meta.{k}")
    for k in REQUIRED_PARAMS:
        if k not in ts["params"]:
            missing.append(f"params.{k}")
    return missing

def main():
    parser = argparse.ArgumentParser(description="Validate required fields in threshold set.")
    parser.add_argument("--file", type=str, required=True, help="Path to TS_*.yml")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    ts = parse_simple_yaml(path)
    missing = validate_thresholds(ts)
    if not missing:
        print("[OK] All required fields present.")
        sys.exit(0)
    else:
        print(f"[FAIL] Missing: {', '.join(missing)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
