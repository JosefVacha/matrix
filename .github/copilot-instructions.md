# MATRIX - Repo-instructions for Copilot (PRIORITNE CTI PRED KAZDOU ODPOVED)

MANDATORY: Before any reasoning or edits, run `python3 scripts/qa/check_copilot_guardrails.py` and log:
Guardrail check: ran check_copilot_guardrails.py — PASS
Files reloaded: copilot-instructions.md, AGENTS.md, PROJECT_STATE.md

## Mission
Thin, modular layer on top of Freqtrade + FreqAI. Use Superalgos only as a mental map of nodes/edges. Phases = design + skeleton; no live keys or exchange execution.

## Role of the Copilot
- Follow official Freqtrade/FreqAI terminology and workflows (strategy I/O, feature engineering, train/inference, backtest).
- Before replying, always read this file + AGENTS.md (if present) + Knowledge/PROJECT_STATE.md.
- If you find a contradiction, propose an edit to those files; after approval, apply it.

## Pipeline (contracts map)
sensor(OHLCV) → feature(gen) → trainer(FreqAI) → server(FreqAI.predict) → strategy → risk → execution(Freqtrade)
 - I/O minimum:
  - OHLCV = DataFrame [date, open, high, low, close, volume], datetime index.
  - Features/labels time-aligned (no leakage), generated within FreqAI-compatible hooks.
  - Inference target: ~1s for TF 5m (informational only).
  - Backtest = static pairlist for reproducibility.

## Guardrails
- Use walk-forward split (train/test), labels with lookahead → no future information in training.
- Data hygiene: NaN policy, robust scaling (median/IQR), optional PCA (variance-based), outlier handling (IQR/IF).
- Do not modify base OHLCV columns; keep features in a clear namespace.
- Telemetry: log inference latency, %NaN per feature, feature drift, label hit-rate (proposal only).

## Workflow
1) For each reply, re-scan: .github/copilot-instructions.md → AGENTS.md → Knowledge/PROJECT_STATE.md.
2) If context is missing, write a proposal to Knowledge/RUNBOOK.md and request approval.
3) Maintain Knowledge/PROJECT_STATE.md (status, TODO, last change). Summarize what you just learned.
4) Never run anything with API keys or against live exchanges. Keep script suggestions safe and separated.

## Language & Terminology
-- **Default language for ALL repo artifacts = English**:
  - Filenames, code identifiers, comments, doc files, VS Code tasks, commit messages, PR titles
  - Use official Freqtrade/FreqAI terms; avoid mixed-language terminology
- **Czech allowed only in**: Knowledge/PROJECT_STATE.md (bilingual OK) and ad-hoc notes (README_cs.md optional)
- **If user asks in Czech, answer in Czech, but produce code/docs/commits in English**

## Links (term references)
- Freqtrade/FreqAI docs: https://www.freqtrade.io/
- Superalgos docs: https://superalgos.org/
