#!/usr/bin/env python3
"""
Idempotent registry skeleton creator for models/<tag>/metadata.json
Usage:
  python scripts/registry/init_model_tag.py --tag M3_DEMO
"""

import argparse
import pathlib
import json
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(
        description="Init model registry metadata skeleton"
    )
    parser.add_argument("--tag", required=True)
    args = parser.parse_args()
    tag = args.tag
    meta_dir = pathlib.Path(f"models/{tag}")
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_path = meta_dir / "metadata.json"
    # Skeleton metadata
    skeleton = {
        "model_tag": tag,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": "<label>",
        "features": [],
        "timeframe": None,
        "train_window": {"from": "", "to": "", "rows": 0},
        "algo": {"name": "ridge", "params": {"alpha": 0.1}},
        "artifacts": {"pickle_path": None},
        "provenance": {
            "dataset_path": "<dataset_path>",
            "commit": None,
            "generator": "scripts/registry/init_model_tag.py",
        },
    }
    # Idempotent update: merge skeleton into existing, preserve unknown fields
    if meta_path.exists():
        try:
            with open(meta_path) as f:
                old = json.load(f)
        except Exception:
            old = {}
        for k, v in skeleton.items():
            if k not in old:
                old[k] = v
        meta = old
    else:
        meta = skeleton
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Initialized registry metadata: {meta_path}")


if __name__ == "__main__":
    main()
