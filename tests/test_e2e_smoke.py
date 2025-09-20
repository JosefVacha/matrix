import json
import subprocess
import sys
from pathlib import Path


def test_e2e_smoke(tmp_path: Path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    dataset = out_dir / "dataset_SMOKE.pkl"
    # run the generator to create dataset inside tmp
    subprocess.check_call([sys.executable, "-m", "scripts.qa.generate_smoke_dataset"])
    # the repo generator writes to data/ by default; copy it into tmp
    repo_dataset = Path("data/dataset_SMOKE.pkl")
    assert repo_dataset.exists(), "Generator did not produce dataset in repo data/"
    dataset.write_bytes(repo_dataset.read_bytes())

    out_json = out_dir / "summary.json"
    cmd = [
        sys.executable,
        "scripts/run_smoke_local.py",
        "--dataset",
        str(dataset),
        "--label-name",
        "label_R_H3_pct",
        "--out-json",
        str(out_json),
        "--model-tag",
        "TMP_SMOKE",
        "--no-save-model",
    ]
    subprocess.check_call(cmd)

    assert out_json.exists(), "Runner did not produce summary JSON"
    data = json.loads(out_json.read_text())
    assert "metrics" in data and "train" in data
    assert data["train"]["n"] > 0
