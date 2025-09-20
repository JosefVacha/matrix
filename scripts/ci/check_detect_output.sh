#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json,sys,os
r=json.load(open('/tmp/detect_output.json'))
found = any(len(v)>0 for v in r.get('results',{}).values())
# write to GITHUB_OUTPUT for GitHub Actions
out=os.environ.get('GITHUB_OUTPUT')
if out:
    with open(out,'a') as f:
        f.write(f'found={str(found).lower()}\n')
# also print
print('found=', found)
if found:
    exit 0
PY
