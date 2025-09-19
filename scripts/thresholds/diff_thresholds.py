"""
diff_thresholds.py

Purpose:
    Compare two docs/thresholds/sets/TS_*.yml files and produce a tiny Markdown diff into docs/diffs/DIFF_TS_<A>_vs_<B>.md.
    (YAML parsing will be minimal; for now, leave as TODO.)

CLI Sketch:
    python diff_thresholds.py --a TS_20250101_...yml --b TS_20250201_...yml --out docs/diffs/DIFF_TS_<A>_vs_<B>.md

No external dependencies; stdlib only. No file I/O logic yet (just stubs).
"""
from typing import Dict, Any
import re
import argparse
from pathlib import Path
import datetime

def parse_simple_yaml(path: Path) -> Dict[str, Any]:
    """
    Parse a simple YAML file with top-level meta: and params: blocks.
    Only supports key: value scalars, no lists or nested maps.
    """
    out = {"meta": {}, "params": {}}
    block = None
    try:
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
    except Exception as e:
        print(f"Error reading YAML: {e}")
        return {"meta": {}, "params": {}}
    return out

def diff_params(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare meta and params blocks, return dict of differences.
    Only keys: created_at, commit, model_tag (meta); UP, DN, hysteresis, cooldown, label.mode, label.H (params).
    """
    keys_meta = ['created_at', 'commit', 'model_tag']
    keys_params = ['UP', 'DN', 'hysteresis', 'cooldown', 'label.mode', 'label.H']
    diff = {"meta": {}, "params": {}}
    for k in keys_meta:
        va, vb = a['meta'].get(k), b['meta'].get(k)
        if va != vb:
            diff['meta'][k] = {'A': va, 'B': vb}
    for k in keys_params:
        va, vb = a['params'].get(k), b['params'].get(k)
        if va != vb:
            diff['params'][k] = {'A': va, 'B': vb}
    return diff

def render_diff(a_name: str, b_name: str, diff: Dict[str, Any]) -> str:
    """
    Render Markdown diff using DIFF_REPORT_TEMPLATE.md structure.
    """
    template_path = Path(__file__).parent.parent.parent / "docs" / "DIFF_REPORT_TEMPLATE.md"
    template = template_path.read_text()
    # Fill compared sets
    out = template.replace("<TS_A.yml>", a_name)
    out = out.replace("<TS_B.yml>", b_name)
    out = out.replace("<YYYY-MM-DD HH:MM>", str(datetime.datetime.now())[:16])
    # Build diff table
    rows = []
    for k, v in diff['meta'].items():
        rows.append(f"| {k} | {v['A'] or 'N/A'} | {v['B'] or 'N/A'} | major |")
    for k, v in diff['params'].items():
        rows.append(f"| {k} | {v['A'] or 'N/A'} | {v['B'] or 'N/A'} | major |")
    table = '\n'.join(rows) if rows else '| (no major changes) | N/A | N/A | none |'
    out = out.replace('| <param_name>  | <A_value>   | <B_value>   | <major/minor/none> |', table)
    return out

def main():
    """
    CLI entry point for threshold set diffing.
    """
    parser = argparse.ArgumentParser(description="Diff two MATRIX threshold sets (TS_*.yml)")
    parser.add_argument("--a", type=str, required=True, help="Path to first TS_*.yml")
    parser.add_argument("--b", type=str, required=True, help="Path to second TS_*.yml")
    parser.add_argument("--out", type=str, required=True, help="Path to output DIFF_*.md")
    args = parser.parse_args()
    a_path = Path(args.a)
    b_path = Path(args.b)
    out_path = Path(args.out)
    if not a_path.exists() or not b_path.exists():
        print("Missing input YAML file(s)")
        exit(1)
    a = parse_simple_yaml(a_path)
    b = parse_simple_yaml(b_path)
    diff = diff_params(a, b)
    diff_md = render_diff(a_path.name, b_path.name, diff)
    out_path.write_text(diff_md)
    print(f"Diff written to {out_path}")

if __name__ == "__main__":
    main()
