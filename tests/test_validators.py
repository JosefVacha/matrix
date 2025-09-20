import subprocess
import sys


def run_script(path: str, args=None):
    if args is None:
        args = []
    cmd = [sys.executable, path] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_check_H_consistency_cli():
    path = "scripts/qa/check_H_consistency.py"
    code, out = run_script(
        path, ["--label-name", "label_R_H12_pct", "--windows", "1,3,12", "--H", "12"]
    )
    assert code == 0
    assert "OK: checked label" in out


def test_check_code_fences_cli():
    path = "scripts/qa/check_code_fences.py"
    code, out = run_script(path)
    assert code == 0
    assert "No code-fence artifacts" in out


def test_check_workspace_health_smoke():
    path = "scripts/qa/check_workspace_health.py"
    code, out = run_script(path)
    # script returns 0 on PASS, 2 on FAIL (per implementation). We accept either but require expected keys
    assert "ws_health:" in out
    assert "en_policy_exit:" in out
    assert "registry_check_exact:" in out
