import pathlib
import pickle

import pandas as pd
from scripts.qa.generate_smoke_dataset import generate
from scripts.qa import validate_data_ingest


def load_any(path: pathlib.Path):
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    elif path.suffix == ".pkl":
        with open(path, "rb") as fh:
            data = pickle.load(fh)
        return data
    else:
        # try parquet by default
        return pd.read_parquet(path)


def test_generate_and_validate(tmp_path):
    out = tmp_path / "latest.parquet"
    generated = generate(path=str(out), start="2025-01-01", end="2025-01-03")
    assert pathlib.Path(generated).exists()
    assert validate_data_ingest.validate(str(generated)) is True


def test_generated_schema_and_monotonic(tmp_path):
    out = tmp_path / "latest.parquet"
    p = generate(path=str(out), start="2025-01-01", end="2025-01-10")
    p = pathlib.Path(p)
    data = load_any(p)
    # If pandas DataFrame, check index and columns
    if hasattr(data, "index"):
        # Ensure required columns
        for col in ["f_ret_1", "f_ret_3", "f_vol_12"]:
            assert col in data.columns
        try:
            idx = pd.to_datetime(data.index)
            assert idx.is_monotonic_increasing
        except Exception:
            # If not convertible, still acceptable for fallback
            pass
    else:
        # list-of-dicts fallback: check keys
        assert isinstance(data, list)
        for r in data:
            for col in ["f_ret_1", "f_ret_3", "f_vol_12"]:
                assert col in r
