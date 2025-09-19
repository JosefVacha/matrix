import json
import subprocess
import sys
from pathlib import Path
import tempfile


def run_notifier_with_input(data: dict):
    p = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    p.write(json.dumps(data).encode())
    p.flush()
    p.close()
    cmd = [
        sys.executable,
        "scripts/qa/notify_guardrail_failure.py",
        "--input-file",
        p.name,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr, Path(p.name)


def test_notifier_writes_artifact_on_failure(tmp_path):
    data = {"ok": False, "reason": "simulated"}
    code, out, inp = run_notifier_with_input(data)
    # notifier returns 1 on failure after writing artifact
    assert code == 1
    # find artifact in outputs/
    outputs = list(Path("outputs").glob("guardrail_failure-*.json"))
    assert outputs, "Expected an artifact written to outputs/"
    # cleanup created files
    for f in outputs:
        try:
            f.unlink()
        except Exception:
            pass
    inp.unlink()


def test_notifier_ok_return_code(tmp_path):
    data = {"ok": True}
    code, out, inp = run_notifier_with_input(data)
    assert code == 0
    # no artifact should be left in outputs
    outputs = list(Path("outputs").glob("guardrail_failure-*.json"))
    assert not outputs
    inp.unlink()
