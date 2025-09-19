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
