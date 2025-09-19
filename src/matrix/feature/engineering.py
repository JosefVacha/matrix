"""
Feature engineering modul.

Generuje příznaky a labely zarovnané v čase bez temporal leakage.
Kontrakt: make_features(df) → (features_df, labels_series) se zarovnanými indexy.
"""
from typing import Tuple, Any
import pandas as pd  # type: ignore


def make_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Generuje features a labels z OHLCV dat.
    
    Args:
        df: OHLCV DataFrame s datetime indexem
        
    Returns:
        Tuple (features_df, labels_series) se zarovnanými indexy v čase.
        Features = technické indikátory, rolling stats, apod.
        Labels = target pro predikci (s look-ahead, ale zarovnané správně).
        
    Guardrails:
        - Žádný temporal leakage (budoucí info v current features)
        - Robust scaling (median/IQR)
        - Volitelná PCA (variance-based)
        - Outlier handling (IQR/IF)
    """
    # TODO: Implementovat robust scaling (median/IQR)
    # TODO: Volitelná PCA (variance-based)  
    # TODO: Outlier detection a handling (IQR/Isolation Forest)
    pass