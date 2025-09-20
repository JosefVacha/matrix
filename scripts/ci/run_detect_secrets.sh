#!/usr/bin/env bash
set -euo pipefail

# Run detect-secrets in baseline-aware mode when a baseline exists.
# - Writes JSON output to /tmp/detect_output.json
# - Exits with status 1 when new findings are present (so PR job fails)

BASELINE_FILE=".secrets.baseline"
OUTPUT_FILE="/tmp/detect_output.json"

echo "Running detect-secrets scan..."

# Build a file list from git tracked files and exclude common noisy paths
EXCLUDE_PATTERNS=(".venv" "venv" "node_modules" "__pycache__" "*.pyc" "*.pkl" "*.parquet" "tests/__pycache__" "/.pytest_cache" "outputs/" "ci-artifacts/")

# Use printf and grep -vF to filter
FILES=$(git ls-files | grep -v -E '\.venv|venv|node_modules|__pycache__|\.pyc$|\.pkl$|\.parquet$|tests/__pycache__|\.pytest_cache|^outputs/|^ci-artifacts/') || true

if [ -z "$FILES" ]; then
        echo "No files to scan after exclusions; falling back to --all-files"
                if [ -f "$BASELINE_FILE" ]; then
                        python3 -m detect_secrets.scan --all-files --baseline "$BASELINE_FILE" --json > "$OUTPUT_FILE" || true
                else
                        python3 -m detect_secrets.scan --all-files --json > "$OUTPUT_FILE" || true
                fi
else
        # write file list to a temp file and pass to detect-secrets
        echo "$FILES" > /tmp/detect_file_list.txt
                if [ -f "$BASELINE_FILE" ]; then
                        python3 -m detect_secrets.scan --files $(cat /tmp/detect_file_list.txt) --baseline "$BASELINE_FILE" --json > "$OUTPUT_FILE" || true
                else
                        python3 -m detect_secrets.scan --files $(cat /tmp/detect_file_list.txt) --json > "$OUTPUT_FILE" || true
                fi
fi

python - <<'PY'
import json,sys,os
p = os.path.abspath('/tmp/detect_output.json')
if not os.path.exists(p):
        print('No detect-secrets output found at', p)
        sys.exit(0)
r=json.load(open(p))
# `results` maps filenames to a list of findings. If any file has findings, fail.
found = False
for f, entries in r.get('results', {}).items():
        if len(entries) > 0:
                print(f"FOUND: {f} -> {len(entries)} potential secrets")
                found = True

if found:
        print('\nSummary: detect-secrets found potential secrets; failing CI')
        # print the full JSON for convenience in logs
        print('\nFull JSON output:')
        print(json.dumps(r, indent=2))
        sys.exit(1)

print('No (new) secrets found')
PY
