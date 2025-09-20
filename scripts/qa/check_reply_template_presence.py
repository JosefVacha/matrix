#!/usr/bin/env python3
"""Lightweight check that the reply-template doc exists and copilot-instructions references it.

Exit codes:
 0 = OK (both present)
 1 = missing one or both
"""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "Knowledge" / "REPLY_TEMPLATES.md"
COPILOT = ROOT / ".github" / "copilot-instructions.md"


def main():
    missing = []
    if not TEMPLATE.exists():
        missing.append(str(TEMPLATE))
    if not COPILOT.exists():
        missing.append(str(COPILOT))
    else:
        txt = COPILOT.read_text(encoding="utf-8")
        if "Knowledge/REPLY_TEMPLATES.md" not in txt:
            missing.append("copilot-instructions.md: missing REPLY_TEMPLATES reference")
        # Check that the copilot instructions explicitly require Czech replies when user asks in Czech
        ltxt = txt.lower()
        if (
            "if user asks in czech, answer in czech" not in ltxt
            and "when the user asks in czech" not in ltxt
        ):
            missing.append(
                "copilot-instructions.md: missing Czech reply rule (must state: If user asks in Czech, answer in Czech)"
            )

    if missing:
        print("Reply template check: MISSING items:")
        for m in missing:
            print(" -", m)
        return 1
    print(
        "Reply template check: OK (Knowledge/REPLY_TEMPLATES.md referenced from copilot-instructions.md)"
    )
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
