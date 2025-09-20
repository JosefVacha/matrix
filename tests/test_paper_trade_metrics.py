import json
from pathlib import Path


def test_extract_metrics(tmp_path):
    # Create a synthetic paper_trade_report.json
    report = {
        "initial_cash": 1000.0,
        "final_net": 1100.5,
        "trades": [
            {"ts": "2025-09-20T00:00:00Z", "side": "buy", "price": 100.0},
            {"ts": "2025-09-20T01:00:00Z", "side": "sell", "price": 110.0},
        ],
    }
    inp = tmp_path / "paper_trade_report.json"
    out = tmp_path / "paper_trade_metrics.json"
    inp.write_text(json.dumps(report))

    # Run the extractor
    from scripts.qa.extract_paper_trade_metrics import extract

    metrics = extract(inp, out)

    assert out.exists()
    data = json.loads(out.read_text())
    assert data["final_net"] == 1100.5
    assert data["trades_count"] == 2
    assert metrics["trades_count"] == 2
