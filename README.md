# MATRIX

![guardrails](https://github.com/JosefVacha/matrix/actions/workflows/smoke-validators.yml/badge.svg)
![paper-trade smoke (manual)](https://github.com/JosefVacha/matrix/actions/workflows/paper_trade_smoke.yml/badge.svg)

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
