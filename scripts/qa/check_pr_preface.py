#!/usr/bin/env python3
"""Check that a PR body begins with the mandatory audit preface.

Usage (CI - automatic): the script reads GITHUB_EVENT_PATH env var set by Actions
and extracts pull_request.body. Locally you can pass --file PATH to check a body
file.
"""
import argparse
import json
import os
import sys
from pathlib import Path


MANDATORY_LINE1 = "Guardrail check: ran check_copilot_guardrails.py — PASS"
MANDATORY_LINE2 = (
    "Files reloaded: copilot-instructions.md, AGENTS.md, PROJECT_STATE.md"
)


def body_from_event(event_path: str) -> str:
    try:
        ev = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except Exception:
        return ""
    # pull_request body
    body = ev.get("pull_request", {}).get("body")
    if body:
        return body
    # fallback: issue body
    return ev.get("issue", {}).get("body", "") or ""


def check_body(body: str) -> bool:
    if not body:
        return False
    # normalize beginning (strip leading whitespace)
    lines = body.lstrip().splitlines()
    if len(lines) < 2:
        return False
    l1 = lines[0].strip()
    l2 = lines[1].strip()
    # allow conditional suffix in second line (e.g., [+ conditional: ...])
    if l1 != MANDATORY_LINE1:
        return False
    if not l2.startswith("Files reloaded:"):
        return False
    # ensure core trio is present
    if "copilot-instructions.md" not in l2 or "AGENTS.md" not in l2 or "PROJECT_STATE.md" not in l2:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Check PR body for audit preface")
    parser.add_argument("--file", help="Path to a file containing the PR body (local)")
    args = parser.parse_args()

    body = ""
    if args.file:
        body = Path(args.file).read_text(encoding="utf-8")
    else:
        evp = os.environ.get("GITHUB_EVENT_PATH")
        if evp:
            body = body_from_event(evp)

    ok = check_body(body)
    if ok:
        print("PR preface: OK")
        sys.exit(0)
    else:
        print("PR preface: MISSING or malformed. PR body must start with the audit preface (two lines).")
        print("Required first line:")
        print(MANDATORY_LINE1)
        print("Required second line must start with 'Files reloaded:' and contain copilot-instructions.md, AGENTS.md, PROJECT_STATE.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
