"""Check that CLI-style scripts expose a safe importable `main()`.

This script attempts to import target modules under `scripts/` and checks
that they define a callable `main` attribute. It exits 0 when all checks
pass, non-zero otherwise. It's intended to ensure tests can import CLI
modules without running side-effects.
"""

import importlib.util
import sys
from pathlib import Path


TARGET_FILES = [
    Path(__file__).parent / "check_code_fences.py",
    Path(__file__).parent / "check_copilot_guardrails.py",
    Path(__file__).parent / "check_workspace_health.py",
]


def load_module_from_path(p: Path):
    try:
        spec = importlib.util.spec_from_file_location(p.stem, str(p))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod
    except Exception as e:
        print(f"IMPORT FAIL: {p} -> {e}")
        return None


def check_file(p: Path) -> bool:
    mod = load_module_from_path(p)
    if mod is None:
        print(f"IMPORT FAIL: {p}")
        return False
    if not hasattr(mod, "main"):
        print(f"MISSING main(): {p}")
        return False
    if not callable(getattr(mod, "main")):
        print(f"main not callable: {p}")
        return False
    return True


def main() -> int:
    ok = True
    for p in TARGET_FILES:
        if not p.exists():
            print(f"MISSING FILE: {p}")
            ok = False
            continue
        if not check_file(p):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
