#!/usr/bin/env bash
set -euo pipefail

# Run full detect-secrets scan and fail if any findings are present
python -m detect_secrets.scan --all-files --json > /tmp/detect_output.json || true
python - <<'PY'
import json,sys
r=json.load(open('/tmp/detect_output.json'))
if any(len(v)>0 for v in r.get('results',{}).values()):
    print('detect-secrets found potential secrets; failing CI')
    sys.exit(1)
print('no secrets found')
PY
