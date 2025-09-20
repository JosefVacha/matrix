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
    subprocess.check_call(cmd, shell=True)


def main():
    repo = os.environ.get('GITHUB_REPOSITORY')
    token = os.environ.get('GITHUB_TOKEN')
    if not repo or not token:
        print('GITHUB_REPOSITORY or GITHUB_TOKEN missing; cannot create PR')
        return 2

    branch = f"baseline-update-{os.getpid()}"
    run(f"git config user.email 'actions@github.com'")
    run(f"git config user.name 'GitHub Actions'")
    run(f"git checkout -b {branch}")

    # write baseline
    cur = Path('outputs/paper_trade_metrics.json')
    if not cur.exists():
        print('Current metrics missing; abort')
        return 3
    data = json.loads(cur.read_text())
    Path('ci/baselines').mkdir(parents=True, exist_ok=True)
    Path('ci/baselines/paper_trade_metrics_baseline.json').write_text(json.dumps(data, indent=2))

    run('git add ci/baselines/paper_trade_metrics_baseline.json')
    run('git commit -m "chore(ci): update baseline metrics (auto)"')
    run(f"git push https://x-access-token:{token}@github.com/{repo} HEAD:{branch}")

    # create PR
    payload = json.dumps({
        'title': 'chore(ci): update baseline metrics (auto)',
        'head': branch,
        'base': 'main',
        'body': 'Auto-generated baseline update from smoke run.'
    })
    run(f"curl -s -X POST -H \"Authorization: token {token}\" -H \"Content-Type: application/json\" -d '{payload}' https://api.github.com/repos/{repo}/pulls")
    print('PR created (attempted)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
