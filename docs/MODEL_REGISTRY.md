# MATRIX Model Registry

## Naming Convention
- <model_tag> = date_modeltype_H_notes

## Metadata Schema

Each model registry entry is stored in models/<model_tag>/metadata.json. Update idempotently after each training run.

Required keys:
```
{
	"model_tag": "M3_SMOKE_RH3",
	"created_at": "ISO-8601",
	"label": "label_R_H3_pct",
	"features": ["f_ret_1","f_ret_3","f_vol_12"],
	"timeframe": "5m",  # or null
	"train_window": {"from":"YYYY-MM-DD","to":"YYYY-MM-DD","rows":123},
	"algo": {"name":"ridge","params":{"alpha":0.1}},
	"artifacts": {"pickle_path":"models/M3_SMOKE_RH3/model.pkl"},
	"provenance": {
		"dataset_path":"data/dataset_SMOKE.parquet",
		"commit": "<git sha1>",
		"generator":"scripts/training/train_baseline.py"
	}
}
```

Notes:
- All fields must be present; unknown fields are preserved on update.
- Pickle path may be null if not saved.
- Timeframe is inferred if possible, else null.
- Commit is git SHA1 if available.

### Example
```
{
	"model_tag": "M3_SMOKE_RH3",
	"created_at": "2025-09-19T12:34:56Z",
	"label": "label_R_H3_pct",
	"features": ["f_ret_1","f_ret_3","f_vol_12"],
	"timeframe": "5m",
	"train_window": {"from":"2025-01-01","to":"2025-01-08","rows":123},
	"algo": {"name":"ridge","params":{"alpha":0.1}},
	"artifacts": {"pickle_path":"models/M3_SMOKE_RH3/model.pkl"},
	"provenance": {
		"dataset_path":"data/dataset_SMOKE.parquet",
		"commit": "df0bd96",
		"generator":"scripts/training/train_baseline.py"
	}
}
```


## Registry Helpers

- [Schema: model_metadata.schema.json](../docs/schemas/model_metadata.schema.json)

### CLI Usage
Init registry skeleton:
```bash
python scripts/registry/init_model_tag.py --tag M3_DEMO
```
Validate registry metadata:
```bash
python scripts/qa/validate_model_metadata.py --file models/M3_DEMO/metadata.json --schema docs/schemas/model_metadata.schema.json
```

### Example
See above for full metadata example.

## Schema (JSON)
Refer to the canonical schema at `docs/schemas/model_metadata.schema.json` (draft-07).

## CLI helpers
Init a model tag (idempotent skeleton):
```bash
python scripts/registry/init_model_tag.py --tag BASELINE_LIN_H3 --out models/BASELINE_LIN_H3/metadata.json
```

Validate metadata file against schema:
```bash
python scripts/qa/validate_model_metadata.py --file models/BASELINE_LIN_H3/metadata.json --schema docs/schemas/model_metadata.schema.json
```

## Example metadata.json
```json
{
	"model_tag": "BASELINE_LIN_H3",
	"created_at": "2025-09-19T12:00:00Z",
	"label": "label_R_H3_pct",
	"timeframe": "5m",
	"features": ["f_ret_1", "f_ret_3", "f_ret_12", "f_oc_range", "f_vol_z"],
	"trainer": {"type": "linear", "alpha": 0.1},
	"provenance": {"commit": "<GIT_SHA>", "builder": "train_baseline.py"},
	"metrics": {"wfo_blocks": 0, "mean_R": null, "hit_rate": null},
	"notes": "Initialized for offline experiments; metrics to be filled after WFO run."
}
```

Notes: the example is intentionally lightweight (no binary artifacts). Use the CLI helpers above to init and validate.
