"""
Feature engineering module.

Generates time-aligned features and labels without temporal leakage.
Contract: make_features(df) -> (features_df, labels_series) with aligned indices.
"""

from typing import Tuple, Any
import pandas as pd  # type: ignore


def make_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generate features and labels from OHLCV data.

    Args:
        df: OHLCV DataFrame with datetime index

    Returns:
        Tuple (features_df, labels_series) with aligned time indices.
        Features = technical indicators, rolling stats, etc.
        Labels = prediction target (with look-ahead, but aligned correctly).

    Guardrails:
        - No temporal leakage (no future info in current features)
        - Robust scaling (median/IQR)
        - Optional PCA (variance-based)
        - Outlier handling (IQR/IF)
    """
    # TODO: Implement robust scaling (median/IQR)
    # TODO: Optional PCA (variance-based)
    # TODO: Outlier detection and handling (IQR/Isolation Forest)
    pass
