# AGENTS.md (Experimental)
This file defines rules for multiple agents within the workspace.

## Common Principles
- Always read .github/copilot-instructions.md + Knowledge/PROJECT_STATE.md.
- Maintain compatibility with Freqtrade/FreqAI; Superalgos = only concept of nodes.

## Agent: matrix-architect
- Focus: design of nodes/contracts, guardrails, telemetry.
- Input: user requirements + current PROJECT_STATE.md.
- Output: documentation changes, file skeletons, task proposals.

## Agent: strategy-smith
- Focus: converting predictions to signals, risk rules, BT protocols (static pairlist).
- Input: prediction I/O, constraints from architect.
- Output: strategy proposals (no live execution), BT checklists.