# Copilot TODOs — Source of Truth

## PHASE M2.2

- [✅] Create baseline models documentation
  - Status: docs/BASELINE_MODELS.md exists and is complete.
- [✅] Update training protocol documentation
  - Status: docs/TRAINING_PROTOCOL.md contains the Dataset builder CLI block.
- [✅] Formalize evaluation metrics documentation
  - Status: docs/EVAL_METRICS.md exists (stub or complete; update if missing).
- [✅] Add WFO metrics template
  - Status: docs/WFO_METRICS_TEMPLATE.md exists (stub created if missing).
- [✅] Document retrain cadence policy
  - Status: docs/RETRAIN_POLICY.md exists (stub created if missing).
- [✅] Implement H-consistency validator
  - Status: scripts/qa/check_H_consistency.py exists; CLI usage documented.

## PHASE M2.3

- [✅] Add dataset builder CLI to docs
  - Status: docs/TRAINING_PROTOCOL.md and docs/DATASET_SCHEMA.md updated.
- [✅] Add smoke test for builder
  - Status: tests/test_build_dataset.py exists and passes.
- [✅] Add echo tasks for builder
  - Status: .vscode/tasks.json updated with ds-build-plan and ds-build-smoke.

## PHASE M2.4

- [✅] Implement offline WFO evaluation runner
- [✅] Add WFO evaluation smoke test
- [✅] Update WFO metrics template with provenance note and JSON keys
- [✅] Add echo tasks for WFO planning and evaluation smoke


## PHASE M3.1

- [✅] Implement scripts/training/train_baseline.py (offline, takes dataset + label, outputs metrics JSON + models/<tag>/metadata.json; model.pkl ignored)
- [✅] Docs/TRAINING_PROTOCOL.md: add “Training Runner CLI” block + example

## PHASE M3.2

- [x] Complete scripts/registry/init_model_tag.py (idempotent) and scripts/qa/validate_model_metadata.py checks — idempotent init proven and metadata validated against schema; registry-check wired.
 - [x] Docs/MODEL_REGISTRY.md: schema link, CLI usage, example JSON present and referencing registry-check task

## PHASE M3.3

- [✅] Docs/RETRAIN_POLICY.md: wire cadence → validator inputs/outputs
- [✅] scripts/qa/check_retrain_cadence.py (stub; exit 0/1); add echo task

## PHASE M3.4

- [✅] CI: GitHub Actions workflow (.github/workflows/smoke-validators.yml) for validators + optional smoke

- [ ] H-consistency integration: ensure usage in EVAL_METRICS.md and WFO provenance; add echo task

## Guardrail enforcement

- [x] Add a pre-edit guardrail check: run `python3 scripts/qa/check_copilot_guardrails.py` to verify `AGENTS.md` and `.github/copilot-instructions.md` are present and readable. This check must be run before making edits that change repo guardrails.
