"""
Risk policy module.

Controls position sizing and risk management.
Contract: size_and_risk(signal, context) -> {stake, sl, tp/roi}.
"""

from typing import Dict, Any, Optional


def size_and_risk(
    signal: Dict[str, bool], context: Dict[str, Any]
) -> Dict[str, Optional[float]]:
    """
    Compute position size and risk parameters.

    Args:
        signal: Trading signal from strategy/core.py
        context: Context info (balance, volatility, etc.)

    Returns:
        Dict of risk parameters, e.g. {
            'stake': float,          # position size
            'stop_loss': float,      # SL level
            'take_profit': float,    # TP level or None
            'roi': Dict              # ROI table for Freqtrade
        }

    Guardrails:
        - Maximum risk per trade
        - Portfolio heat check
        - Volatility-based sizing
    """
    pass
