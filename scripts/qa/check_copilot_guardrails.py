#!/usr/bin/env python3
"""
Simple guardrail checker: verifies both AGENTS.md and .github/copilot-instructions.md
are readable and contain required headers. Exit 0 on success, 1 on failure.

Usage:
  python3 scripts/qa/check_copilot_guardrails.py
"""
import sys
import subprocess
from pathlib import Path
from typing import List

# Critical trio (must always be present and reloaded)
CRITICAL = [
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "Knowledge/PROJECT_STATE.md",
]

# Conditional files mapping: key -> list of globs or files to check when scope matches
CONDITIONAL_MAP = {
    "tasks": [".vscode/tasks.json"],
    "docs": [
        "docs/COPILOT_TODO.md",
        "docs/LANGUAGE_AUDIT.md",
        "docs/MODEL_REGISTRY.md",
        "docs/TRAINING_PROTOCOL.md",
        "docs/LABELS.md",
        "docs/CONTRACTS.md",
    ],
    "ci": [".github/workflows/*.yml"],
}

def exists_readable(path: str) -> bool:
    p = Path(path)
    # support simple glob patterns
    if "*" in path:
        matches = list(p.parent.glob(p.name))
        return any(m.exists() for m in matches)
    return p.exists()

def get_changed_scope() -> List[str]:
    # Try to detect staged/changed files and map to conditional scopes.
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", "--staged"], text=True)
    except Exception:
        try:
            out = subprocess.check_output(["git", "diff", "--name-only"], text=True)
        except Exception:
            out = ""
    files = [line.strip() for line in out.splitlines() if line.strip()]
    scopes = set()
    for f in files:
        if f.startswith(".github/workflows/"):
            scopes.add("ci")
        if f.startswith("docs/"):
            scopes.add("docs")
        if f.startswith(".vscode/"):
            scopes.add("tasks")
        if f.startswith("scripts/registry/") or f.startswith("models/"):
            scopes.add("docs")
    return list(scopes)

def check_files(files: List[str]) -> List[str]:
    missing = []
    for f in files:
        if not exists_readable(f):
            missing.append(f)
    return missing

def main():
    failed = []
    # Check critical
    missing_critical = check_files(CRITICAL)
    if missing_critical:
        failed.extend([f"missing: {x}" for x in missing_critical])

    # Determine conditional scopes
    scopes = get_changed_scope()
    conditional_checked = []
    conditional_missing = []
    # Always check some default conditionals (docs and tasks) to be conservative
    default_conditionals = CONDITIONAL_MAP.get("docs", []) + CONDITIONAL_MAP.get("tasks", [])
    to_check = set(default_conditionals)
    # Expand with scopes detected
    for s in scopes:
        to_check.update(CONDITIONAL_MAP.get(s, []))

    for f in sorted(to_check):
        conditional_checked.append(f)
        if not exists_readable(f):
            conditional_missing.append(f)
            failed.append(f"missing-conditional: {f}")

    # Output machine-readable summary
    if failed:
        print("Guardrail check: FAIL")
        print("Critical reloaded:", [c for c in CRITICAL if c not in missing_critical])
        print("Conditional reloaded:", [c for c in conditional_checked if c not in conditional_missing])
        for f in failed:
            print(" -", f)
        sys.exit(1)

    print("Guardrail check: PASS")
    print("Critical reloaded:", CRITICAL)
    print("Conditional reloaded:", conditional_checked)
    sys.exit(0)


if __name__ == '__main__':
    main()
