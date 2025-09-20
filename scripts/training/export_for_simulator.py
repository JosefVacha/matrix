"""Export predictions for the paper-trading simulator.

Two safe modes:
 - --model-pickle: load a local sklearn-like model pickle and produce predictions for the smoke dataset index
 - --predictions-csv: reindex an existing CSV to the smoke dataset index (fill missing with 0.0)

This script is offline-only and does not contact external services.
"""
import argparse
import pandas as pd
from pandas import DatetimeIndex


def load_smoke_index(smoke_path: str) -> DatetimeIndex:
    df = pd.read_parquet(smoke_path)
    # Expect a datetime index; if not, try common column names
    if isinstance(df.index, pd.DatetimeIndex):
        return df.index
    for col in ("date", "datetime", "timestamp"):  # common fallbacks
        if col in df.columns:
            return pd.DatetimeIndex(pd.to_datetime(df[col]))
    raise RuntimeError("Cannot determine datetime index from smoke dataset")


def reindex_predictions(pred_df: pd.DataFrame, index: DatetimeIndex) -> pd.DataFrame:
    pred_df = pred_df.copy()
    # Ensure datetime column named 'datetime'
    if "datetime" not in pred_df.columns:
        possible = [c for c in pred_df.columns if "date" in c or "time" in c]
        if not possible:
            raise RuntimeError("No datetime column in predictions CSV")
        pred_df = pred_df.rename(columns={possible[0]: "datetime"})
    pred_df["datetime"] = pd.to_datetime(pred_df["datetime"])
    pred_df = pred_df.set_index("datetime")
    pred_df = pred_df.reindex(index)
    if "prediction" not in pred_df.columns:
        # If there's a single unnamed column, try to use it
        cols = [c for c in pred_df.columns]
        if cols:
            pred_df = pred_df.rename(columns={cols[0]: "prediction"})
        else:
            pred_df["prediction"] = 0.0
    pred_df["prediction"] = pred_df["prediction"].fillna(0.0)
    return pred_df[["prediction"]].reset_index().rename(columns={"index": "datetime"})


def predict_from_pickle(pickle_path: str, index: DatetimeIndex, features_fn=None) -> pd.DataFrame:
    try:
        import joblib
    except Exception:
        raise RuntimeError("joblib is required to load model pickles. Install it in your environment.")

    model = joblib.load(pickle_path)
    # features_fn(index) should return a DataFrame X aligned to index
    if features_fn is None:
        # Fall back to a dummy features DataFrame of zeros matching index length
        X = pd.DataFrame(0.0, index=index, columns=["feat_dummy"])
    else:
        X = features_fn(index)

    # Try common predict interfaces
    if hasattr(model, "predict_proba"):
        preds = model.predict_proba(X)[:, 1]
    elif hasattr(model, "predict"):
        preds = model.predict(X)
    else:
        raise RuntimeError("Model object has no predict/predict_proba method")

    out = pd.DataFrame({"datetime": index, "prediction": preds})
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--smoke", default="data/dataset_SMOKE.parquet", help="Path to smoke dataset")
    p.add_argument("--model-pickle", default=None, help="Path to a local model pickle")
    p.add_argument("--predictions-csv", default=None, help="Existing predictions CSV to reindex")
    p.add_argument("--output", default="predictions.csv", help="Output CSV path")
    args = p.parse_args()

    index = load_smoke_index(args.smoke)
    if args.predictions_csv:
        pred = pd.read_csv(args.predictions_csv)
        out = reindex_predictions(pred, index)
    elif args.model_pickle:
        out = predict_from_pickle(args.model_pickle, index)
    else:
        raise SystemExit("Provide either --model-pickle or --predictions-csv")

    out.to_csv(args.output, index=False, date_format="%Y-%m-%dT%H:%M:%S")
    print(f"Wrote predictions to {args.output}")


if __name__ == "__main__":
    main()
