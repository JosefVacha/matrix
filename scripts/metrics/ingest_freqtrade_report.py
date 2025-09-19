#!/usr/bin/env python3
"""
Ingest Freqtrade backtest output (JSON/CSV/txt) and fill REPORT/SUMMARY markers.
Stdlib only: argparse, pathlib, json, csv, re, textwrap, sys
"""

import argparse, pathlib, json, csv, re, textwrap, sys


def parse_json(path):
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        return data
    except Exception:
        return None


def parse_csv(path):
    try:
        rows = list(
            csv.DictReader(pathlib.Path(path).read_text(encoding="utf-8").splitlines())
        )
        return rows
    except Exception:
        return None


def parse_txt(path):
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    out = {}
    for line in lines:
        m = re.match(r"(\w+):\s*([\d\.\-%]+)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out if out else None


def fill_report(report_path, data):
    # Minimal marker fill: RUN_META, PERF_PROXY, SIGNALS
    text = (
        pathlib.Path(report_path).read_text(encoding="utf-8")
        if pathlib.Path(report_path).exists()
        else ""
    )

    def marker(name, content):
        return f"<!-- {name} -->\n{content}\n<!-- /{name} -->"

    # Fill RUN_META
    run_meta = data.get("run_meta", {})
    run_meta_str = "\n".join(f"{k}: {v}" for k, v in run_meta.items())
    text = (
        re.sub(
            r"<!-- RUN_META -->([\s\S]*?)<!-- /RUN_META -->",
            marker("RUN_META", run_meta_str),
            text,
        )
        if "<!-- RUN_META -->" in text
        else text + "\n" + marker("RUN_META", run_meta_str)
    )
    # Fill PERF_PROXY
    perf = data.get("perf", {})
    perf_str = "\n".join(f"{k}: {v}" for k, v in perf.items())
    text = (
        re.sub(
            r"<!-- PERF_PROXY -->([\s\S]*?)<!-- /PERF_PROXY -->",
            marker("PERF_PROXY", perf_str),
            text,
        )
        if "<!-- PERF_PROXY -->" in text
        else text + "\n" + marker("PERF_PROXY", perf_str)
    )
    # Fill SIGNALS
    signals = data.get("signals", {})
    signals_str = "\n".join(f"{k}: {v}" for k, v in signals.items())
    text = (
        re.sub(
            r"<!-- SIGNALS -->([\s\S]*?)<!-- /SIGNALS -->",
            marker("SIGNALS", signals_str),
            text,
        )
        if "<!-- SIGNALS -->" in text
        else text + "\n" + marker("SIGNALS", signals_str)
    )
    pathlib.Path(report_path).write_text(text, encoding="utf-8")
    return ["RUN_META", "PERF_PROXY", "SIGNALS"]


def render_summary(summary_path, data):
    # Minimal summary: just dump key metrics
    lines = []
    run_tag = summary_path.stem.split("SUMMARY_")[-1]
    lines.append(f"run_tag: {run_tag}")
    for k in ("trigger_rate", "long_rate", "short_rate", "churn_rate", "max_drawdown"):
        v = data.get("signals", {}).get(k) or data.get("perf", {}).get(k) or "N/A"
        lines.append(f"{k}: {v}")
    pathlib.Path(summary_path).write_text("\n".join(lines), encoding="utf-8")
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Ingest Freqtrade report and fill markers."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()
    input_path = pathlib.Path(args.input)
    data = parse_json(input_path) or {}
    if not data:
        rows = parse_csv(input_path)
        if rows:
            # Aggregate: avg_trade_return, win_rate, max_drawdown
            agg = {
                k: sum(float(r.get(k, 0)) for r in rows) / len(rows)
                for k in ("avg_trade_return", "win_rate", "max_drawdown")
                if k in rows[0]
            }
            data = {"perf": agg}
    if not data:
        txt = parse_txt(input_path)
        if txt:
            data = {"perf": txt}
    if not data:
        print(f"Could not parse input: {input_path}")
        sys.exit(1)
    filled = fill_report(args.report, data)
    summary_lines = render_summary(pathlib.Path(args.summary), data)
    print(f"Filled markers: {filled}\nSummary lines: {summary_lines}")
    sys.exit(0)


if __name__ == "__main__":
    main()
