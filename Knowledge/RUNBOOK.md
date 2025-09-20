# MATRIX - RUNBOOK

## Denní ritus práce s Copilotem

### Před každou odpovědí Copilot musí:
1. **Načíst prioritní instrukce** z `.github/copilot-instructions.md`
2. **Zkontrolovat AGENTS.md** (pokud existuje) pro kontextové pravidla
3. **Přečíst aktuální stav** z `Knowledge/PROJECT_STATE.md`
4. **Identifikovat případné rozpory** mezi realitou a instrukcemi

### Jak požádat Copilota o pomoc:
- **Buď konkrétní** v požadavcích (používej Freqtrade/FreqAI terminologii)
- **Uveď kontext** - na čem pracuješ, co chceš dosáhnout
- **Specifikuj bezpečnost** - vždy pripomeň "žádné API klíče, žádné live trading"
- **Požádej o validaci** - nech si vysvětlit, co Copilot pochopil z instrukcí

### Automatické kontroly Copilota:
- ✅ **Bezpečnost:** Žádné produkční API klíče nebo live trading
- ✅ **Terminologie:** Kompatibilita s oficiální Freqtrade/FreqAI dokumentací
- ✅ **Pipeline:** Dodržování definované kontraktové mapy
- ✅ **Data hygiena:** Walk-forward split, žádný temporal leakage
- ✅ **Dokumentace:** Aktualizace PROJECT_STATE.md při změnách

### Reportování změn:
Copilot při každé změně updatuje:
1. **PROJECT_STATE.md** - shrnutí nového stavu a naučené poznatky
2. **Instrukční soubory** - při zjištění nesouladu (po schválení)
3. **TODO sekci** - aktualizace dalších kroků

### Když něco není jasné:
1. Copilot **navrhne řešení** a zapíše ho do RUNBOOK.md
2. **Vyžádá si schválení** před implementací
3. **Dokumentuje rozhodnutí** pro budoucí referenci

### Pracovní konvence:
- **Statická pairlist** pro reprodukovatelné backtesty
- **Skeleton příkazy** pro bezpečnost (echo místo skutečných příkazů)
- **Docs-first přístup** - vždy odkazuj na oficiální dokumentaci
- **Modulární design** - každý komponent s jasným I/O kontraktem

### Escalace problémů:
Pokud Copilot narazí na:
- **Nekompatibilitu** s Freqtrade/FreqAI → navrhne změnu instrukcí
- **Bezpečnostní riziko** → okamžitě zastaví a upozorní
- **Chybějící kontext** → požádá o doplnění informací
- **Rozpor v požadavcích** → vyžádá si clarifikaci

## Vzorové dotazy pro Copilota:

### ✅ Dobré dotazy:
- "Vytvoř FreqAI-kompatibilní feature engineering modul pro technické indikátory"
- "Navrhni BacktestEngine s walk-forward validací pro Matrix pipeline"
- "Implementuj telemetrii pro sledování inference latence"

### ❌ Špatné dotazy:
- "Spusť live trading na Binance" (bezpečnostní riziko)
- "Změň OHLCV sloupce" (porušuje guardrails)
- "Použij budoucí data pro trénink" (temporal leakage)

## Baseline & Notifier Playbook

This section documents the safe, reviewable process for updating performance baselines and enabling remote notifications from CI.

1) Local verification
- Run the smoke simulator locally and extract metrics:

```bash
python3 scripts/trading/paper_trading_sim.py --dataset data/dataset_SMOKE.parquet --output outputs/paper_trade_report.json
python3 scripts/qa/extract_paper_trade_metrics.py --input outputs/paper_trade_report.json --output outputs/paper_trade_metrics.json
```

- Compare to existing baseline (example):

```bash
python3 scripts/qa/compare_metrics_to_baseline.py --metrics '{"final_net": 0.05, "max_drawdown": 0.10}'
```

2) Propose baseline update (manual PR)
- If metrics improve or a new metric (e.g. `max_drawdown`) is available, prepare a PR in which:
  - `ci/baselines/paper_trade_metrics_baseline.json` is updated with the proposed values.
  - The PR description includes: run command used, environment (python/pandas versions), and a short explanation for the change.
- Include maintainers as reviewers and wait for at least one approval before merging.

3) Enabling remote notifications (safe pattern)
- Always perform at least one manual verification run (dry-run) and inspect artifacts before enabling automation.
- To enable notifications for a single run (manual):
  - Use the workflow dispatch input `allow_notifications=true` when running `ci_paper_trade_smoke.yml` or `simulate-notifier-dispatch.yml`.
  - Ensure `ALLOW_NOTIFICATIONS` repository secret is set to `1` (see below).
- To enable repo-wide automation:
  - Add repository secret `ALLOW_NOTIFICATIONS` with value `1` in Settings → Secrets.
  - Ensure `SLACK_WEBHOOK` and/or a bot `GITHUB_TOKEN` are present and scoped minimally.
  - Do NOT merge a change that removes `--dry-run` until the manual verification is approved.

4) Rollback & audit
- To disable notifier automation immediately, set `ALLOW_NOTIFICATIONS` to `0` or delete the secret.
- Audit created issues/PRs and check the GitHub Actions logs for token usage.

Checklist before merging any automation changes
- [ ] At least one dry-run verification completed and reviewed
- [ ] Baseline tolerances documented and agreed
- [ ] Secrets reviewed and scoped (ALLOW_NOTIFICATIONS, SLACK_WEBHOOK)
- [ ] Workflow inputs configured so remote actions remain opt-in per dispatch

End of playbook