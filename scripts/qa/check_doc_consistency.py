#!/usr/bin/env python3
"""
Check docstring and contract consistency for mapping/adapter/CONTRACTS.md.
Stdlib only: argparse, pathlib, re, sys, textwrap.
"""

import argparse, pathlib, re, sys, textwrap

MUST_TERMS = [
    "enter_long",
    "enter_short",
    "exit_long",
    "exit_short",
    "hysteresis",
    "cooldown",
    "no leakage",
    "0/1 lists",
    "same length as predictions",
]

TARGETS = {
    "mapping.py": (
        "src/matrix/strategy/mapping.py",
        r"def map_predictions_to_signals\(.*?\):([\s\S]*?)def |$",
    ),
    "adapter.py": (
        "src/matrix/adapter/freqtrade_strategy_adapter.py",
        r"""(\"\"\"[\s\S]*?\"\"\")""",
    ),
    "CONTRACTS.md": ("docs/CONTRACTS.md", r"## Strategy I/O([\s\S]*?)(##|$)"),
}


def extract_doc(path, pattern):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1) if m else ""


def check_terms(doc, terms):
    missing = [t for t in terms if t not in doc]
    return missing


def main():
    parser = argparse.ArgumentParser(
        description="Check doc consistency across mapping, adapter, CONTRACTS.md."
    )
    args = parser.parse_args()
    results = {}
    for label, (path, pattern) in TARGETS.items():
        doc = extract_doc(path, pattern)
        missing = check_terms(doc, MUST_TERMS)
        results[label] = missing
    ok = all(not v for v in results.values())
    print("\nDoc Consistency Checklist:")
    for label, missing in results.items():
        print(f"- {label}: {'OK' if not missing else 'Missing: ' + ', '.join(missing)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
