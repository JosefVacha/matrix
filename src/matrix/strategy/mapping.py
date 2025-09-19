"""
map_predictions_to_signals

Pure Python reference mapping function for MATRIX signal generation.

Args:
    preds: list/tuple/Iterable of float predictions
    up: float (long entry threshold)
    dn: float (short entry threshold)
    hysteresis: float (buffer to prevent immediate flip)
    cooldown_bars: int (bars to suppress new entries after exit)

Returns:
    dict with four parallel lists of 0/1:
        - enter_long
        - enter_short
        - exit_long
        - exit_short

Behavior:
    - Enter long if pred >= up and not cooling down; enter short if pred <= dn and not cooling down.
    - Hysteresis: after long, require pred < (up - hysteresis) to allow exit; analogously for short.
    - Cooldown: after exit, suppress new entries for N bars.

Examples:
    >>> map_predictions_to_signals([0.2, 0.15, 0.05, -0.1, 0.12], up=0.1, dn=-0.1, hysteresis=0.02, cooldown_bars=2)
    {'enter_long': [1, 0, 0, 0, 0], 'enter_short': [0, 0, 0, 1, 0], 'exit_long': [0, 0, 1, 0, 0], 'exit_short': [0, 0, 0, 0, 0]}
"""
from typing import Iterable, List, Dict, Union

def map_predictions_to_signals(
    preds: Union[List[float], tuple[float, ...], Iterable[float]],
    *,
    up: float,
    dn: float,
    hysteresis: float,
    cooldown_bars: int
) -> Dict[str, List[int]]:
    enter_long, enter_short, exit_long, exit_short = [], [], [], []
    state = None  # None, 'long', 'short'
    cooldown = 0
    last_entry_idx = -cooldown_bars
    for i, pred in enumerate(preds):
        # Cooldown logic
        if cooldown > 0:
            enter_long.append(0)
            enter_short.append(0)
            cooldown -= 1
        else:
            if state is None:
                if pred >= up:
                    enter_long.append(1)
                    enter_short.append(0)
                    state = 'long'
                    last_entry_idx = i
                elif pred <= dn:
                    enter_long.append(0)
                    enter_short.append(1)
                    state = 'short'
                    last_entry_idx = i
                else:
                    enter_long.append(0)
                    enter_short.append(0)
            elif state == 'long':
                if pred < (up - hysteresis):
                    exit_long.append(1)
                    exit_short.append(0)
                    state = None
                    cooldown = cooldown_bars
                else:
                    exit_long.append(0)
                    exit_short.append(0)
            elif state == 'short':
                if pred > (dn + hysteresis):
                    exit_long.append(0)
                    exit_short.append(1)
                    state = None
                    cooldown = cooldown_bars
                else:
                    exit_long.append(0)
                    exit_short.append(0)
        # Pad exits for first entry
        if len(exit_long) < len(enter_long):
            exit_long.append(0)
        if len(exit_short) < len(enter_short):
            exit_short.append(0)
    # Ensure all lists are same length
    n = len(enter_long)
    for k in [enter_short, exit_long, exit_short]:
        while len(k) < n:
            k.append(0)
    return {
        'enter_long': enter_long,
        'enter_short': enter_short,
        'exit_long': exit_long,
        'exit_short': exit_short
    }
