"""
Offline smoke tests for map_predictions_to_signals (no external runner required).
TODO: Convert to pytest later.
"""
from src.matrix.strategy.mapping import map_predictions_to_signals

def test_cooldown():
    preds = [0.2, 0.2, 0.2, -0.2, 0.2, 0.2]
    out = map_predictions_to_signals(preds, up=0.1, dn=-0.1, hysteresis=0.02, cooldown_bars=2)
    # After exit, next entry should be suppressed for 2 bars
    assert out['enter_long'][4] == 0

def test_hysteresis():
    preds = [0.2, 0.2, 0.05, -0.2, 0.2]
    out = map_predictions_to_signals(preds, up=0.1, dn=-0.1, hysteresis=0.1, cooldown_bars=1)
    # Hysteresis should prevent immediate flip-flop
    assert out['exit_long'][2] == 1
    assert out['enter_short'][3] == 1

def test_output_shape():
    preds = [0.2, -0.2, 0.2, -0.2]
    out = map_predictions_to_signals(preds, up=0.1, dn=-0.1, hysteresis=0.02, cooldown_bars=1)
    n = len(preds)
    for k in out:
        assert len(out[k]) == n
        assert all(x in (0, 1) for x in out[k])

if __name__ == "__main__":
    test_cooldown()
    test_hysteresis()
    test_output_shape()
    print("Mapping smoke tests passed.")
