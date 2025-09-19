"""
Risk policy modul.

Řídí pozice sizing a risk management.
Kontrakt: size_and_risk(signal, context) → {stake, sl, tp/roi}.
"""
from typing import Dict, Any, Optional


def size_and_risk(signal: Dict[str, bool], context: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Vypočítá velikost pozice a risk parametry.
    
    Args:
        signal: Trading signál z strategy/core.py
        context: Kontextové info (balance, volatility, apod.)
        
    Returns:
        Dict s risk parametry: {
            'stake': float,          # velikost pozice
            'stop_loss': float,      # SL úroveň
            'take_profit': float,    # TP úroveň nebo None
            'roi': Dict              # ROI table pro Freqtrade
        }
        
    Guardrails:
        - Maximální risk per trade
        - Portfolio heat kontrola
        - Volatility-based sizing
    """
    pass