# ADR 0007: FreqAI Features and Labels

## Context
- Moving from stubs to minimal, testable semantics for features and labels.
- Need a single source of truth for feature/label generation and contracts.

## Decision
- All feature/label logic centralized in `matrix.freqai.hooks.generate_features` and `generate_labels`.
- Adapter and training protocol use outputs from hooks; contracts documented in docs.

## Consequences
- Hooks own the data contracts; adapter and training protocol reference them.
- Training protocol documents walk-forward evaluation and reproducibility.
- Enables offline, reproducible, audit-friendly model development.
