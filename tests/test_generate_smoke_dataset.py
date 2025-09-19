def test_generate_smoke_dataset(tmp_path):
    out = tmp_path / "dataset_SMOKE.parquet"
    # import local generator
    from scripts.qa.generate_smoke_dataset import generate

    p = generate(str(out))
    assert p.exists()

    # Load either parquet (pandas) or fallback pickle (either pandas pickle or pickled rows)
    if p.suffix == ".parquet":
        import pandas as pd

        df = pd.read_parquet(p)
        for c in ["f_ret_1", "f_ret_3", "f_vol_12", "label_R_H3"]:
            assert c in df.columns
        assert df.index.is_monotonic_increasing
    else:
        # The fallback could be either a pandas pickle (DataFrame) or a pickled list-of-dicts
        import pickle

        with p.open("rb") as fh:
            obj = pickle.load(fh)
        if isinstance(obj, list):
            # list of dicts
            assert len(obj) > 0
            row = obj[0]
            for k in ["date", "f_ret_1", "f_ret_3", "f_vol_12", "label_R_H3"]:
                assert k in row
        else:
            # assume pandas object
            import pandas as pd

            df = obj
            for c in ["f_ret_1", "f_ret_3", "f_vol_12", "label_R_H3"]:
                assert c in df.columns
            assert df.index.is_monotonic_increasing
