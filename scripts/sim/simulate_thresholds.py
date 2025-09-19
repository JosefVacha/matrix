"""
simulate_thresholds.py

Purpose: Generate synthetic prediction series, map to signals, compute proxy metrics.

Usage:
    python simulate_thresholds.py --len 500 --noise 0.2 --up 0.1 --dn -0.1 --hysteresis 0.02 --cooldown 3 --out docs/summaries/SIM_SUMMARY_<TAG>.md

Output: Markdown summary with trigger_rate, long/short split, churn proxy, avg hold bars, ASCII sparkline.

NO LIVE ACTION; OFFLINE ONLY.
"""
import argparse
import math
import random
from pathlib import Path
import sys
import textwrap

sys.path.insert(0, 'src/matrix/strategy')
from mapping import map_predictions_to_signals

def generate_preds(length: int, noise: float) -> list[float]:
    return [math.sin(i * 2 * math.pi / 50) + random.uniform(-noise, noise) for i in range(length)]

def ascii_sparkline(vals: list[float], width: int = 60) -> str:
    minv, maxv = min(vals), max(vals)
    scale = (maxv - minv) or 1
    step = max(1, len(vals) // width)
    chars = '▁▂▃▄▅▆▇█'
    out = ''
    for i in range(0, len(vals), step):
        v = vals[i]
        idx = int((v - minv) / scale * (len(chars) - 1))
        out += chars[idx]
    return out

def compute_metrics(signals: dict, preds: list[float], cooldown: int) -> dict:
    entries = sum(signals['enter_long']) + sum(signals['enter_short'])
    exits_lt_cooldown = 0
    last_entry = None
    for i, (el, es) in enumerate(zip(signals['enter_long'], signals['enter_short'])):
        if el or es:
            last_entry = i
        if signals['exit_long'][i] or signals['exit_short'][i]:
            if last_entry is not None and (i - last_entry) < cooldown:
                exits_lt_cooldown += 1
            last_entry = None
    hold_times = []
    state = None
    entry_idx = None
    for i, (el, es) in enumerate(zip(signals['enter_long'], signals['enter_short'])):
        if el or es:
            state = 'long' if el else 'short'
            entry_idx = i
        if state and (signals['exit_long'][i] or signals['exit_short'][i]):
            hold_times.append(i - entry_idx)
            state = None
    avg_hold = round(sum(hold_times) / len(hold_times), 2) if hold_times else 0
    trigger_rate = round(entries / len(preds), 4)
    long_rate = round(sum(signals['enter_long']) / entries, 4) if entries else 0
    short_rate = round(sum(signals['enter_short']) / entries, 4) if entries else 0
    churn_rate = round(exits_lt_cooldown / entries, 4) if entries else 0
    return dict(trigger_rate=trigger_rate, long_rate=long_rate, short_rate=short_rate, churn_rate=churn_rate, avg_hold=avg_hold)

def render_summary(metrics: dict, preds: list[float], args) -> str:
    return textwrap.dedent(f"""
    # MATRIX Synthetic Simulator Summary
    
    **Parameters:**
    - Length: {args.len}
    - Noise: {args.noise}
    - UP: {args.up}
    - DN: {args.dn}
    - Hysteresis: {args.hysteresis}
    - Cooldown: {args.cooldown}
    
    **Proxy Metrics:**
    - Trigger Rate: {metrics['trigger_rate']}
    - Long Rate: {metrics['long_rate']}
    - Short Rate: {metrics['short_rate']}
    - Churn Rate: {metrics['churn_rate']}
    - Avg Hold Bars: {metrics['avg_hold']}
    
    **Predictions Sparkline:**
    {ascii_sparkline(preds)}
    """)

def main():
    parser = argparse.ArgumentParser(description="Run MATRIX synthetic threshold simulator.")
    parser.add_argument("--len", type=int, default=500)
    parser.add_argument("--noise", type=float, default=0.2)
    parser.add_argument("--up", type=float, default=0.1)
    parser.add_argument("--dn", type=float, default=-0.1)
    parser.add_argument("--hysteresis", type=float, default=0.02)
    parser.add_argument("--cooldown", type=int, default=3)
    parser.add_argument("--out", type=str, required=True)
    args = parser.parse_args()
    preds = generate_preds(args.len, args.noise)
    signals = map_predictions_to_signals(preds, up=args.up, dn=args.dn, hysteresis=args.hysteresis, cooldown_bars=args.cooldown)
    metrics = compute_metrics(signals, preds, args.cooldown)
    summary = render_summary(metrics, preds, args)
    Path(args.out).write_text(summary)
    print(f"Summary written to {args.out}")

if __name__ == "__main__":
    main()
