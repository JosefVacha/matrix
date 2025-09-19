"""
WARNING: OFFLINE EXPERIMENTAL ADAPTER — NO LIVE TRADING

Freqtrade IStrategy skeleton for DRY backtest only.
- Delegates mapping logic to matrix.strategy.mapping via adapter layer.
- Thresholds injected manually from docs/thresholds/sets/TS_*.yml (see DRY_BACKTEST_PROTOCOL.md).
- See CONTRACTS.md for I/O contract; see THRESHOLDS_SETS.md for threshold format.
"""

from freqtrade.strategy.interface import IStrategy


class MatrixAdapterStrategy(IStrategy):
    """
    Minimal Freqtrade IStrategy skeleton for offline DRY backtest.
    All mapping logic is delegated to matrix.strategy.mapping via adapter.
    Thresholds must be injected manually from TS files (see DRY_BACKTEST_PROTOCOL.md).
    WARNING: NO LIVE TRADING; OFFLINE ONLY.
    """

    # --- Required Freqtrade method signatures ---
    def populate_indicators(self, dataframe, metadata):
        """Stub: indicators populated via adapter."""
        pass

    def populate_entry_trend(self, dataframe, metadata):
        """Stub: entry signals populated via adapter."""
        pass

    def populate_exit_trend(self, dataframe, metadata):
        """Stub: exit signals populated via adapter."""
        pass

    # ...other required IStrategy methods (pass)...
