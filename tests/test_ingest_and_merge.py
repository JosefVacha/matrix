"""
Offline smoke test for ingest_freqtrade_report.py and merge_summaries.py
"""
import shutil, pathlib, sys
from scripts.metrics.ingest_freqtrade_report import main as ingest_main
from scripts.metrics.merge_summaries import main as merge_main

def test_ingest_and_merge():
    raw_json = pathlib.Path("docs/REPORTS/RAW/FT_SAMPLE.json")
    report_out = pathlib.Path("docs/REPORTS/REPORT_SAMPLE_INGEST.md")
    summary_out = pathlib.Path("docs/summaries/SUMMARY_SAMPLE_INGEST.md")
    recap_out = pathlib.Path("docs/STABILITY_RECAP_INGEST.md")
    # Clean up
    for p in [report_out, summary_out, recap_out]:
        if p.exists(): p.unlink()
    # Ingest
    sys.argv = ["", "--input", str(raw_json), "--report", str(report_out), "--summary", str(summary_out)]
    try:
        ingest_main()
    except SystemExit:
        pass
    # Merge
    sys.argv = ["", "--inputs", str(summary_out), "--out", str(recap_out)]
    try:
        merge_main()
    except SystemExit:
        pass
    # Check
    assert "trigger_rate" in summary_out.read_text(encoding="utf-8")
    assert "run_tag" in recap_out.read_text(encoding="utf-8")

if __name__ == "__main__":
    test_ingest_and_merge()
    pass
