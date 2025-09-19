# Freqtrade Backtest Outputs: Accepted Formats

## JSON (Preferred)
Paste/export a JSON file with at least these fields (extra fields ignored):

```
{
  "run_meta": {"timeframe": "5m", "timerange": "20250101-20250131", "pairlist": ["BTC/USDT"], "strategy": "MatrixAdapterStrategy", "commit": "abc123"},
  "perf": {"avg_trade_return": 0.012, "win_rate": 0.43, "max_drawdown": -0.12, "exposure": 0.85},
  "signals": {"entries": 42, "exits_lt_cooldown": 5, "long_rate": 0.51, "short_rate": 0.49, "trigger_rate": 0.12, "hold_time_median": 15}
}
```

## CSV or txt (Fallback)
Paste/export a table with columns:

```
pair,n_trades,win_rate,avg_trade_return,max_drawdown
BTC/USDT,42,0.43,0.012,-0.12
ETH/USDT,38,0.41,0.011,-0.13
```

## Copy Directions
- Save outputs into `docs/REPORTS/RAW/` (git-tracked, small files).
- Use scripts/metrics/ingest_freqtrade_report.py to ingest and fill REPORT/SUMMARY markers.
