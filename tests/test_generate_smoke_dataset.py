import pandas as pd


def test_generate_smoke_dataset(tmp_path):
    out = tmp_path / "dataset_SMOKE.parquet"
    # import local generator
    from scripts.qa.generate_smoke_dataset import generate

    p = generate(str(out))
    assert p.exists()

    # Load either parquet or pickle depending on what generator created
    if p.suffix == ".parquet":
        df = pd.read_parquet(p)
    else:
        df = pd.read_pickle(p)
    # Expect at least these columns
    for c in ["f_ret_1", "f_ret_3", "f_vol_12", "label_R_H3"]:
        assert c in df.columns

    assert df.index.is_monotonic_increasing
