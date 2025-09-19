"""Zero-deps guardrail test runner.

Run with:
    python3 -m tests.test_guardrails

Exits 0 on pass, 1 on fail. Prints machine-readable single-line status.
"""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/qa/check_copilot_guardrails.py")
COPILOT = Path(".github/copilot-instructions.md")

EXPECTED_PREFACE = (
    "Guardrail check: ran check_copilot_guardrails.py — PASS\n"
    "Files reloaded: copilot-instructions.md, AGENTS.md, PROJECT_STATE.md"
)

def main():
    # 1) script exists and returns 0
    if not SCRIPT.exists():
        print("guardrails_test: fail:guardrail-script-missing")
        sys.exit(1)
    p = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"guardrails_test: fail:guardrail-script-failed(rc={p.returncode})")
        sys.exit(1)

    # 2) check the literal preface block appears in copilot-instructions.md
    if not COPILOT.exists():
        print("guardrails_test: fail:copilot-instructions-missing")
        sys.exit(1)
    text = COPILOT.read_text(encoding="utf-8")
    # Normalize line endings and strip trailing spaces for match
    normalized = "\n".join([ln.rstrip() for ln in text.splitlines()])
    if EXPECTED_PREFACE not in normalized:
        # If the literal preface lines are missing, fail. If they are present
        # but the Audit Preface heading is missing, that's non-fatal.
        print("guardrails_test: fail:preface-not-found")
        sys.exit(1)
    # optional: check for the Audit Preface heading and note if missing
    if "## Audit Preface" not in normalized:
        print("note: '## Audit Preface' heading not found (ok, preface lines present)")

    print("guardrails_test: pass")
    sys.exit(0)

if __name__ == '__main__':
    main()
