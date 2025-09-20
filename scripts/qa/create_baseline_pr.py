#!/usr/bin/env python3
"""Create a PR updating the baseline file.

This script expects GITHUB_TOKEN in env and git remote is set. It will:
 - create a branch
 - write outputs/paper_trade_metrics.json to ci/baselines/paper_trade_metrics_baseline.json
 - push the branch
 - open a PR via the GitHub API
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def run(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        # In dry-run or test environments git may be missing; surface a warning but continue
        print(f"Warning: command failed: {cmd}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-push', action='store_true', help='Allow pushing the baseline branch and creating the PR (requires ALLOW_NOTIFICATIONS=1)')
    parser.add_argument('--base-branch', default=os.environ.get('BASE_BRANCH','main'), help='Base branch for the PR')
    args = parser.parse_args()

    repo = os.environ.get('GITHUB_REPOSITORY')
    token = os.environ.get('GITHUB_TOKEN')
    allow_notifications = os.environ.get('ALLOW_NOTIFICATIONS') == '1'
    if not repo:
        print('GITHUB_REPOSITORY missing; cannot compute remote URL')
        return 2

    branch = f"baseline-update-{os.getpid()}"
    run("git config user.email 'actions@github.com'")
    run("git config user.name 'GitHub Actions'")
    run(f"git checkout -b {branch}")

    # read current metrics artifact
    cur = Path('outputs/paper_trade_metrics.json')
    if not cur.exists():
        print('Current metrics missing; abort')
        return 3
    data = json.loads(cur.read_text())
    Path('ci/baselines').mkdir(parents=True, exist_ok=True)
    # prepare new baseline file contents (not written until allow-push)
    new_baseline_path = Path('ci/baselines/paper_trade_metrics_baseline.json')
    proposed_baseline_text = json.dumps(data, indent=2)

    # create PR payload (dry-run friendly)
    # compute diff for PR body
    old = None
    base_file = Path('ci/baselines/paper_trade_metrics_baseline.json')
    if base_file.exists():
        old = json.loads(base_file.read_text())
    new = data
    old_final = float(old.get('final_net')) if old else None
    new_final = float(new.get('final_net'))
    delta = new_final - (old_final if old_final is not None else 0.0)
    pct = (delta / old_final * 100.0) if old_final not in (None, 0.0) else None

    body_lines = [
        'Auto-generated baseline update from smoke run.',
        '',
        'Metrics change:',
        f"- old_final_net: {old_final if old_final is not None else 'n/a'}",
        f"- new_final_net: {new_final}",
        f"- delta: {delta}",
        f"- delta_pct: {pct if pct is not None else 'n/a'}",
        f"- new_trades_count: {int(new.get('trades_count',0))}",
    ]

    payload = {
        'title': 'chore(ci): update baseline metrics (auto)',
        'head': branch,
        'base': args.base_branch,
        'body': '\n'.join(body_lines)
    }

    print('\n--- Proposed baseline PR payload (dry-run) ---')
    print(json.dumps(payload, indent=2))
    print('\n--- Proposed baseline file (ci/baselines/paper_trade_metrics_baseline.json) ---')
    print(proposed_baseline_text)

    # If allow-push requested, perform network writes — only allowed when ALLOW_NOTIFICATIONS=1
    if args.allow_push:
        if not token:
            print('GITHUB_TOKEN missing; cannot push or create PR')
            return 4
        if not allow_notifications:
            print('ALLOW_NOTIFICATIONS != "1"; refusing to perform remote writes. Set ALLOW_NOTIFICATIONS=1 to allow this action.')
            return 5

        # write baseline file, commit, push, then create PR
        new_baseline_path.write_text(proposed_baseline_text)
        run('git add ci/baselines/paper_trade_metrics_baseline.json')
        run('git commit -m "chore(ci): update baseline metrics (auto)"')
        run(f"git push https://x-access-token:{token}@github.com/{repo} HEAD:{branch}")

        # create PR via API
        import urllib.request

        req = urllib.request.Request(
            f'https://api.github.com/repos/{repo}/pulls',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'token {token}',
                'Content-Type': 'application/json',
                'User-Agent': 'matrix-baseline-bot'
            },
            method='POST'
        )
        with urllib.request.urlopen(req) as resp:
            print('PR response:', resp.status)
            print(resp.read().decode())
        print('PR created')
    else:
        print('\nDry-run complete. To perform the push and create a PR run with --allow-push and set ALLOW_NOTIFICATIONS=1 in the environment.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
