import json
from pathlib import Path
import subprocess


def test_aggregate_outputs(tmp_path):
    out = tmp_path / "outputs"
    out.mkdir()
    # create a guardrail file
    guard = out / "guardrail_check.json"
    guard.write_text(
        json.dumps({"ok": True, "preface_ok": True, "language_ok": True}),
        encoding="utf-8",
    )
    # create another file
    other = out / "foo.json"
    other.write_text(json.dumps({"a": 1}), encoding="utf-8")

    # run the aggregator script in tmp_path
    script = Path.cwd() / "scripts" / "qa" / "aggregate_outputs.py"
    res = subprocess.run(["python3", str(script)], cwd=tmp_path)
    assert res.returncode == 0
    summary = out / "summary.json"
    assert summary.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["guardrail"]["ok"] is True
