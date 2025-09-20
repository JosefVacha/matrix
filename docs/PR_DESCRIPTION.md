## PR: Hardening guardrails, notifier, CI wiring, and dev hygiene

Summary
- Add conservative guardrail runner and machine-readable JSON output: `scripts/qa/check_copilot_guardrails.py`
- Add a safe notifier that writes artifacts and can (opt-in) create GitHub issues or post to Slack: `scripts/qa/notify_guardrail_failure.py`
- Add an opt-in CI watcher and Makefile helpers: `scripts/qa/watch_pr_ci_polling.sh`, `Makefile` target `watch-pr-ci`
- Enforce mandatory two-line audit preface in PRs via `scripts/qa/check_pr_preface.py` and run it early in the validators job
- Add documentation and maintainer guidance (docs/*) and unit tests for new behavior

Key files changed
- scripts/qa/check_copilot_guardrails.py — machine-readable guardrail checker
- scripts/qa/notify_guardrail_failure.py — notifier (safe-by-default; requires ALLOW_NOTIFICATIONS=1 and explicit flags)
- scripts/qa/check_pr_preface.py — rejects PRs missing audit preface
- scripts/qa/watch_pr_ci_polling.sh — opt-in watcher with backoff and optional auto-notify
- Makefile — helper targets (run-guardrails, watch-pr-ci, simulate-notifier)
- docs/NOTIFIER_USAGE.md, docs/WATCHER_SERVICE.md, docs/PR_MAINTAINER_GUIDE.md — docs for maintainers

Security & Safety
- Notifier is conservative by default: it always writes a local artifact but WILL NOT perform any remote action unless both (a) the caller passes `--enable-issues`/`--enable-slack` and (b) the environment variable `ALLOW_NOTIFICATIONS=1` is set.
- This replicable two-step requirement prevents accidental issue creation or Slack posts from casual CLI runs or from untrusted CI.
- CI workflows will not enable notifications by default; maintainers must opt-in via secrets and explicit configuration.

How to test locally
1. Run guardrails:

```
python3 scripts/qa/check_copilot_guardrails.py --json --output-file outputs/guardrail_check.json
cat outputs/guardrail_check.json
```

2. Dry-run notifier (no remote actions):

```
python3 scripts/qa/notify_guardrail_failure.py --input-file outputs/test_guardrail_fake.json --dry-run
```

3. Start watcher in dry-run:

```
make watch-pr-ci PR=chore/qa-guardrails ONCE=1 INTERVAL=5
```

Notes for reviewers
- Verify `copilot-instructions.md` contains the required two-line audit preface.
- Review `Knowledge/REPLY_TEMPLATES.md` for Czech template consistency.
- Confirm CI secrets policy before enabling notifier in workflows.
