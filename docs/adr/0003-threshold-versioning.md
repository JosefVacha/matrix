# ADR 0003: Threshold Versioning

## Context
- Thresholds are critical for signal generation and risk management.
- Frequent changes require auditability and rollback.

## Decision
- All threshold sets are stored as TS_*.yml files in docs/thresholds/sets/.
- Diffs and rollback are supported via Markdown diff reports and versioned files.
- Validators ensure required fields and provenance.

## Consequences
- Threshold changes are fully auditable.
- Rollback to previous sets is trivial.
- Diff reports document rationale and impact.

## References
- scripts/thresholds/diff_thresholds.py
- docs/DIFF_REPORT_TEMPLATE.md
- docs/THRESHOLDS_SETS.md
