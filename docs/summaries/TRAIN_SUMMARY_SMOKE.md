# TRAIN SUMMARY — SMOKE

<!-- RUN_META -->
Keys from summary JSON:
- run_tag: str
- label: str
- features: list[str]
- train: {from: str, to: str, n: int}
- model: {type: str, alpha/lmbd: float}
- metrics: {mae: float, mse: float, r2: float, resid_mean: float, resid_std: float}
- created_at: str (ISO-8601)

<!-- MODEL_META -->
Keys from models/<tag>/metadata.json (types):
- model_tag: str
- created_at: str
- label: str
- features: list[str]
- timeframe: str or null
- train_window: {from: str, to: str, rows: int}
- algo: {name: str, params: dict}
- artifacts: {pickle_path: str or null}
- provenance: {dataset_path: str, commit: str or null, generator: str}

<!-- METRICS -->
Example metrics block:
```
{
  "mae": 0.012,
  "mse": 0.0002,
  "r2": 0.98,
  "resid_mean": 0.0001,
  "resid_std": 0.01
}
```

<!-- NOTES -->
- All outputs are offline, deterministic, and contract-compliant.
- Registry metadata is idempotent and preserves unknown fields.
- See TRAINING_PROTOCOL.md and MODEL_REGISTRY.md for full schema.
