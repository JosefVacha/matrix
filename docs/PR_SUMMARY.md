# PR Summary — guardrails, baseline automation, and simulator

This file provides a short summary of the draft PR (branch: `chore/qa-guardrails-notifier-ready`, PR: https://github.com/JosefVacha/matrix/pull/10) and highlights the most review-relevant files and rationale.

1) Goal
- Harden QA guardrails and developer hygiene.
- Provide a deterministic paper-trade smoke simulator and metrics extraction.
- Add a safe, dry-run-first baseline proposal pipeline that can be opt‑in to create PRs.

2) High-impact files to review
- `scripts/qa/check_copilot_guardrails.py` — guardrail runner (must PASS before edits)
- `scripts/trading/paper_trading_sim.py` — deterministic simulator (writes JSON + CSV)
- `scripts/qa/extract_paper_trade_metrics.py` — metrics extractor used by CI
- `ci/baselines/paper_trade_metrics_baseline.json` — seeded baseline values
- `scripts/qa/create_baseline_pr.py` — dry-run-first PR creator; network writes gated by `--allow-push` and `ALLOW_NOTIFICATIONS=1`
- `.github/workflows/propose_baseline_pr.yml` — manual dispatch workflow that runs simulation, extracts metrics, uploads artifacts, and optionally proposes a baseline PR
- `docs/RUNBOOK.md`, `docs/CI_RUN_INSTRUCTIONS.md`, `docs/PR_REVIEW_CHECKLIST.md` — playbook and run instructions for maintainers

3) Rationale & Safety
- All remote writes are opt-in and double gated (CLI flag + repo secret). Default behavior is dry-run only.
- The simulator is intentionally small and deterministic (no external calls) so CI smoke runs are fast and reproducible.
- Baseline creation is automated only when the team explicitly enables it and inspects a dry-run first.

4) Suggested review order
  1. Run `scripts/qa/check_copilot_guardrails.py` locally — verify PASS
 2. Run the smoke simulator + extractor and compare metrics locally
 3. Inspect the `create_baseline_pr.py` payload printed in dry-run mode
 4. Check the workflow logs/artifacts from a dry-run (see `docs/CI_RUN_INSTRUCTIONS.md`) before enabling push

5) Quick decisions for maintainers
- If acceptable: set `ALLOW_NOTIFICATIONS=1` and optionally provide `DEFAULT_PR_REVIEWERS` and `DEFAULT_PR_LABELS` envs to have created PRs automatically request reviewers and add labels.
- If any remote-write behavior is not acceptable, keep workflows dry-run and merge only the simulator/guardrail docs parts.

6) Contact
- If you want me to run a dry-run dispatch and gather artifacts now, say so and I will prepare/execute the `gh workflow run` command (dry-run only).
