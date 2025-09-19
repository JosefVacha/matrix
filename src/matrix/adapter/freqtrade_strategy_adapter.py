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
    # Pseudocode: call mapping.map_predictions_to_signals()
    # ...existing code...
    return {
        k: [0] * len(preds)
        for k in ["enter_long", "enter_short", "exit_long", "exit_short"]
    }


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
    # Pseudocode: for col in signal_cols, attach to df_like
    # ...existing code...
    return df_like
