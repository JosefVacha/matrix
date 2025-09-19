"""
OHLCV sensor modul.

Poskytuje rozhraní pro získávání OHLCV dat s časovým indexem.
Kontrakt: get_ohlcv(pair, timeframe) → DataFrame [date, open, high, low, close, volume] s datetime indexem.
"""

from typing import Optional
import pandas as pd


def get_ohlcv(
    pair: str, timeframe: str, since: Optional[str] = None, limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Získá OHLCV data pro zadaný pair a timeframe.

    Args:
        pair: Trading pair (např. "BTC/USDT")
        timeframe: Časový rámec (např. "5m", "1h", "1d")
        since: Datum od kdy (ISO format nebo timestamp)
        limit: Maximální počet záznamů

    Returns:
        DataFrame s indexem datetime a sloupci [open, high, low, close, volume]
        Sloupce musí být číselné typy, bez NaN pokud možno.
    """
    pass
