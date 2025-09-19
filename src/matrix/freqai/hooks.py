"""
FreqAI Hook Functions for MATRIX Feature Engineering.

These functions serve as the bridge between MATRIX's feature engineering
and FreqAI's training/inference pipeline. All functions are designed to
maintain temporal integrity and prevent data leakage.

Contract Requirements:
- All functions must preserve DataFrame index alignment
- No future information leakage in features/labels
- Robust handling of NaN values with telemetry logging
- Type hints and comprehensive docstrings required

See docs/CONTRACTS.md for detailed I/O specifications.
See docs/LABELS.md for label generation semantics.
"""

import pandas as pd


def generate_features(df_ohlcv: pd.DataFrame) -> pd.DataFrame:
    """
    Generate minimal model-ready features from OHLCV data for FreqAI training/inference.

    Args:
        df_ohlcv: DataFrame with OHLCV data, datetime index required.
            Columns: ['open', 'high', 'low', 'close', 'volume']

    Returns:
        DataFrame with generated features, same index as input.
        Columns (prefix 'f_'):
            - f_ret_1, f_ret_3, f_ret_12: percent/log returns over 1, 3, 12 bars (right-aligned)
            - f_hl_range: high-low range
            - f_oc_range: open-close range
            - f_vol_z: volume z-score (robust scaling: median/IQR)

    Contract:
        - MUST preserve df_ohlcv.index exactly
        - MUST NOT use future information (no forward-looking calculations)
        - All rolling/statistics are right-aligned (window ends at t)
        - Drop warmup rows (first max(window) rows)
        - NaN-safe: drop rows with NaN after feature generation
        - Columns prefixed 'f_'
    TODO: Implement with pandas; for now, stub only.
    """
    pass


def generate_labels(df_ohlcv: pd.DataFrame, mode: str = "R", **kwargs) -> pd.Series:
    """
    Generate labels for supervised learning: forward return over H bars.

    Args:
        df_ohlcv: DataFrame with OHLCV data, datetime index required.
        mode: 'R' for return
        H: Lookahead horizon (bars)
        transform: 'log' or 'pct' for log-return or percent-return

    Returns:
        Series with labels, same index as input (last H rows become NaN)

    Formula:
        - If transform='pct': label_t = (close_{t+H} / close_t) - 1
        - If transform='log': label_t = log(close_{t+H} / close_t)
    Alignment:
        - Label for t uses close at t and t+H (lookahead)
        - Last H rows become NaN and are dropped downstream
    Contract:
        - Strict lookahead: no leakage
        - Index aligned to t
    TODO: Implement with pandas; for now, stub only.
    """
    pass


def feature_columns() -> list[str]:
    """
    Return list of feature column names (deterministic, doc-only).
    Columns: 'f_ret_1', 'f_ret_3', 'f_ret_12', 'f_hl_range', 'f_oc_range', 'f_vol_z'
    """
    return ['f_ret_1', 'f_ret_3', 'f_ret_12', 'f_hl_range', 'f_oc_range', 'f_vol_z']


def label_name() -> str:
    """
    Return label name (deterministic, doc-only).
    Format: 'label_R_<H>_<transform>'
    """
    return "label_R_<H>_<transform>"
