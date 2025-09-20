#!/usr/bin/env python3
"""Simple offline paper-trading simulator.

This simulator reads a Parquet or pickle OHLCV dataset (data/dataset_SMOKE.parquet by default),
accepts a simple signal function (buy/sell/hold per row) and simulates fills at next-close,
applies a flat fee and percentage slippage, and writes a report JSON and trade CSV to outputs/.

This is intentionally small and deterministic for reproducible smoke runs.
"""

import argparse
import json
from pathlib import Path
import pandas as pd
import csv


def load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    else:
        return pd.read_pickle(path)


def simple_signal(df: pd.DataFrame) -> pd.Series:
    # Very small deterministic signal for smoke: buy when close > open, sell when close < open
    sig = pd.Series(index=df.index, data=0)
    sig[df["close"] > df["open"]] = 1
    sig[df["close"] < df["open"]] = -1
    return sig


def run_sim(df: pd.DataFrame, initial_cash: float, fee: float, slippage_pct: float):
    cash = initial_cash
    position = 0.0
    trades = []

    signals = simple_signal(df)

    for i in range(len(df) - 1):
        ts = df.index[i]
        nxt_close = float(df.iloc[i + 1]["close"])
        sig = int(signals.iloc[i])

        if sig == 1 and position <= 0:
            # buy one unit
            fill_price = nxt_close * (1 + slippage_pct)
            cost = fill_price + fee
            if cash >= cost:
                cash -= cost
                position = 1.0
                trades.append(
                    {"ts": str(ts), "side": "buy", "price": fill_price, "cash": cash}
                )
        elif sig == -1 and position >= 0:
            # sell existing position
            fill_price = nxt_close * (1 - slippage_pct)
            proceeds = fill_price - fee
            if position > 0:
                cash += proceeds
                trades.append(
                    {"ts": str(ts), "side": "sell", "price": fill_price, "cash": cash}
                )
                position = 0

    # final mark-to-market
    final_close = float(df.iloc[-1]["close"])
    net = cash + position * final_close
    return {
        "initial_cash": initial_cash,
        "final_net": net,
        "cash": cash,
        "position": position,
        "trades": trades,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="data/dataset_SMOKE.parquet")
    parser.add_argument("--initial-cash", type=float, default=1000.0)
    parser.add_argument("--fee", type=float, default=0.1)
    parser.add_argument("--slippage-pct", type=float, default=0.001)
    parser.add_argument("--output", default="outputs/paper_trade_report.json")
    args = parser.parse_args()

    p = Path(args.dataset)
    if not p.exists():
        print("Dataset not found:", p)
        return

    df = load_dataset(p)
    # If dataset lacks OHLCV columns, try to synthesize a close series from labels/features
    if "close" not in df.columns:
        if "label_R_H3_pct" in df.columns:
            # treat as pct returns per row and build price series
            pct = df["label_R_H3_pct"].fillna(0).astype(float)
            price = 100.0 * (1.0 + pct).cumprod()
            df = df.copy()
            df["close"] = price
            df["open"] = df["close"].shift(1).fillna(df["close"]).astype(float)
            df["high"] = df[["open", "close"]].max(axis=1)
            df["low"] = df[["open", "close"]].min(axis=1)
            df["volume"] = 1.0
        elif "label_R_H3" in df.columns:
            val = df["label_R_H3"].fillna(0).astype(float)
            price = 100.0 + val.cumsum()
            df = df.copy()
            df["close"] = price
            df["open"] = df["close"].shift(1).fillna(df["close"]).astype(float)
            df["high"] = df[["open", "close"]].max(axis=1)
            df["low"] = df[["open", "close"]].min(axis=1)
            df["volume"] = 1.0
        else:
            raise SystemExit(
                "Dataset missing OHLCV columns and no suitable label to synthesize price"
            )

    # ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    out = run_sim(df, args.initial_cash, args.fee, args.slippage_pct)
    outp = Path(args.output)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    # write trades CSV
    trades_csv = outp.with_name(outp.stem + "_trades.csv")
    with open(trades_csv, "w", newline="") as f:
        if out["trades"]:
            writer = csv.DictWriter(f, fieldnames=out["trades"][0].keys())
            writer.writeheader()
            writer.writerows(out["trades"])
    print("Wrote report:", outp)


if __name__ == "__main__":
    main()
