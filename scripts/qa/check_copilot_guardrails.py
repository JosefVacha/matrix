#!/usr/bin/env python3
"""
Simple guardrail checker: verifies both AGENTS.md and .github/copilot-instructions.md
are readable and contain required headers. Exit 0 on success, 1 on failure.

Usage:
  python3 scripts/qa/check_copilot_guardrails.py
"""
import sys
from pathlib import Path

FILES = ["AGENTS.md", ".github/copilot-instructions.md"]
KEY_SNIPPETS = {
    "AGENTS.md": "Always read .github/copilot-instructions.md",
    ".github/copilot-instructions.md": "Before replying, always read this file + AGENTS.md",
}

failed = []
for p in FILES:
    path = Path(p)
    if not path.exists():
        failed.append(f"missing: {p}")
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        failed.append(f"unreadable: {p} ({e})")
        continue
    snippet = KEY_SNIPPETS.get(p)
    if snippet and snippet not in text:
        failed.append(f"snippet-missing: {p} (expected snippet not found)")

if failed:
    print("Guardrail check: FAIL")
    for f in failed:
        print(" -", f)
    sys.exit(1)

print("Guardrail check: PASS (AGENTS.md and .github/copilot-instructions.md verified)")
sys.exit(0)
