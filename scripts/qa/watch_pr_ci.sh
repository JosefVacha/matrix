#!/usr/bin/env bash
# Helper: watch PR CI runs using gh CLI
# Usage: ./scripts/qa/watch_pr_ci.sh <pr-number-or-branch>

set -euo pipefail
PR_OR_REF=${1:-}
REPO=${GITHUB_REPOSITORY:-$(git config --get remote.origin.url | sed -n 's#.*/\([^/.]*\)\.git#\1#p')}

if [ -z "$PR_OR_REF" ]; then
  echo "Usage: $0 <pr-number|branch-name>"
  echo "Example: $0 12   # PR number"
  echo "         $0 chore/qa-guardrails  # branch name"
  exit 2
fi

# Determine branch name if PR number provided
if [[ "$PR_OR_REF" =~ ^[0-9]+$ ]]; then
  PR_NUM=$PR_OR_REF
  BRANCH=$(gh pr view "$PR_NUM" --json headRefName -q .headRefName) || {
    echo "Failed to query PR $PR_NUM via gh"; exit 3
  }
else
  BRANCH=$PR_OR_REF
fi

echo "Repo: ${REPO}" 
echo "Watching branch: ${BRANCH}"

echo "Recent workflow runs for branch (smoke-validators and simulate-notifier):"
# List latest runs for two relevant workflows
gh run list --repo "${REPO}" --branch "${BRANCH}" --workflow smoke-validators.yml -L 10 || true
gh run list --repo "${REPO}" --branch "${BRANCH}" --workflow simulate-notifier-dispatch.yml -L 10 || true

# Show most recent run details and artifacts for the smoke-validators workflow
LATEST_RUN_ID=$(gh run list --repo "${REPO}" --branch "${BRANCH}" --workflow smoke-validators.yml -L 1 --json databaseId -q '.[0].databaseId' || true)
if [ -n "$LATEST_RUN_ID" ] && [ "$LATEST_RUN_ID" != "null" ]; then
  echo "\nDetails for latest smoke-validators run id=${LATEST_RUN_ID}:"
  gh run view "$LATEST_RUN_ID" --repo "${REPO}" --log --json conclusion,createdAt,artifacts
  echo "Artifacts (if any):"
  gh run view "$LATEST_RUN_ID" --repo "${REPO}" --log || true
  echo "Use 'gh run download $LATEST_RUN_ID --repo ${REPO} -D outputs/<dir>' to fetch artifacts"
else
  echo "No recent smoke-validators runs found for branch ${BRANCH}."
fi

exit 0
