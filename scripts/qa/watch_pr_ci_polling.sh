#!/usr/bin/env bash
set -euo pipefail

# Simple opt-in polling watcher for PR CI runs and artifacts.
# Usage: watch_pr_ci_polling.sh <pr-or-branch> [--interval SECONDS] [--once]

PR_IDENT=${1:-}
if [ -z "${PR_IDENT}" ]; then
  echo "Usage: $0 <pr-or-branch> [--interval SECONDS] [--once]"
  exit 2
fi

INTERVAL=30
ONCE=0
AUTO_NOTIFY=0
MAX_BACKOFF=300
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --interval)
      INTERVAL=${2:-}
      shift 2
      ;;
    --auto-notify)
      AUTO_NOTIFY=1
      shift
      ;;
    --once)
      ONCE=1
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

echo "Watching PR/branch: ${PR_IDENT} (interval=${INTERVAL}s)"

fetch_runs() {
  # Uses gh CLI if available, otherwise prints a friendly hint.
  if command -v gh >/dev/null 2>&1; then
    gh run list --branch "${PR_IDENT}" --limit 5 --json databaseId,name,status,conclusion,createdAt -q '.[] | {id: .databaseId, name: .name, status: .status, conclusion: .conclusion, createdAt: .createdAt}' || true
  else
    echo "gh CLI not found; install 'gh' to enable automatic run listing." >&2
  fi
}

download_artifacts() {
  if ! command -v gh >/dev/null 2>&1; then
    echo "gh CLI not available; skipping artifact download." >&2
    return
  fi
  # Download artifacts for the most recent run for the branch/pr
  local run_id
  run_id=$(gh run list --branch "${PR_IDENT}" --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null || true)
  if [ -z "${run_id}" ] || [ "null" = "${run_id}" ]; then
    echo "No recent run found for ${PR_IDENT}" >&2
    return
  fi
  echo "Downloading artifacts for run ${run_id}..."
  mkdir -p outputs/ci-artifacts
  gh run download "${run_id}" -D outputs/ci-artifacts || true
}

while true; do
  echo "[watch_pr_ci_polling] $(date --iso-8601=seconds) — fetching runs..."
  fetch_runs || true
  if download_artifacts; then
    # reset backoff on success
    BACKOFF=0
  else
    # increase backoff up to MAX_BACKOFF
    BACKOFF=$((BACKOFF+INTERVAL))
    if [ -z "${BACKOFF}" ] || [ "${BACKOFF}" -lt 1 ]; then BACKOFF=${INTERVAL}; fi
    if [ "${BACKOFF}" -gt "${MAX_BACKOFF}" ]; then BACKOFF=${MAX_BACKOFF}; fi
    echo "No artifacts or download failed; backing off ${BACKOFF}s"
    sleep "${BACKOFF}"
  fi

  # optional: scan downloaded artifacts for guardrail failure JSON and auto-notify
  if [ "${AUTO_NOTIFY}" -eq 1 ] && [ -d outputs/ci-artifacts ]; then
    for jf in outputs/ci-artifacts/**/guardrail_check.json outputs/ci-artifacts/guardrail_check.json; do
      [ -e "$jf" ] || continue
      echo "Found guardrail artifact: $jf"
      if python3 -c 'import json,sys
f=sys.argv[1]
o=json.load(open(f))
print(o.get("ok") is not True)
' "$jf" | grep -q True; then
        echo "Guardrail failure detected in $jf"
        if [ -x scripts/qa/notify_guardrail_failure.py ] || [ -f scripts/qa/notify_guardrail_failure.py ]; then
          echo "Auto-notify enabled; invoking notifier for $jf"
          python3 scripts/qa/notify_guardrail_failure.py --input-file "$jf" || true
        fi
      fi
    done
  fi
  if [ "${ONCE}" -eq 1 ]; then
    echo "--once specified; exiting after one iteration"
    exit 0
  fi
  # if we used BACKOFF above, loop already slept; otherwise sleep for INTERVAL
  if [ -n "${BACKOFF:-}" ] && [ "${BACKOFF}" -gt 0 ]; then
    continue
  fi
  sleep "${INTERVAL}"
done
