# ADR 0005: Ingest Freqtrade Output

## Context
- Manual transcription of backtest results is error-prone and slow.
- Need unified, reproducible metrics view for audit trail.

## Decision
- Implement stdlib-only ingestor for JSON/CSV/txt Freqtrade outputs.
- Write/append machine markers to REPORT; render SUMMARY; merge to recap.

## Consequences
- Reproducible audit trail; tolerant to partial data.
- Faster, less error-prone reporting.
