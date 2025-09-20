"""Check for accidental Markdown code-fence markers in Python files.

This script scans the repository for occurrences of the literal sequence
of three backtick characters inside Python source files. Such artifacts often
appear when Markdown snippets are accidentally pasted into code and can
break imports or tests.

Exit codes:
 - 0: clean
 - 1: one or more Python files contain the three-backtick sequence
"""

import sys
from pathlib import Path


def find_code_fences(root: Path):
    """Return list of file paths (strings) that contain the three-backtick
    sequence.
    """
    violations = []
    self_path = Path(__file__).resolve()
    for p in root.rglob("*.py"):
        # avoid reporting this checker script itself
        try:
            if p.resolve() == self_path:
                continue
        except Exception:
            # if resolving fails, continue and let the read_text step handle issues
            pass
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            # skip unreadable files
            continue
        if "```" in text:
            violations.append(str(p))
    return violations


def main() -> int:
    repo_root = Path(__file__).parent.parent
    bad = find_code_fences(repo_root)
    if bad:
        print("Found code-fence artifacts in Python files:")
        for f in bad:
            print(f" - {f}")
        return 1
    print("No code-fence artifacts found in Python files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
