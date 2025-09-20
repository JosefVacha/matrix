#!/usr/bin/env python3
"""Notify about guardrail failures.

Behavior:
- Runs `scripts/qa/check_copilot_guardrails.py --json` (or reads JSON from --input-file).
- If ok: prints message and exits 0.
- If failed: writes a timestamped JSON to `outputs/guardrail_failure-<ts>.json` and
  - if `gh` CLI is available and `GITHUB_TOKEN` in env, attempts to create a GitHub issue (best-effort).
  - otherwise prints instructions for the maintainer.

This script is intentionally conservative: it will not attempt any destructive actions.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
import os
import urllib.request
import urllib.error


def run_guardrail_json() -> dict:
    try:
        p = subprocess.run(
            [sys.executable, "scripts/qa/check_copilot_guardrails.py", "--json"],
            capture_output=True,
            text=True,
        )
        out = p.stdout.strip()
        if not out:
            return {"ok": False, "error": "no output"}
        return json.loads(out)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def write_artifact(data: dict) -> Path:
    outdir = Path("outputs")
    outdir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    p = outdir / f"guardrail_failure-{ts}.json"
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return p


def try_create_issue(title: str, body: str) -> bool:
    # Prefer GitHub REST API when token and repo are available
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if token and repo:
        try:
            url = f"https://api.github.com/repos/{repo}/issues"
            data = json.dumps({"title": title, "body": body}).encode("utf-8")
            req = urllib.request.Request(url, data=data, method="POST")
            req.add_header("Authorization", f"token {token}")
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                issue_url = resp_data.get("html_url")
                if issue_url:
                    print("Created GitHub issue:", issue_url)
                    return True
            print("GitHub API: unexpected response; could not determine issue URL")
        except urllib.error.HTTPError as e:
            try:
                err = e.read().decode()
            except Exception:
                err = str(e)
            print("GitHub API error:", err)
        except Exception as e:
            print("Error while creating issue via GitHub API:", e)

    # Fallback to gh CLI if available
    gh = shutil_which("gh")
    if not gh:
        print("gh CLI not available; skipping gh CLI fallback")
        return False
    try:
        cmd = ["gh", "issue", "create", "--title", title, "--body", body]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            print("Created GitHub issue via gh:", p.stdout.strip())
            return True
        print("gh issue create failed:", p.stderr)
        return False
    except Exception as e:
        print("Error while creating issue via gh CLI:", e)
        return False


def shutil_which(cmd: str):
    from shutil import which

    return which(cmd)


def main():
    # allow reading precomputed JSON via --input-file
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", help="Path to guardrail JSON output (optional)")
    parser.add_argument("--enable-issues", action="store_true", help="Allow creating GitHub issues (off by default)")
    parser.add_argument("--enable-slack", action="store_true", help="Allow posting to Slack webhook (off by default)")
    parser.add_argument("--dry-run", action="store_true", help="Do not perform any remote actions; print what would be done")
    args = parser.parse_args()

    if args.input_file:
        try:
            data = json.loads(Path(args.input_file).read_text(encoding="utf-8"))
        except Exception as e:
            print("Failed to read input file:", e)
            sys.exit(2)
    else:
        data = run_guardrail_json()

    if data.get("ok"):
        print("Guardrail OK — no action needed")
        sys.exit(0)

    art = write_artifact(data)
    print(f"Wrote guardrail failure artifact: {art}")

    title = "Guardrail check failed: repository guardrails"
    # Avoid embedding triple-backticks in Python source; some validators scan for code-fence artifacts.
    body = (
        "Guardrail check failed. See attached artifact.\n\nJSON:\n"
        + json.dumps(data, indent=2)
        + "\n"
    )
    # Optionally post to Slack if a webhook is configured and the caller enabled it
    # Additionally require ALLOW_NOTIFICATIONS=1 in the environment to permit any remote actions.
    allow = os.environ.get("ALLOW_NOTIFICATIONS") == "1"
    slack_webhook = os.environ.get("SLACK_WEBHOOK")
    if not allow and (args.enable_slack or args.enable_issues):
        print("Remote notifications are disabled. Set ALLOW_NOTIFICATIONS=1 to allow creating issues or posting to Slack.")

    if args.dry_run:
        print("Dry-run mode: no remote actions will be performed even if enables/ALLOW_NOTIFICATIONS are set")

    if args.enable_slack and slack_webhook and allow and (not args.dry_run):
        try:
            payload = json.dumps(
                {
                    "text": f"Guardrail failure in {os.environ.get('GITHUB_REPOSITORY', '<repo>')}: {title}\nSee artifact: {art}"
                }
            ).encode("utf-8")
            req = urllib.request.Request(slack_webhook, data=payload, method="POST")
            req.add_header("Content-Type", "application/json")
            urllib.request.urlopen(req, timeout=10)
            print("Posted Slack notification (webhook)")
        except Exception as e:
            print("Failed posting to Slack webhook:", e)
    elif not args.enable_slack and slack_webhook:
        print("Slack webhook available but not enabled (use --enable-slack to allow posting)")

    created = False
    if args.enable_issues and allow and (not args.dry_run):
        created = try_create_issue(title, body)
    elif args.enable_issues and not allow:
        print("Issue creation requested but ALLOW_NOTIFICATIONS!=1; skipping issue creation")
    elif args.enable_issues and args.dry_run:
        print("Dry-run: would create GitHub issue but --dry-run was set; not creating")
    else:
        print("Issue creation disabled (use --enable-issues to allow creating GitHub issues)")

    if not created:
        print("To create an issue manually, run:")
        print(f'  gh issue create --title "{title}" --body-file {art}')
    sys.exit(1)


if __name__ == "__main__":
    main()
