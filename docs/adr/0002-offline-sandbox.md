# ADR 0002: Offline Sandbox & WFO

## Context
- Live trading and data downloads are risky and non-reproducible in early development.
- Walk-forward optimization (WFO) requires deterministic, static datasets.

## Decision
- All MATRIX workflows run strictly offline in the sandbox phase.
- No API keys, no live exchange connections, no downloads.
- WFO splits and threshold selection are performed on static, versioned data.

## Consequences
- Enables reproducible, auditable experiments.
- Reduces risk of accidental live trading.
- Facilitates robust threshold versioning and rollback.

## References
- docs/THRESHOLDS_SETS.md
- docs/SANDBOX_BT.md
