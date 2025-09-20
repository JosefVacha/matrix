#!/usr/bin/env python3
"""Aggregate JSON outputs under outputs/ into outputs/summary.json

This script looks for files like outputs/guardrail_check.json and combines
selected keys into a compact summary for maintainers.
"""
import json
from pathlib import Path

OUT = Path("outputs")
SUMMARY = OUT / "summary.json"

if not OUT.exists():
    print("No outputs/ directory found")
    raise SystemExit(0)

summary = {}
for p in OUT.glob("*.json"):
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if p.name == "guardrail_check.json" or p.name.startswith("guardrail"):
        summary["guardrail"] = {k: data.get(k) for k in ["ok","preface_ok","language_ok","missing_critical","missing_conditionals"]}
    else:
        summary[p.name] = data

SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"Wrote {SUMMARY}")
