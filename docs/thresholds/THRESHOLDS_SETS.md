# THRESHOLDS_SETS.md

## Threshold Set Versioning for MATRIX Sandbox

### Naming Convention
Threshold set files are named as follows:
```
TS_<YYYYMMDD>_<H>_<model-tag>_<notes>.yml
```
- `<YYYYMMDD>`: Date of creation
- `<H>`: Label horizon (e.g., H12)
- `<model-tag>`: Model identifier (e.g., lgbm_v1)
- `<notes>`: Short descriptor (e.g., grid, stable, test)

**Example:**
```
TS_20241219_H12_lgbm_v1_grid.yml
```

### Threshold Set File Structure
Each threshold set YAML file contains:
```yaml
meta:
  created_at: <YYYY-MM-DD>
  author: <name>
  commit: <git hash>
  timeframe: <e.g., 5m>
  pairlist_ref: <pairlist file>
  model_tag: <model identifier>
params:
  UP: <float>
  DN: <float>
  hysteresis: <float>
  cooldown: <int>
  label:
    mode: <e.g., regression>
    H: <int>
provenance:
  report_ref: <REPORT_TEMPLATE.md section or file>
  wfo_blocks: <number>
  notes: <freeform>
```

### Usage
- Select a threshold set for each sandbox run.
- Link chosen set in REPORT_TEMPLATE.md under "Chosen Threshold Set".
- Document provenance and rationale for each set.
- Update stability score after each run.

### Example Template
See `docs/thresholds/sets/TS_YYYYMMDD_TEMPLATE.yml` for a placeholder file structure.