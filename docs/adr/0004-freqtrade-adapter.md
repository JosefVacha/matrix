# ADR 0004: Freqtrade Adapter Layer

## Context
- Keep core mapping framework-agnostic (no vendor lock)
- Use a thin adapter to convert predictions to Freqtrade signal columns
- Thresholds injected from TS files (see THRESHOLDS_SETS.md)

## Decision
- Adapter layer wraps mapping logic and produces Freqtrade-compatible signal columns
- Thresholds loaded from static YAML files
- All logic is offline, reproducible, and audit-friendly

## Consequences
- Clearer tests and contract boundaries
- Easier rollback/change of thresholds
- No vendor lock-in; mapping remains framework-agnostic
