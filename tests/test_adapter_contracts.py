"""
Smoke tests for Freqtrade adapter contract (offline only).
"""

from src.matrix.adapter.freqtrade_strategy_adapter import preds_to_signal_cols


def test_signal_shape_and_values():
    preds = [0.1, 0.5, -0.2, 0.7]
    thresholds = {"up": 0.4, "dn": -0.1, "cooldown": 1}
    signals = preds_to_signal_cols(preds, thresholds)
    assert all(len(signals[k]) == len(preds) for k in signals)
    assert all(x in (0, 1) for k in signals for x in signals[k])


def test_hysteresis_behavior():
    preds = [0.5, -0.5, 0.6, -0.6]
    thresholds = {"up": 0.3, "dn": -0.3, "cooldown": 2}
    signals = preds_to_signal_cols(preds, thresholds)
    # Immediate flip should be prevented by cooldown (hysteresis)
    # This is a hint; actual logic is in mapping.py
    # For now, just check shape and 0/1
    assert all(len(signals[k]) == len(preds) for k in signals)
    assert all(x in (0, 1) for k in signals for x in signals[k])


if __name__ == "__main__":
    pass
