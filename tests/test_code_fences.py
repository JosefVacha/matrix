import sys
import subprocess
from pathlib import Path


def test_no_code_fences():
    script = Path("scripts/qa/check_code_fences.py")
    p = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert p.returncode == 0, (
        f"Code fences found or checker failed:\n{p.stdout}\n{p.stderr}"
    )
