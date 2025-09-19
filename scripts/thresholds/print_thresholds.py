"""
print_thresholds.py

Prints key threshold values from a MATRIX TS_*.yml file for copy-paste.

Usage:
    python print_thresholds.py --file docs/thresholds/sets/TS_*.yml

Output:
    UP=<...> DN=<...> HYST=<...> COOLDOWN=<...>

Exit 0 on success, 1 on error.
"""
import argparse
import re
from pathlib import Path
import sys
import textwrap

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

def main():
    parser = argparse.ArgumentParser(description="Print key thresholds for copy-paste.")
    parser.add_argument("--file", type=str, required=True, help="Path to TS_*.yml")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    ts = parse_simple_yaml(path)
    try:
        up = ts["params"]["UP"]
        dn = ts["params"]["DN"]
        hyst = ts["params"]["hysteresis"]
        cooldown = ts["params"]["cooldown"]
        print(f"UP={up} DN={dn} HYST={hyst} COOLDOWN={cooldown}")
        sys.exit(0)
    except Exception:
        print("[FAIL] Could not parse required threshold values.")
        sys.exit(1)

if __name__ == "__main__":
    main()
