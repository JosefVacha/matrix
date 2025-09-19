#!/usr/bin/env bash
# Install a lightweight pre-commit hook that runs quick QA checks locally.
# This script will copy a pre-commit script into .git/hooks/pre-commit but
# will not enable any other tooling.

set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
HOOK_DIR="$ROOT/.git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

mkdir -p "$HOOK_DIR"
cat > "$HOOK_FILE" <<'HOOK'
#!/usr/bin/env bash
echo "Running lightweight pre-commit QA checks..."
python3 scripts/qa/check_code_fences.py || { echo "Code-fence check failed"; exit 1; }
python3 scripts/qa/check_cli_exports.py || { echo "CLI export check failed"; exit 1; }
echo "Pre-commit QA checks passed"
exit 0
HOOK

chmod +x "$HOOK_FILE"
echo "Installed pre-commit hook at $HOOK_FILE"
