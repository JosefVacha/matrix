# MATRIX Model Registry

## Layout
- models/<model_tag>/model.pkl (placeholder; not committed)
- models/<model_tag>/metadata.json (tracked; small)
- models/.keep (git)

## Metadata Fields
- created_at
- author
- commit
- timeframe
- pairlist_ref
- label: {mode, H, transform}
- features: {windows, prefix}
- model: {type, params}
- training_ranges: [...]
- evaluation: {metrics_summary}
- notes
- SHA256 of artifact (if available)

## Notes
- model.pkl is gitignored; only metadata.json and SHA256 are tracked
- See docs/MODEL_REGISTRY.md for naming, update, deprecation
