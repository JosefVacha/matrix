# MATRIX Coding Standards

## Typing
- Use explicit type hints for all functions and public variables
- Prefer Python 3.10+ type syntax

## Module Layout
- One module per logical function (strategy, telemetry, etc.)
- Keep mapping and simulator logic framework-agnostic

## Docstrings
- All public functions/classes must have docstrings (EN only)
- Document behavior, inputs, outputs, edge cases

## Error Handling
- Use stdlib only for all tools/scripts
- Handle missing/invalid data gracefully (exit code 1, clear message)
