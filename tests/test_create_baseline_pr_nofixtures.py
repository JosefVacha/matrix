import json
import os
import subprocess
import tempfile
from pathlib import Path


def run_dry_run_and_capture():
    td = Path(tempfile.mkdtemp())
    # setup minimal repo layout
    (td / "outputs").mkdir()
    metrics = {"final_net": 42.0, "trades_count": 1}
    (td / "outputs" / "paper_trade_metrics.json").write_text(json.dumps(metrics))
    # copy script
    from shutil import copyfile

    copyfile("scripts/qa/create_baseline_pr.py", str(td / "create_baseline_pr.py"))
    # run dry-run
    env = os.environ.copy()
    env["GITHUB_REPOSITORY"] = "owner/repo"
    p = subprocess.run(
        ["python3", "create_baseline_pr.py"],
        cwd=td,
        capture_output=True,
        text=True,
        env=env,
    )
    return p


if __name__ == "__main__":
    res = run_dry_run_and_capture()
    print("returncode=", res.returncode)
    print(res.stdout)
    if res.returncode != 0:
        raise SystemExit("dry-run test failed")
