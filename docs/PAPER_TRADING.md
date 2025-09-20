# Paper Trading Simulator — Usage & Interpretation

This repository includes a small, deterministic paper-trading simulator (`scripts/trading/paper_trading_sim.py`) intended for smoke tests and maintainers to validate trading logic end-to-end without executing real orders.

Quick start (local)

1. Ensure dev dependencies are installed in your venv (pandas):

```
python3 -m pip install -r requirements-dev.txt
```

2. Run the simulator against the canonical smoke dataset:

```
make paper-trade-sim
```

3. Outputs:
 - `outputs/paper_trade_report.json` — summary with `initial_cash`, `final_net`, `trades` and cash/position state
 - `outputs/paper_trade_report_trades.csv` — per-trade CSV (timestamp, side, price, cash)

Mapping FreqAI model -> simulator signals

- A trained FreqAI model should produce per-row predictions (probability or point estimate) aligned to the OHLCV index used by the simulator.
- Convert model outputs to discrete signals: buy (1), sell (-1), hold (0). A simple threshold example:

```
pred = model.predict_proba(X)[:, 1]
signal = np.where(pred > 0.6, 1, np.where(pred < 0.4, -1, 0))
```

- Save the signals as a column `signal` in a DataFrame that matches the dataset index and use a tiny adapter to feed it into the simulator (or patch `simple_signal` in `paper_trading_sim.py`).

Interpreting results

- `final_net - initial_cash` is your P&L for the run.
- Review `paper_trade_report_trades.csv` to inspect per-trade fills and `cash` evolution.
- Use `outputs/summary.json` or the aggregator scripts (if present) to combine metrics across runs.

Safety & reproducibility

- The simulator is offline-only and will never connect to exchanges.
- The simulator will synthesize a price series if your smoke dataset doesn't contain OHLCV, using label columns (helpful for early experiments).
- Keep `ALLOW_NOTIFICATIONS` disabled unless you explicitly want the notifier to perform remote actions.

Next steps (recommended)

- Extend the simulator to support position sizing strategies and realistic slippage models.
- Add a CI smoke check that runs the simulator on a tiny dataset to prevent regressions.
- Build an adapter to feed direct FreqAI outputs into the simulator for rapid model-to-backtest loops.
