import json
import os
import subprocess
from pathlib import Path


def test_create_baseline_pr_dry_run(tmp_path, monkeypatch):
    # prepare a fake outputs file
    out_dir = tmp_path / "outputs"
    out_dir.mkdir()
    metrics = {"final_net": 123.45, "trades_count": 2}
    (out_dir / "paper_trade_metrics.json").write_text(json.dumps(metrics))

    # run script with working dir set to tmp_path
    env = os.environ.copy()
    env["GITHUB_REPOSITORY"] = "owner/repo"
    # ensure no tokens present
    env.pop("GITHUB_TOKEN", None)
    env.pop("ALLOW_NOTIFICATIONS", None)

    res = subprocess.run(
        ["python3", str(Path.cwd() / "scripts" / "qa" / "create_baseline_pr.py")],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert "Proposed baseline PR payload" in res.stdout
    assert "Proposed baseline file" in res.stdout
