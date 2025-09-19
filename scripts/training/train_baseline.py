# Minimal offline training runner for baseline models
# Compatible with numpy, pandas, and optionally scikit-learn (Ridge)
# Usage: see TRAINING_PROTOCOL.md

import argparse
import pathlib
import sys
import json
import datetime
import numpy as np
import pandas as pd

try:
    from sklearn.linear_model import Ridge

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# --- Helpers ---
def load_dataset(path):
    path = pathlib.Path(path)
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix == ".pkl":
        df = pd.read_pickle(path)
    else:
        raise ValueError(f"Unsupported dataset format: {path.suffix}")
    if not df.index.is_monotonic_increasing:
        raise ValueError("Dataset index must be monotonic increasing (UTC)")
    return df


def select_features(df, features):
    if features:
        return [f for f in features if f in df.columns]
    # Default: all columns starting with 'f_'
    return [c for c in df.columns if c.startswith("f_")]


def right_align_train(df, train_from, train_to):
    # Assumes index is datetime
    mask = (df.index >= train_from) & (df.index <= train_to)
    return df.loc[mask]


def train_ridge(X, y, alpha):
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    y_pred = model.predict(X)
    return model, y_pred


def train_ols_tikhonov(X, y, lmbd):
    # OLS with Tikhonov regularization: (X^T X + lmbd*I)^-1 X^T y
    X_ = np.asarray(X)
    y_ = np.asarray(y)
    n_features = X_.shape[1]
    A = X_.T @ X_ + lmbd * np.eye(n_features)
    b = X_.T @ y_
    coef = np.linalg.solve(A, b)
    y_pred = X_ @ coef

    class Model:
        def __init__(self, coef):
            self.coef_ = coef

        def predict(self, X):
            return np.asarray(X) @ self.coef_

    return Model(coef), y_pred


def compute_metrics(y_true, y_pred):
    resid = y_true - y_pred
    mae = float(np.mean(np.abs(resid)))
    mse = float(np.mean(resid**2))
    r2 = (
        float(1 - np.sum(resid**2) / np.sum((y_true - np.mean(y_true)) ** 2))
        if len(y_true) > 1
        else float("nan")
    )
    return {
        "mae": mae,
        "mse": mse,
        "r2": r2,
        "resid_mean": float(np.mean(resid)),
        "resid_std": float(np.std(resid)),
    }


def save_json(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def save_pickle(obj, path):
    import pickle

    with open(path, "wb") as f:
        pickle.dump(obj, f)


def update_metadata(meta_path, new_meta):
    # Idempotent update: merge new_meta into existing, preserve unknown fields
    meta_path = pathlib.Path(meta_path)
    if meta_path.exists():
        try:
            with open(meta_path) as f:
                old = json.load(f)
        except Exception:
            old = {}
        old.update(new_meta)
        meta = old
    else:
        meta = new_meta
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)


# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(description="Offline baseline model trainer")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--label-name", required=True)
    parser.add_argument("--features", default="", help="Comma-separated feature names")
    parser.add_argument("--train-from", required=True)
    parser.add_argument("--train-to", required=True)
    parser.add_argument("--model-tag", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--save-model", required=False)
    parser.add_argument(
        "--alpha", type=float, default=0.1, help="Ridge alpha (if sklearn)"
    )
    parser.add_argument(
        "--lmbd", type=float, default=0.0, help="OLS regularization (if no sklearn)"
    )
    args = parser.parse_args()

    df = load_dataset(args.dataset)
    features = (
        [f.strip() for f in args.features.split(",") if f.strip()]
        if args.features
        else []
    )
    features = select_features(df, features)
    if args.label_name not in df.columns:
        print(f"Label column {args.label_name} not found in dataset.", file=sys.stderr)
        sys.exit(1)
    df_train = right_align_train(df, args.train_from, args.train_to)
    X = df_train[features].values
    y = df_train[args.label_name].values
    if len(X) == 0 or len(y) == 0:
        print("No training data in selected window.", file=sys.stderr)
        sys.exit(1)

    # Train model
    if SKLEARN_AVAILABLE:
        model, y_pred = train_ridge(X, y, args.alpha)
        model_type = {"type": "ridge", "alpha": args.alpha}
        algo = {"name": "ridge", "params": {"alpha": args.alpha}}
    else:
        model, y_pred = train_ols_tikhonov(X, y, args.lmbd)
        model_type = {"type": "ols", "lmbd": args.lmbd}
        algo = {"name": "ols", "params": {"lmbd": args.lmbd}}
    metrics = compute_metrics(y, y_pred)
    created_at = datetime.datetime.utcnow().isoformat()

    # Save summary JSON
    summary = {
        "run_tag": args.model_tag,
        "label": args.label_name,
        "features": features,
        "train": {
            "from": args.train_from,
            "to": args.train_to,
            "n": int(len(df_train)),
        },
        "model": model_type,
        "metrics": metrics,
        "created_at": created_at,
    }
    save_json(summary, args.out_json)

    # Save model pickle (optional)
    pickle_path = None
    if args.save_model:
        save_pickle(model, args.save_model)
        pickle_path = str(args.save_model)

    # Write registry metadata
    meta_dir = pathlib.Path(f"models/{args.model_tag}")
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_path = meta_dir / "metadata.json"
    # Try to infer timeframe from dataset name (simple heuristic)
    tf = None
    if "5m" in str(args.dataset):
        tf = "5m"
    meta = {
        "model_tag": args.model_tag,
        "created_at": created_at,
        "label": args.label_name,
        "features": features,
        "timeframe": tf,
        "train_window": {
            "from": args.train_from,
            "to": args.train_to,
            "rows": int(len(df_train)),
        },
        "algo": algo,
        "artifacts": {"pickle_path": pickle_path},
        "provenance": {
            "dataset_path": str(args.dataset),
            "commit": get_git_sha1(),
            "generator": "scripts/training/train_baseline.py",
        },
    }
    update_metadata(meta_path, meta)


# --- Git SHA1 helper ---
def get_git_sha1():
    import subprocess

    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=pathlib.Path(__file__).parent.parent.parent,
            stderr=subprocess.DEVNULL,
        )
        return sha.decode().strip()
    except Exception:
        return None


if __name__ == "__main__":
    main()
