# WFO Metrics Template

Filled by scripts/training/evaluate_wfo.py

| train_from | train_to | test_from | test_to | n | nan_ratio | trigger_rate | mean_R | hit_rate | dd_min |
|------------|----------|-----------|---------|---|-----------|-------------|--------|----------|--------|
| <PH>       | <PH>     | <PH>      | <PH>    | <PH> | <PH>      | <PH>        | <PH>   | <PH>     | <PH>   |

## JSON keys example
```
{
  "run_tag": "SMOKE_2D",
  "label": "label_R_H3_pct",
  "params": {"block_days":2,"gap_days":0,"from":"2025-01-01","to":"2025-01-10"},
  "blocks": [
    {"train_from":"...","train_to":"...","test_from":"...","test_to":"...",
     "n":123, "nan_ratio":0.0, "trigger_rate":0.42, "mean_R":0.0012, "hit_rate":0.52, "dd_min":-0.05}
  ]
}
```
