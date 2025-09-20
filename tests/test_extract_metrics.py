import json
from pathlib import Path

from scripts.qa import extract_paper_trade_metrics as extractor


def test_extract_metrics(tmp_path: Path):
    report = {
        "final_net": 1200.0,
        "equity": [1000.0, 1100.0, 1050.0, 1200.0],
        "trades": [
            {"pnl": 100.0},
            {"pnl": -50.0},
            {"pnl": 150.0},
        ],
    }
    inp = tmp_path / "report.json"
    out = tmp_path / "metrics.json"
    inp.write_text(json.dumps(report))

    metrics = extractor.extract(inp, out)

    assert metrics["final_net"] == 1200.0
    assert metrics["trades_count"] == 3
    assert round(metrics["trade_pnl_mean"], 6) == round((100.0 - 50.0 + 150.0) / 3.0, 6)
    assert metrics["trade_pnl_max"] == 150.0
    assert metrics["trade_pnl_min"] == -50.0
    # Expected max drawdown: peak at 1100, dip to 1050 => (1100-1050)/1100
    expected_dd = (1100.0 - 1050.0) / 1100.0
    assert round(metrics["max_drawdown"], 8) == round(expected_dd, 8)
