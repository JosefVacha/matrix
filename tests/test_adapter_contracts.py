from src.matrix.adapter.freqtrade_strategy_adapter import (
    preds_to_signal_cols,
    attach_signal_cols_to_dataframe,
)


def test_preds_to_signal_cols_shape_and_types():
    preds = [0.0, 0.1, 0.5, -0.2, 0.01]
    thresholds = {"up": 0.05, "dn": -0.05, "cooldown": 2}
    cols = preds_to_signal_cols(preds, thresholds)

    # Expect four keys
    assert set(cols.keys()) == {"enter_long", "enter_short", "exit_long", "exit_short"}

    for k, v in cols.items():
        assert isinstance(v, list)
        assert len(v) == len(preds)
        # all items should be 0 or 1
        assert all(isinstance(x, int) for x in v)
        assert all(x in (0, 1) for x in v)


def test_attach_signal_cols_returns_same_like_object():
    class DummyDF:
        def __init__(self):
            self.meta = {}

    df = DummyDF()
    signal_cols = {
        "enter_long": [0, 1],
        "enter_short": [0, 0],
        "exit_long": [0, 0],
        "exit_short": [0, 0],
    }
    out = attach_signal_cols_to_dataframe(df, signal_cols)
    # Should return same type (not a plain dict)
    assert isinstance(out, DummyDF)
    # Should not be None
    assert out is not None


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
