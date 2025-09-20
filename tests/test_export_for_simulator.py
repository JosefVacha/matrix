import pandas as pd
from pathlib import Path

from scripts.training import export_for_simulator as exporter


def test_reindex_predictions(tmp_path: Path):
    # Create a tiny smoke dataset with a datetime index
    idx = pd.date_range("2020-01-01", periods=4, freq="D")
    smoke = pd.DataFrame({"close": [1, 2, 3, 4]}, index=idx)
    smoke_path = tmp_path / "smoke.parquet"
    smoke.to_parquet(smoke_path)

    # Create a small predictions CSV that misses one timestamp
    pred_df = pd.DataFrame(
        {
            "datetime": [idx[0].isoformat(), idx[2].isoformat()],
            "prediction": [0.5, -0.2],
        }
    )
    pred_csv = tmp_path / "preds.csv"
    pred_df.to_csv(pred_csv, index=False)

    # Load smoke index and reindex predictions
    index = exporter.load_smoke_index(str(smoke_path))
    out = exporter.reindex_predictions(pd.read_csv(pred_csv), index)

    # Should have 4 rows, missing filled with 0.0
    assert len(out) == 4
    # Predictions present at positions 0 and 2
    assert out.iloc[0]["prediction"] == 0.5
    assert out.iloc[2]["prediction"] == -0.2
    # Missing entries filled with 0.0
    assert out.iloc[1]["prediction"] == 0.0
    assert out.iloc[3]["prediction"] == 0.0
