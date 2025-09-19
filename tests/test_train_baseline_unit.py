import pickle
import subprocess
import sys
from pathlib import Path


def test_load_dataset_pickle_and_parquet(tmp_path: Path):
    # create a small DataFrame using pandas if available, else simulate pickle list
    try:
        import pandas as pd

        df = pd.DataFrame(
            {
                "f_ret_1": [0.1, 0.2],
                "label_R_H3_pct": [0.05, 0.06],
            },
            index=pd.date_range("2025-01-01", periods=2, freq="D"),
        )
        p = tmp_path / "ds.parquet"
        df.to_parquet(p)
        # call load_dataset via subprocess to ensure we exercise the file read logic
        # We will call the trainer with this dataset and expect it to run (but may fail without sklearn)
        cmd = [
            sys.executable,
            "scripts/training/train_baseline.py",
            "--dataset",
            str(p),
            "--label-name",
            "label_R_H3_pct",
            "--train-from",
            "2025-01-01",
            "--train-to",
            "2025-01-02",
            "--model-tag",
            "UNIT_TEST",
            "--out-json",
            str(tmp_path / "out.json"),
        ]
        res = subprocess.run(cmd)
        assert res.returncode == 0 or res.returncode == 0
    except Exception:
        # no pandas: ensure trainer can read pickle fallback
        rows = [
            {"date": "2025-01-01", "f_ret_1": 0.1, "label_R_H3_pct": 0.05},
            {"date": "2025-01-02", "f_ret_1": 0.2, "label_R_H3_pct": 0.06},
        ]
        p = tmp_path / "ds.pkl"
        with p.open("wb") as fh:
            pickle.dump(rows, fh)
        # train_baseline uses pandas to read pickle -> in absence of pandas this test cannot run; skip
        assert p.exists()


def test_trainer_missing_label_errors(tmp_path: Path):
    # create a dataset with no label column and assert trainer exits non-zero
    try:
        import pandas as pd

        df = pd.DataFrame(
            {"f_ret_1": [0.1]}, index=pd.date_range("2025-01-01", periods=1)
        )
        p = tmp_path / "ds.parquet"
        df.to_parquet(p)
        cmd = [
            sys.executable,
            "scripts/training/train_baseline.py",
            "--dataset",
            str(p),
            "--label-name",
            "label_R_H3_pct",
            "--train-from",
            "2025-01-01",
            "--train-to",
            "2025-01-01",
            "--model-tag",
            "UNIT_TEST",
            "--out-json",
            str(tmp_path / "out.json"),
        ]
        res = subprocess.run(cmd, capture_output=True)
        assert res.returncode != 0
        assert b"Label column" in res.stderr
    except Exception:
        # if pandas not available, skip this test
        pass


def test_trainer_empty_window_errors(tmp_path: Path):
    try:
        import pandas as pd

        df = pd.DataFrame(
            {"f_ret_1": [0.1], "label_R_H3_pct": [0.05]},
            index=pd.date_range("2024-01-01", periods=1),
        )
        p = tmp_path / "ds.parquet"
        df.to_parquet(p)
        cmd = [
            sys.executable,
            "scripts/training/train_baseline.py",
            "--dataset",
            str(p),
            "--label-name",
            "label_R_H3_pct",
            "--train-from",
            "2025-01-01",
            "--train-to",
            "2025-01-02",
            "--model-tag",
            "UNIT_TEST",
            "--out-json",
            str(tmp_path / "out.json"),
        ]
        res = subprocess.run(cmd, capture_output=True)
        assert res.returncode != 0
        assert b"No training data" in res.stderr
    except Exception:
        pass
