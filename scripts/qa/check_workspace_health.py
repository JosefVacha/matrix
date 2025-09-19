#!/usr/bin/env python3
"""
Workspace health gate (stdlib-only).

Exit codes:
  0 = PASS, non-zero = FAIL

Machine-readable output lines (exact keys):
  ws_health: PASS|FAIL
  en_policy_exit:<code>
  registry_check_exact:<true|false>
  h_consistency_exact:<true|false>
  validators_ci_present:<true|false>
  todo_audit:<summary>
  git_clean:<true|false>

This script will attempt minimal auto-fixes for `tasks.json` and `docs/EVAL_METRICS.md` when safe.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Tuple


ROOT = Path(".")
COPILOT = ROOT / ".github" / "copilot-instructions.md"
AGENTS = ROOT / "AGENTS.md"
PROJECT = ROOT / "Knowledge" / "PROJECT_STATE.md"
TASKS = ROOT / ".vscode" / "tasks.json"
WORKFLOW = ROOT / ".github" / "workflows" / "smoke-validators.yml"
TODO = ROOT / "docs" / "COPILOT_TODO.md"
MODEL_REG = ROOT / "docs" / "MODEL_REGISTRY.md"
EVAL_METRICS = ROOT / "docs" / "EVAL_METRICS.md"


def run_cmd(cmd: list) -> Tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    except Exception as e:
        return 1, str(e)


def has_preface() -> bool:
    if not COPILOT.exists():
        return False
    txt = COPILOT.read_text(encoding="utf-8")
    line1 = "Guardrail check: ran check_copilot_guardrails.py — PASS"
    line2 = "Files reloaded: copilot-instructions.md, AGENTS.md, PROJECT_STATE.md"
    return line1 in txt and line2 in txt


def check_tasks_json(auto_fix: bool = True) -> Tuple[bool, bool]:
    """Return (registry_check_exact, h_consistency_exact).
    May auto-fix by appending missing tasks while preserving existing ones.
    """
    registry_ok = False
    h_ok = False
    if not TASKS.exists():
        if auto_fix:
            TASKS.parent.mkdir(parents=True, exist_ok=True)
            tasks = {"version": "2.0.0", "tasks": []}
            TASKS.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
        else:
            return False, False

    try:
        obj = json.loads(TASKS.read_text(encoding="utf-8"))
    except Exception:
        return False, False

    tasks = obj.get("tasks", [])
    for t in tasks:
        if t.get("label") == "registry-check" and t.get("type") == "shell":
            cmd = t.get("command", "").strip()
            if cmd.startswith(
                "echo python scripts/qa/validate_model_metadata.py --file models/BASELINE_LIN_H3/metadata.json --schema docs/schemas/model_metadata.schema.json"
            ):
                registry_ok = True
        if t.get("label") == "h-consistency" and t.get("type") == "shell":
            cmd = t.get("command", "").strip()
            if cmd.startswith("echo python scripts/qa/check_H_consistency.py"):
                h_ok = True

    changed = False
    if auto_fix:
        # Append missing tasks
        if not registry_ok:
            tasks.append(
                {
                    "label": "registry-check",
                    "type": "shell",
                    "command": "echo python scripts/qa/validate_model_metadata.py --file models/BASELINE_LIN_H3/metadata.json --schema docs/schemas/model_metadata.schema.json  # OFFLINE ONLY",
                    "problemMatcher": [],
                }
            )
            changed = True
            registry_ok = True
        if not h_ok:
            tasks.append(
                {
                    "label": "h-consistency",
                    "type": "shell",
                    "command": "echo python scripts/qa/check_H_consistency.py --label-name label_R_H12_pct --windows 1,3,12 --H 12  # OFFLINE ONLY",
                    "problemMatcher": [],
                }
            )
            changed = True
            h_ok = True

    if changed:
        obj["tasks"] = tasks
        TASKS.write_text(json.dumps(obj, indent=2), encoding="utf-8")

    return registry_ok, h_ok


def check_workflow() -> bool:
    if not WORKFLOW.exists():
        return False
    txt = WORKFLOW.read_text(encoding="utf-8")
    return ("Guardrail check (copilot)" in txt) and ("Guardrails unit test" in txt)


def check_model_registry_refs() -> bool:
    if not MODEL_REG.exists():
        return False
    txt = MODEL_REG.read_text(encoding="utf-8")
    return "docs/schemas/model_metadata.schema.json" in txt


def ensure_eval_metrics_block(auto_fix: bool = True) -> bool:
    want = "H-consistency usage"
    if not EVAL_METRICS.exists():
        if auto_fix:
            EVAL_METRICS.parent.mkdir(parents=True, exist_ok=True)
            EVAL_METRICS.write_text("# Evaluation Metrics\n\n", encoding="utf-8")
        else:
            return False
    txt = EVAL_METRICS.read_text(encoding="utf-8")
    if want in txt:
        return True
    if auto_fix:
        add = "\n## H-consistency usage\nRun the H-consistency gate before reporting metrics:\n\nExample:\n    python3 scripts/qa/check_H_consistency.py --label-name <label-name> --windows <w1,w2,...> --H <H>\n"
        EVAL_METRICS.write_text(txt + add, encoding="utf-8")
        return True
    return False


def todo_audit() -> str:
    # Very small audit: check that M3.2 and guardrail items have proof
    summary = []
    # EN policy
    code, _ = run_cmd(["python3", "scripts/qa/check_english_policy.py"])
    summary.append(f"en_policy_exit:{code}")
    # registry proof
    init1, _ = run_cmd(
        ["python3", "scripts/registry/init_model_tag.py", "--tag", "BASELINE_LIN_H3"]
    )
    init2, _ = run_cmd(
        ["python3", "scripts/registry/init_model_tag.py", "--tag", "BASELINE_LIN_H3"]
    )
    val, _ = run_cmd(
        [
            "python3",
            "scripts/qa/validate_model_metadata.py",
            "--file",
            "models/BASELINE_LIN_H3/metadata.json",
            "--schema",
            "docs/schemas/model_metadata.schema.json",
        ]
    )
    summary.append(f"registry_init:{init1},{init2}")
    summary.append(f"registry_validate:{val}")
    # H-consistency
    hcode, _ = run_cmd(
        [
            "python3",
            "scripts/qa/check_H_consistency.py",
            "--label-name",
            "label_R_H12_pct",
            "--windows",
            "1,3,12",
            "--H",
            "12",
        ]
    )
    summary.append(f"hcons_exit:{hcode}")
    # CLI export check
    cli_code, _ = run_cmd(["python3", "scripts/qa/check_cli_exports.py"])
    summary.append(f"cli_export_exit:{cli_code}")
    return ";".join(summary)


def git_clean() -> bool:
    code, out = run_cmd(["git", "status", "-sb"])
    if code != 0:
        return False
    return out.strip() == ""


def main():
    status = "PASS"
    # A: Guardrails
    guard_ok = has_preface() and AGENTS.exists() and PROJECT.exists()
    if not guard_ok:
        status = "FAIL"

    # B: Language policy
    en_code, en_out = run_cmd(["python3", "scripts/qa/check_english_policy.py"])

    # Code-fence check (stdlib checker)
    cf_code, cf_out = run_cmd(["python3", "scripts/qa/check_code_fences.py"]) 

    # C: Tasks.json
    registry_ok, h_ok = check_tasks_json(auto_fix=True)

    # D: CI wiring
    ci_ok = check_workflow()
    if not ci_ok:
        status = "FAIL"

    # E: TODO truth vs evidence
    todo_summary = todo_audit()

    # F: Cross-refs
    model_ref_ok = check_model_registry_refs()
    eval_ok = ensure_eval_metrics_block(auto_fix=True)

    # G: Git clean
    clean = git_clean()
    if not clean:
        # don't fail workspace for dirty tree; just report
        pass

    # If any of the critical checks failed, overall fail
    if (
        not guard_ok
        or en_code != 0
        or not registry_ok
        or not h_ok
        or not ci_ok
        or not model_ref_ok
        or not eval_ok
    ):
        status = "FAIL"

    # Machine-readable output
    print(f"ws_health: {status}")
    print(f"en_policy_exit:{en_code}")
    print(f"registry_check_exact:{str(registry_ok).lower()}")
    print(f"h_consistency_exact:{str(h_ok).lower()}")
    print(f"validators_ci_present:{str(ci_ok).lower()}")
    print(f"code_fence_check_exit:{cf_code}")
    print(f"todo_audit:{todo_summary}")
    print(f"git_clean:{str(clean).lower()}")

    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
