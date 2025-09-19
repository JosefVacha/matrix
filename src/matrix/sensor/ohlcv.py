"""
OHLCV sensor module.

Provides an interface for fetching OHLCV data with a datetime index.
Contract: get_ohlcv(pair, timeframe) -> DataFrame [date, open, high, low, close, volume] with datetime index.
"""

from typing import Optional
import pandas as pd


def get_ohlcv(
    pair: str, timeframe: str, since: Optional[str] = None, limit: Optional[int] = None
) -> pd.DataFrame:
    """
    Fetch OHLCV data for the given pair and timeframe.

    Args:
        pair: Trading pair (e.g. "BTC/USDT")
        timeframe: Timeframe (e.g. "5m", "1h", "1d")
        since: Starting date (ISO format or timestamp)
        limit: Maximum number of records

    Returns:
        DataFrame indexed by datetime with columns [open, high, low, close, volume].
        Columns should be numeric types; avoid NaN when possible.
    """
    pass
