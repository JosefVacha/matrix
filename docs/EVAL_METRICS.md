# Evaluation Metrics (Stub)

## Regression proxies

## Signal hygiene

## Risk proxies

## Aggregation

## Mapping to SUMMARY markers
| metric         | marker key         |
|----------------|-------------------|
| MAE            | mae               |
| MAPE           | mape              |
| R² proxy       | r2_proxy          |
| trigger_rate   | trigger_rate      |
| churn_rate     | churn_rate        |
| max drawdown   | max_dd            |
| exposure       | exposure          |

## H-consistency Usage
```bash
# H-consistency — verify label ↔ window ↔ H linkage (exit 0 = OK, non-zero = mismatch)
python scripts/qa/check_H_consistency.py \
	--label-name label_R_H12_pct \
	--windows 1,3,12 \
	--H 12
```

## H-consistency gate
Use this gate to ensure the label, windows and horizon (H) are consistent before reporting metrics.

CLI usage (exit codes):
- 0 = OK (consistency verified)
- non-zero = mismatch or error

Example output:
```bash
$ python3 scripts/qa/check_H_consistency.py --label-name label_R_H12_pct --windows 1,3,12 --H 12
OK: checked label label_R_H12_pct with H=12 and windows=[1,3,12]
exit: 0
```

## H-consistency usage
Run the H-consistency gate before reporting metrics:

```bash
python3 scripts/qa/check_H_consistency.py --label-name <label-name> --windows <w1,w2,...> --H <H>
```
