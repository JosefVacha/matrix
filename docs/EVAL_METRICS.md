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
