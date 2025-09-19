#!/usr/bin/env python3
"""
Check repository files for Czech diacritics outside allowed paths.

Usage:
  python scripts/qa/check_english_policy.py

Exit code 0 when no violations, 1 when violations found.
"""

import re
import sys
from pathlib import Path

DIACRITICS_RE = re.compile(r"[áčřžšěůýíďťňóúÁČŘŽŠĚŮÝÍĎŤŇÓÚ]")

WHITELIST_PREFIXES = (
    "Knowledge/",
    "README_cs.md",
    "scripts/qa/check_english_policy.py",
    ".git/",
    ".venv/",
    "dist/",
    "build/",
    "__pycache__",
)


def allowed(path: Path) -> bool:
    sp = str(path)
    for w in WHITELIST_PREFIXES:
        if sp.startswith(w) or ("/" + w) in sp:
            return True
    return False


def is_binary(path: Path) -> bool:
    # Heuristic: skip large files and common binary extensions
    try:
        if path.suffix.lower() in (
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pyc",
            ".so",
            ".dll",
            ".exe",
        ):
            return True
        if path.stat().st_size > 200_000:  # >200KB, probably binary or large
            return True
    except Exception:
        return True
    return False


def scan(root: Path):
    violations = []
    for p in root.rglob("*"):
        try:
            if p.is_dir():
                continue
            rel = p.relative_to(root)
        except Exception:
            rel = p
        srel = str(rel)
        if allowed(Path(srel)):
            continue
        if is_binary(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            # skip unreadable files
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if DIACRITICS_RE.search(line):
                snippet = line.strip()
                violations.append((srel, i, snippet))
                # show first match per file
                break
    return violations


def main():
    root = Path(".")
    viol = scan(root)
    if not viol:
        print("English policy check: PASS (no diacritics found outside whitelist)")
        return 0
    print("English policy check: FAIL - diacritics found in these files:")
    for f, ln, snippet in viol:
        print(f"{f}:{ln}: {snippet}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
