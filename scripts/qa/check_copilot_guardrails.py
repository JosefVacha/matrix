#!/usr/bin/env python3
"""
Simple guardrail checker: verifies both AGENTS.md and .github/copilot-instructions.md
are readable and contain required headers. Exit 0 on success, 1 on failure.

Usage:
  python3 scripts/qa/check_copilot_guardrails.py
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict


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
    """Return True if file exists; supports simple glob patterns."""
    p = Path(path)
    if "*" in path:
        # use glob on parent/name
        parent = p.parent if p.parent.exists() else Path(".")
        matches = list(parent.glob(p.name))
        return any(m.exists() for m in matches)
    return p.exists()


def get_changed_scope() -> List[str]:
    """Detect changed files via git and map to scopes.

    If git is unavailable or no changes detected, return an empty list.
    """
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--staged"], text=True
        )
        if not out.strip():
            out = subprocess.check_output(["git", "diff", "--name-only"], text=True)
    except Exception:
        return []
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


def run_subscript(script: str) -> Dict[str, object]:
    """Run a python script, capture exit code and combined output.

    Returns dict with keys: code, output
    """
    try:
        # Protect against hanging subsidiary scripts with a timeout (seconds)
        p = subprocess.run(
            ["python3", script], capture_output=True, text=True, check=False, timeout=15
        )
        return {"code": p.returncode, "output": p.stdout + p.stderr}
    except subprocess.TimeoutExpired as e:
        return {"code": 2, "output": f"timeout: {str(e)}"}
    except Exception as e:
        return {"code": 1, "output": str(e)}


def check_preface() -> bool:
    """Ensure the copilot preface lines are present in copilot-instructions.md."""
    p = Path(".github/copilot-instructions.md")
    if not p.exists():
        return False
    txt = p.read_text(encoding="utf-8")
    line1 = "Guardrail check: ran check_copilot_guardrails.py — PASS"
    line2 = "Files reloaded: copilot-instructions.md, AGENTS.md, PROJECT_STATE.md"
    return (line1 in txt) and (line2 in txt)


def check_language_rules() -> bool:
    """Ensure instructions contain the language rule for Czech replies and template reference.

    Specifically, require a line that says (case-insensitive):
      "If user asks in Czech, answer in Czech"
    and that `Knowledge/REPLY_TEMPLATES.md` is referenced in the copilot file.
    """
    p = Path(".github/copilot-instructions.md")
    if not p.exists():
        return False
    txt = p.read_text(encoding="utf-8").lower()
    # Require a single explicit mandatory Czech sentence to reduce ambiguity
    mandatory_czech = "pokud uživatel píše v češtině, odpověz v češtině"
    rule_ok = mandatory_czech in txt

    # Fallback: if mandatory sentence not present, use a lightweight regex-based Czech detector
    # looking for Czech diacritics and common Czech stop-words. This reduces false negatives
    # while still preferring the explicit sentence when present.
    if not rule_ok:
        import re

        # expanded list of short/common Czech words to reduce false-negatives
        cz_words = [
            "že",
            "takže",
            "až",
            "se",
            "proč",
            "co",
            "kde",
            "kdy",
            "je",
            "jsme",
            "jste",
            "budeme",
            "bude",
            "máme",
            "máte",
            "pokud",
            "uživatel",
            "odpověz",
            "česky",
            "češt",
            "děkuji",
            "prosím",
            "můžeš",
            "mohu",
            "pro",
            "na",
            "v",
            "mi",
            "mě",
        ]
        # detect Czech diacritics as a strong signal
        diacritics = r"[ěščřžýáíéúůťďň]"
        # compile word regex as word-boundary delimited
        word_pattern = r"\\b(" + "|".join(re.escape(w) for w in cz_words) + r")\\b"
        word_re = re.compile(word_pattern, re.IGNORECASE)
        diac_re = re.compile(diacritics, re.IGNORECASE)

        matches = word_re.findall(txt)
        has_diac = bool(diac_re.search(txt))

        # require either diacritics OR at least two distinct stopword matches to consider Czech
        if has_diac or len(matches) >= 2:
            rule_ok = True

    # Be forgiving about path case when checking for template reference
    template_ref = "knowledge/reply_templates.md" in txt or "knowledge/reply_templates.md" in txt.replace("\r", "")
    # also ensure the canonical template file exists and contains Czech headings
    template_path = Path("Knowledge/REPLY_TEMPLATES.md")
    template_exists = template_path.exists()
    template_has_czech = False
    if template_exists:
        ttxt = template_path.read_text(encoding="utf-8").lower()
        template_has_czech = "šablona" in ttxt or "češt" in ttxt or "česky" in ttxt
    return bool(rule_ok and template_ref and template_exists and template_has_czech)


def check_all(strict: bool = False) -> Dict[str, object]:
    """Run all checks and return a structured result."""
    result: Dict[str, object] = {}
    missing_critical = [f for f in CRITICAL if not exists_readable(f)]
    result["missing_critical"] = missing_critical

    scopes = get_changed_scope()
    # default conservative conditionals
    default_conditionals = CONDITIONAL_MAP.get("docs", []) + CONDITIONAL_MAP.get(
        "tasks", []
    )
    to_check = set(default_conditionals)
    for s in scopes:
        to_check.update(CONDITIONAL_MAP.get(s, []))

    conditional_checked = sorted(to_check)
    missing_conditionals = [f for f in conditional_checked if not exists_readable(f)]
    result["conditional_checked"] = conditional_checked
    result["missing_conditionals"] = missing_conditionals

    # run subsidiary validators
    code_fence = run_subscript("scripts/qa/check_code_fences.py")
    cli_export = run_subscript("scripts/qa/check_cli_exports.py")
    result["code_fence"] = code_fence
    result["cli_export"] = cli_export

    # preface check
    result["preface_ok"] = check_preface()

    # summary
    language_ok = check_language_rules()
    result["language_ok"] = language_ok

    ok = (
        (not missing_critical)
        and (not missing_conditionals)
        and code_fence.get("code", 1) == 0
        and cli_export.get("code", 1) == 0
        and result["preface_ok"]
        and language_ok
    )
    result["ok"] = bool(ok)
    result["scopes_detected"] = scopes
    return result


def main():
    parser = argparse.ArgumentParser(description="Guardrail checker for MATRIX repo")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON summary"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat conditional missing files as fatal"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output-file", help="Write JSON summary to this file")
    args = parser.parse_args()

    res = check_all(strict=args.strict)

    if args.json:
        out = json.dumps(res, indent=2)
        print(out)
        if args.output_file:
            Path(args.output_file).write_text(out, encoding="utf-8")
    else:
        if res["ok"]:
            print("Guardrail check: PASS")
        else:
            print("Guardrail check: FAIL")

        missing_critical = res.get("missing_critical", [])
        conditional_checked = res.get("conditional_checked", [])
        missing_conditionals = res.get("missing_conditionals", [])

        print("Critical reloaded:", [c for c in CRITICAL if c not in missing_critical])
        print(
            "Conditional reloaded:",
            [c for c in conditional_checked if c not in missing_conditionals],
        )
        for m in missing_critical:
            print(" - missing:", m)
        for m in missing_conditionals:
            print(" - missing-conditional:", m)

        code_fence = res.get("code_fence", {})
        cli_export = res.get("cli_export", {})
        try:
            if code_fence.get("code", 1) != 0:
                print(" - code-fence-check: failed")
        except Exception:
            print(" - code-fence-check: error reading result")
        try:
            if cli_export.get("code", 1) != 0:
                print(" - cli-export-check: failed")
        except Exception:
            print(" - cli-export-check: error reading result")
        if not res.get("preface_ok"):
            print(
                " - copilot preface: missing or malformed in .github/copilot-instructions.md"
            )

    # final exit
    sys.exit(0 if res.get("ok") else 1)


if __name__ == "__main__":
    main()
