import subprocess
import sys


def test_reply_template_presence_ok():
    p = subprocess.run(
        [sys.executable, "scripts/qa/check_reply_template_presence.py"],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, f"Checker failed: {p.stdout}\n{p.stderr}"
    assert "OK" in p.stdout
