import subprocess
import sys
from pathlib import Path


def test_guardrail_fails_when_czech_rule_missing(tmp_path):
    copilot = Path(".github/copilot-instructions.md")
    orig = copilot.read_text(encoding="utf-8")
    try:
        # create a modified version without the Czech rule
        modified = "\n".join(
            [
                l
                for l in orig.splitlines()
                if "czech" not in l.lower() and "češt" not in l.lower()
            ]
        )
        copilot.write_text(modified, encoding="utf-8")
        p = subprocess.run(
            [sys.executable, "scripts/qa/check_copilot_guardrails.py", "--json"],
            capture_output=True,
            text=True,
        )
        assert p.returncode != 0
        assert "language_ok" in p.stdout or "language_ok" in p.stderr
    finally:
        copilot.write_text(orig, encoding="utf-8")
