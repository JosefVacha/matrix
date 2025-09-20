#!/usr/bin/env bash
set -euo pipefail
# Safe helper to dispatch the propose_baseline_pr workflow with allow_push=true
# Usage: ALLOW_NOTIFICATIONS=1 ./scripts/qa/dispatch_propose_baseline.sh [ref] [metrics-json]

REPO="${GITHUB_REPOSITORY:-JosefVacha/matrix}"
REF="${1:-chore/qa-guardrails}"
METRICS="${2:-'{"final_net":0.01}'}"

if [ "${ALLOW_NOTIFICATIONS:-}" != "1" ]; then
  echo "Refusing to dispatch: ALLOW_NOTIFICATIONS != 1 (must be set to '1' in env)."
  echo "Set the repository secret ALLOW_NOTIFICATIONS=1 or export ALLOW_NOTIFICATIONS=1 locally before running."
  exit 2
fi

echo "Preflight checks:"
echo "- gh installed? -> $(command -v gh >/dev/null && echo yes || echo no)"
if ! command -v gh >/dev/null; then
  echo "Please install GitHub CLI and authenticate (gh auth login) before running."
  exit 3
fi

echo "- gh auth status:" 
gh auth status || true

echo "Dispatching workflow propose_baseline_pr.yml -> repo=${REPO} ref=${REF} allow_push=true"

# Use gh workflow run; metrics may need quoting as JSON string
gh workflow run propose_baseline_pr.yml --repo "${REPO}" --ref "${REF}" --field allow_push=true --field metrics="${METRICS}"

echo "Workflow dispatched. Monitor with: gh run watch --repo ${REPO} or gh run list --repo ${REPO}"

exit 0
