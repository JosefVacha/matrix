"""
Freqtrade Strategy Adapter Layer (Skeleton)

References:
- docs/CONTRACTS.md (Strategy I/O contract)
- docs/thresholds/THRESHOLDS_SETS.md (Thresholds format)

Purpose:
- Provide a thin, documented adapter for Freqtrade-compatible signal mapping.
- Guarantee: I/O alignment, no leakage, signals aligned to predictions, 0/1 columns only.
- NO live trading, NO downloads, NO auto-runs.
"""

from typing import List, Dict, Any

# Import the pure-Python mapping function implemented elsewhere in the repo.
from src.matrix.strategy.mapping import map_predictions_to_signals

try:
    import pandas as pd
except Exception:
    pd = None


# --- Adapter Helpers ---
def inject_thresholds_from_yaml(yaml_path: str) -> dict:
    """
    Load a minimal threshold set from a YAML file (see THRESHOLDS_SETS.md).
    Only the required keys (e.g., 'up', 'dn', 'cooldown') are parsed.
    Returns a dict suitable for signal mapping.
    Note: Use only local, static files. No downloads.
    """
    # Pseudocode: parse YAML subset (reuse scripts/thresholds/print_thresholds.py logic)
    # ...existing code...
    return {}


def preds_to_signal_cols(preds: List[float], thresholds: dict) -> Dict[str, List[int]]:
    """
    Wraps matrix.strategy.mapping.map_predictions_to_signals().
    Args:
        preds: List of prediction floats (aligned to DataFrame index)
        thresholds: Dict with 'up', 'dn', 'cooldown' (see THRESHOLDS_SETS.md)
    Returns:
        Dict with four keys: 'enter_long', 'enter_short', 'exit_long', 'exit_short',
        each a list of 0/1 (same length as preds).
    Contract:
        - No leakage; signals aligned to preds
        - 0/1 only; same length
    """
    # Normalize threshold keys and provide defaults if missing
    up = float(thresholds.get("up", 0.0))
    dn = float(thresholds.get("dn", 0.0))
    hysteresis = float(thresholds.get("hysteresis", 0.01))
    cooldown = int(thresholds.get("cooldown", thresholds.get("cooldown_bars", 0)))

    # Delegate to the canonical mapping implementation
    mapped = map_predictions_to_signals(
        preds, up=up, dn=dn, hysteresis=hysteresis, cooldown_bars=cooldown
    )

    # Ensure outputs are lists of ints and match length
    out = {}
    for k in ["enter_long", "enter_short", "exit_long", "exit_short"]:
        vals = mapped.get(k, [])
        out[k] = [int(v) for v in list(vals)]
        # Guarantee same length as preds
        if len(out[k]) != len(preds):
            out[k] = [0] * len(preds)
    return out


def attach_signal_cols_to_dataframe(
    df_like: Any, signal_cols: Dict[str, List[int]]
) -> Any:
    """
    Document how signal columns would be attached to a Freqtrade DataFrame.
    Args:
        df_like: DataFrame-like object (Freqtrade expects pandas.DataFrame)
        signal_cols: Dict of signal lists (see preds_to_signal_cols)
    Returns:
        df_like with new columns: 'enter_long', 'enter_short', 'exit_long', 'exit_short'
    Note:
        This is pseudocode only; do not perform actual pandas operations here.
    """
    # If pandas is available and df_like is a DataFrame, attach columns safely
    if pd is not None and isinstance(df_like, pd.DataFrame):
        for col, values in signal_cols.items():
            # Truncate/extend values to match index length
            n = len(df_like.index)
            vals = list(values)
            if len(vals) < n:
                vals = vals + [0] * (n - len(vals))
            elif len(vals) > n:
                vals = vals[:n]
            df_like[col] = vals
        return df_like

    # Generic df-like: attempt to set attribute or dict-style
    try:
        # If it supports item assignment (like dict), try that
        for col, values in signal_cols.items():
            try:
                df_like.__setattr__(col, values)
            except Exception:
                try:
                    df_like[col] = values
                except Exception:
                    # Fallback: store in a .meta dict if present
                    if hasattr(df_like, "meta") and isinstance(df_like.meta, dict):
                        df_like.meta[col] = values
        return df_like
    except Exception:
        return df_like
