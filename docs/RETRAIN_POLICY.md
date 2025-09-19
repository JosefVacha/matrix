# Retrain Cadence Policy


## Cadence Types
- Time-based: retrain if days since last_train > max_days
- Data-based: retrain if new data available or data freshness below threshold
- Drift-based: retrain if drift_metric (e.g. feature/label drift) exceeds threshold

## Inputs
- last_train: ISO date of last training
- min_days: minimum days before retrain allowed
- max_days: maximum days before retrain required
- drift: drift status (none|low|high)
- summaries_dir: directory with summary reports

## Exit Criteria
- Retrain required if (days since last_train > max_days)
- Retrain required if (drift == high and days > min_days)
- Otherwise, retrain not required

## Validator I/O
- Input: CLI args (see check_retrain_cadence.py)
- Output: exit 0 (pass) or 1 (fail), print JSON {"pass": true/false, "reason": "..."}

## Guardrails
- Record commit hashes + TS set
- No feature changes mid-cycle

## Outcome
- New model_tag
- Update model metadata
- Decision note (KEEP/DEPRECATE old)
