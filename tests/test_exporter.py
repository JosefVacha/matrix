import csv
import pathlib
import pandas as pd


def make_test_dataset(path: pathlib.Path):
    # 5 rows of deterministic sample OHLCV-like DataFrame with datetime index
    idx = pd.date_range(start="2025-09-01T00:00:00", periods=5, freq="H")
    df = pd.DataFrame(
        {
            "open": [100 + i for i in range(5)],
            "high": [101 + i for i in range(5)],
            "low": [99 + i for i in range(5)],
            "close": [100 + i for i in range(5)],
            "volume": [10 * (i + 1) for i in range(5)],
            "f_ret_1": [0.01 * i for i in range(5)],
        },
        index=idx,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
    return df


def test_exporter_writes_csv(tmp_path):
    repo_root = pathlib.Path.cwd()
    test_data = tmp_path / "data" / "test_latest.parquet"
    out_csv = tmp_path / "outputs" / "test_predictions.csv"

    # create a small dataset
    df = make_test_dataset(test_data)

    # run exporter function directly
    from scripts.training import export_for_simulator as exporter

    out_path = exporter.export_predictions(
        dataset_path=str(test_data), output=str(out_csv)
    )
    assert out_path.exists()

    # validate CSV structure
    with open(out_path, newline="") as fh:
        reader = csv.reader(fh)
        headers = next(reader)
        assert headers == ["date", "pair", "prediction"]
        rows = list(reader)

    # number of rows should match dataset length
    assert len(rows) == len(df)

    # ensure date column values parse and predictions are numbers
    import datetime

    for r, (idx, _) in zip(rows, df.iterrows()):
        dt_str = r[0]
        # parsing should not raise
        _ = pd.to_datetime(dt_str)
        pred = float(r[2])
        assert not pd.isna(pred)
