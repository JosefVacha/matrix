# MATRIX

![guardrails](https://github.com/JosefVacha/matrix/actions/workflows/smoke-validators.yml/badge.svg)
![paper-trade smoke (manual)](https://github.com/JosefVacha/matrix/actions/workflows/paper_trade_smoke.yml/badge.svg)
![paper-trade smoke (weekly)](https://github.com/JosefVacha/matrix/actions/workflows/ci_paper_trade_smoke.yml/badge.svg)
![propose baseline PR](https://github.com/JosefVacha/matrix/actions/workflows/propose_baseline_pr.yml/badge.svg)

MATRIX = thin modular layer over Freqtrade + FreqAI; Superalgos only as mental node map.

## What is MATRIX

MATRIX is a thin, modular layer built on top of the Freqtrade and FreqAI framework, providing a structured approach to algorithmic trading. The project uses node concepts inspired by Superalgos for better pipeline organization.

## Pipeline Map

```
sensor(OHLCV) → feature(gen) → trainer(FreqAI) → server(FreqAI.predict) → strategy → risk → execution(Freqtrade)
```

### Main Components:
- **Sensor**: OHLCV data acquisition
- **Feature Engineering**: FreqAI-compatible feature generation
- **Trainer**: Model training using FreqAI
- **Prediction Server**: Inference using FreqAI
- **Strategy**: Converting predictions to trading signals
- **Risk Management**: Risk control
- **Execution**: Trade execution via Freqtrade

## ⚠️ SECURITY WARNING ⚠️

**THIS PROJECT IS IN DEVELOPMENT PHASE - NO API KEYS, NO LIVE TRADING!**

- Do not use production API keys
- Do not perform live trading
- All tests only with paper money or backtests

## Documentation and Links

- [Freqtrade Documentation](https://www.freqtrade.io/)
- [FreqAI Documentation](https://www.freqtrade.io/en/stable/freqai/)
- [Superalgos Documentation](https://superalgos.org/) (conceptual inspiration)
 - [Notifier usage and safe enablement](docs/NOTIFIER_USAGE.md)
 - [RUNBOOK (maintainer playbook)](Knowledge/RUNBOOK.md)

## Getting Started

### Configuration
1. Copy `configs/*.example.json` → `configs/*.json`
2. Fill in local settings (API keys, paths) - **configs/*.json are in .gitignore**
3. Never push production configuration to Git

### Backtesting
**For backtests use `configs/pairlist.static.json`** - guarantees reproducible results. In live/dry the pairlist can be different, but don't drag it into BT.

*Detailed documentation will be added during project development.*

### Guardrails quick check

Run the guardrail script directly:

```bash
python3 scripts/qa/check_copilot_guardrails.py
```

Run the stdlib-only unit test (exits 0 on pass; prints `guardrails_test: pass`):

```bash
python3 -m tests.test_guardrails
```

## License

MIT License - viz LICENSE soubor.

## Developer commands

Run quick developer checks using the repository Makefile:

- `make precommit` — run pre-commit hooks locally
- `make detect-secrets-scan` — run a detect-secrets scan using the repository baseline (if present)
- `make venv` — create a local virtualenv and install dev requirements

## Smoke-run CI and local reproduction

The repository includes a deterministic smoke dataset generator, a small paper-trading simulator, and CI jobs that run nightly/manual smoke-runs.

To reproduce the smoke-run locally:

```bash
# create venv (if not already created)
make venv
source .venv/bin/activate

# generate the canonical smoke dataset (30 days example)
python3 scripts/qa/generate_smoke_dataset.py --path data/dataset_SMOKE.parquet --days 30

# run the simulator and extract metrics
python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json
python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json

# (optional) propose baseline PR dry-run
python3 scripts/qa/create_baseline_pr.py
```

CI behavior:
- The `Smoke backtest` workflow runs on-demand and nightly. It will run unit tests, the simulator, extract metrics, and compare metrics to the stored baseline. If a regression is detected the job fails.
- Automatic baseline PR creation is gated and will only push/create PRs when `ALLOW_NOTIFICATIONS` is explicitly set to `1` in repository secrets.
