# ADR 0001: Language Policy

## Context
- MATRIX is a collaborative project with contributors fluent in English and Czech.
- Code, docs, and config files must be clear, maintainable, and compatible with Freqtrade/FreqAI.

## Decision
- All repo artifacts (code, docs, filenames, commit messages) use English by default.
- Czech is allowed only in Knowledge/PROJECT_STATE.md and ad-hoc notes.
- Mapping function and simulator docstrings are English-only.

## Consequences
- Ensures compatibility with upstream projects and global contributors.
- Reduces translation/maintenance overhead.
- Knowledge files remain bilingual for local context.

## References
- .github/copilot-instructions.md
- Freqtrade/FreqAI docs
