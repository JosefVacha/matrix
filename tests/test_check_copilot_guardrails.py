import json
import subprocess
import sys


def test_guardrail_checker_json():
    cmd = [sys.executable, "scripts/qa/check_copilot_guardrails.py", "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    assert p.returncode == 0
    out = p.stdout.strip()
    assert out, "expected JSON output"
    data = json.loads(out)
    assert data.get("ok") is True
