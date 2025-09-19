#!/usr/bin/env python3
"""
Generate/update thresholds changelog from DIFF_TS files.
Stdlib only: argparse, pathlib, re, datetime, textwrap
"""

import argparse, pathlib, re, datetime, textwrap


def parse_diff(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(r"DIFF_TS_(\w+)_vs_(\w+)", path.name)
    sets = m.groups() if m else ("A", "B")
    up = re.search(r"up: ([\d\.\-]+)", text)
    dn = re.search(r"dn: ([\d\.\-]+)", text)
    hyst = re.search(r"hysteresis: ([\d\.\-]+)", text)
    cd = re.search(r"cooldown: ([\d\.\-]+)", text)
    notes = re.search(r"stability notes:([\s\S]*?)(\n\n|$)", text)
    return {
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "sets": sets,
        "up": up.group(1) if up else "N/A",
        "dn": dn.group(1) if dn else "N/A",
        "hysteresis": hyst.group(1) if hyst else "N/A",
        "cooldown": cd.group(1) if cd else "N/A",
        "notes": notes.group(1).strip() if notes else "",
    }


def update_changelog(changelog_path, entries):
    lines = []
    if changelog_path.exists():
        lines = changelog_path.read_text(encoding="utf-8").splitlines()
    seen = set()
    for e in entries:
        key = f"{e['date']}|{e['sets'][0]}|{e['sets'][1]}"
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"- {e['date']}: DIFF {e['sets'][0]} vs {e['sets'][1]} | up={e['up']} dn={e['dn']} hysteresis={e['hysteresis']} cooldown={e['cooldown']}"
            + (f" | notes: {e['notes']}" if e["notes"] else "")
        )
    changelog_path.write_text("\n".join(lines), encoding="utf-8")
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Generate/update thresholds changelog from DIFF_TS files."
    )
    parser.add_argument("--diffs", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    entries = [parse_diff(pathlib.Path(p)) for p in args.diffs]
    lines = update_changelog(pathlib.Path(args.out), entries)
    print("Updated CHANGELOG:")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
