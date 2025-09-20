### 2025-09-20 - Smoke-backtest workflow added
- Created branch `chore/smoke-backtest-notify` and opened PR: https://github.com/JosefVacha/matrix/pull/17
- Added `.github/workflows/smoke-backtest.yml` (scheduled/manual) to run ingest tests, generate deterministic smoke dataset, export predictions, run paper-trading simulator with predictions, extract metrics, compare to baseline, and upload artifacts.
- Workflow includes a placeholder Slack notifier; maintainers can enable it by adding `SLACK_WEBHOOK_URL` repository secret.

CZ: Přidán workflow pro smoke-backtest (denní/manual). Notifikátor Slack je placeholder — přidejte `SLACK_WEBHOOK_URL` v repo secrets pro aktivaci.
