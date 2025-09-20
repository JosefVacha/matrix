## Developer convenience targets for local CI hygiene

.PHONY: precommit detect-secrets-scan venv

precommit:
	@echo "Running pre-commit hooks (install pre-commit first: pip install pre-commit)"
	pre-commit run --all-files

detect-secrets-scan:
	@echo "Running detect-secrets scan (uses .secrets.baseline if present)"
	python3 -m pip install detect-secrets==1.4.0
	./scripts/ci/run_detect_secrets.sh || true

venv:
	python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install -r requirements-dev.txt
# Makefile: helper targets for maintainers


.PHONY: run-guardrails simulate-notifier run-tests ci-lint

run-guardrails:
	python3 scripts/qa/check_copilot_guardrails.py --json --output-file outputs/guardrail_check.json
	@echo "Wrote outputs/guardrail_check.json"

# Usage: make simulate-notifier REPO=owner/repo
simulate-notifier:
	@echo "Triggering simulate-notifier dispatch via gh..."
	@REPO=$${REPO:-$${GITHUB_REPOSITORY:-$(shell git config --get remote.origin.url | sed 's#.*/\([^.]*\)\.git#\1#')}}; \
	if [ -z "$$REPO" ]; then echo "Could not determine repo; set REPO=owner/repo"; exit 1; fi; \
	gh workflow run simulate-notifier-dispatch.yml --repo $$REPO

run-tests:
	python3 -m pytest -q

# Run linters/formatters if available; non-fatal
ci-lint:
	@echo "Running ci-lint (non-fatal if tools missing)"
	@command -v black >/dev/null 2>&1 && black . || echo "black not installed; skipping"
	@command -v flake8 >/dev/null 2>&1 && flake8 || echo "flake8 not installed; skipping"

fetch-artifacts:
	@echo "Fetch artifacts for a run: make fetch-artifacts RUN_ID=<id>"
	@RUN_ID=$${RUN_ID:-}; \
	if [ -z "$$RUN_ID" ]; then echo "Please set RUN_ID"; exit 1; fi; \
	gh run download $$RUN_ID -D outputs/ || echo "download failed or no artifacts"

watch-pr-ci:
	@echo "Opt-in: watch PR/branch CI runs and download artifacts"
	@echo "Usage: make watch-pr-ci PR=<pr-or-branch> [INTERVAL=30] [ONCE=1]"
	@PR=$${PR:-}; \
	if [ -z "$$PR" ]; then echo "Please set PR=<pr-or-branch>"; exit 2; fi; \
	INTERVAL=$${INTERVAL:-30}; ONCE=$${ONCE:-0}; \
	bash scripts/qa/watch_pr_ci_polling.sh $$PR --interval $$INTERVAL $$( [ "$$ONCE" -eq 1 ] && echo --once )

paper-trade-sim:
	@echo "Run paper trading simulator against smoke dataset"
	@python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json || true
