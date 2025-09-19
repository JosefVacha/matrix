# ADR 0006: DRY Runbook and Exit Criteria

## Context
- DRY runs must be reproducible, reviewable, and auditable.
- Manual steps and exit criteria should be centralized for stable review cadence.

## Decision
- Create a canonical RUNBOOK_DRY.md with stepwise flow and exit checklist.
- Add rehearsal helper script to print exact commands for human-in-the-loop runs.
- Add thresholds changelog generator from DIFF_TS files.

## Consequences
- Predictable PRs and stable review cadence.
- Less drift between mapping, adapter, and contracts.
- Clear audit trail for thresholds and DRY runs.
## Outcome
[TS_DECISION_20250919_SAMPLE.md](../DECISIONS/TS_DECISION_20250919_SAMPLE.md) documents the M1 decision.
