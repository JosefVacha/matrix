import pathlib
from scripts.qa import generate_smoke_dataset



def test_generate_writes_file(tmp_path):
    out = tmp_path / "latest.parquet"
    path = generate_smoke_dataset.generate(path=str(out), start="2025-01-01", end="2025-01-07")
    assert pathlib.Path(path).exists()


def test_generate_deterministic(tmp_path):
    out1 = tmp_path / "a.parquet"
    out2 = tmp_path / "b.parquet"
    p1 = generate_smoke_dataset.generate(path=str(out1), start="2025-01-01", end="2025-01-07")
    p2 = generate_smoke_dataset.generate(path=str(out2), start="2025-01-01", end="2025-01-07")
    # Prefer comparing DataFrame content when pandas is available; fallback to binary compare
    try:
        import pandas as pd

        df1 = pd.read_parquet(p1) if p1.suffix == ".parquet" else pd.read_pickle(p1)
        df2 = pd.read_parquet(p2) if p2.suffix == ".parquet" else pd.read_pickle(p2)
        # Use equals (index and values) for determinism
        assert df1.equals(df2)
    except Exception:
        with open(p1, "rb") as f1, open(p2, "rb") as f2:
            b1 = f1.read()
            b2 = f2.read()
        assert b1 == b2
