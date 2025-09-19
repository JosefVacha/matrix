#!/usr/bin/env python3
"""Zero-deps workspace health unit test.

Run with: python3 -m tests.test_workspace_health
"""

import subprocess
import sys


def main():
    try:
        p = subprocess.run([sys.executable, 'scripts/qa/check_workspace_health.py'], capture_output=True, text=True)
    except Exception as e:
        print(f'workspace_health_test: fail:exec-error:{e}')
        sys.exit(1)
    if p.returncode != 0:
        print(f'workspace_health_test: fail:rc={p.returncode}')
        print(p.stdout)
        print(p.stderr)
        sys.exit(1)
    print('workspace_health_test: pass')
    sys.exit(0)


if __name__ == '__main__':
    main()
