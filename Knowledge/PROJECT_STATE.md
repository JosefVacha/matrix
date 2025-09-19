# MATRIX - Project State

## Current Project Status / Aktuální stav projektu
**Last Updated / Datum poslední aktualizace:** 19 September 2025  
**Phase / Fáze:** First-Run Sandbox Preparation / Příprava první sandbox run  
**Status:** ✅ READY FOR FIRST OFFLINE RUN - Data placement docs + precheck + report template / Připraveno pro první offline run
**Last Updated / Datum poslední aktualizace:** 19 September 2025
**Phase / Fáze:** Churn & Stability Calculators, Summary/Merge Updates / Kalkulátory churn & stability, úpravy summary/merge
**Status:** 🟢 CHURN & STABILITY CALCULATORS INTEGRATED: SUMMARY now includes churn, merge tool prints JSON aggregates, echo tasks added / Kalkulátory churn & stability integrovány, SUMMARY nyní obsahuje churn, merge tool tiskne JSON agregáty, echo úlohy přidány

## Completed Tasks / Co bylo dokončeno
1. ✅ **Directory Structure / Adresářová struktura** - Created all required folders / Vytvořeny všechny potřebné složky (configs/, strategies/, scripts/, src/, tests/, Knowledge/, .vscode/, .github/)
2. ✅ **Basic Files / Základní soubory** - README.md, LICENSE (MIT), .gitignore, .copilotignore
3. ✅ **VS Code Settings / VS Code nastavení** - Enabled instruction file support / Zapnuta podpora pro instrukční soubory v .vscode/settings.json
4. ✅ **Copilot Instructions / Copilot instrukce** - Created .github/copilot-instructions.md with priority guidelines / Vytvořen s prioritními pokyny
5. ✅ **AGENTS.md** - Multi-agent rules definition (experimental) / Definice pravidel pro více agentů (experimentální)
6. ✅ **VS Code Tasks** - Basic skeleton tasks (download-data, backtest, hyperopt, UI, webserver, validate-contracts) / Základní skeleton úloh
7. ✅ **Knowledge Structure / Knowledge struktura** - PROJECT_STATE.md and RUNBOOK.md / PROJECT_STATE.md a RUNBOOK.md
8. ✅ **Python Skeleton Modules / Python skeleton moduly** - Complete src/matrix/ structure with type hints and contracts / Kompletní struktura s type hints a kontrakty
9. ✅ **Configuration Placeholders / Konfigurační placeholdery** - freqtrade.example.json a freqai.example.json (bez API klíčů)
10. ✅ **Test Skeletons / Test kostry** - test_contracts.py a test_walkforward.py s TODO strukturou
11. ✅ **I/O Contracts / I/O Kontrakty** - docs/CONTRACTS.md s MUST/SHOULD pravidly pro všechny moduly
12. ✅ **WFO Checklist** - docs/WFO_CHECKLIST.md pro walk-forward validaci
13. ✅ **Static Pairlist / Statická pairlist** - configs/pairlist.static.json pro reprodukovatelné BT
14. ✅ **Language Standardization / Jazyková standardizace** - English-first repository policy / Angličtina jako primární jazyk repozitáře
15. ✅ **FreqAI Hooks Skeleton / FreqAI hooks skeleton** - src/matrix/freqai/hooks.py with generate_features, generate_labels, feature_columns, label_name
16. ✅ **Bridge Integration / Integrace bridge** - Updated src/matrix/infra/freqai_bridge.py with prepare_training_data and prepare_inference_data
17. ✅ **Telemetry Sinks / Telemetrie** - Extended src/matrix/telemetry/metrics.py and created src/matrix/telemetry/logger.py
18. ✅ **Hook Config Placeholders / Hook config placeholdery** - Added commented hook references to configs/freqai.example.json
19. ✅ **Documentation Updates / Aktualizace dokumentace** - Added FreqAI Hooks Contract to docs/CONTRACTS.md and created docs/LABELS.md
20. ✅ **Sandbox Backtest Protocol / Sandbox backtest protokol** - docs/SANDBOX_BT.md with offline WFO blocks, static pairlist, report template
21. ✅ **Sandbox Config Template / Sandbox config template** - configs/backtest.sandbox.example.json with offline-only settings and placeholders  
22. ✅ **Threshold Optimization Methodology / Metodika optimalizace prahů** - docs/THRESHOLDS.md with 3-step process: Grid Sweep → WFO Evaluation → Stability Check
23. ✅ **Strategy Core Enhancement / Vylepšení strategy core** - Updated src/matrix/strategy/core.py with comprehensive threshold implementation TODOs
24. ✅ **Metrics Collection Framework / Framework pro sběr metrik** - docs/METRICS_CHECKLIST.md with 4-phase implementation priority (Data Quality → Signal Behavior → Performance → Risk → Advanced)
25. ✅ **Telemetry Metrics Implementation Plan / Plán implementace telemetrie** - Enhanced src/matrix/telemetry/metrics.py with TODO buckets for all METRICS_CHECKLIST.md phases
26. ✅ **FreqTrade Strategy Integration / Integrace FreqTrade strategie** - strategies/MatrixStrategy.py skeleton with MATRIX pipeline integration points
27. ✅ **Sandbox VS Code Tasks / Sandbox VS Code úlohy** - Added bt-sandbox-plan, thresholds-plan, metrics-first tasks for planning workflow
28. ✅ **Data Placement Documentation / Dokumentace umístění dat** - data/README.md with OHLCV file structure, naming conventions, validation checklist
29. ✅ **Pre-Run Validation Checklist / Kontrolní seznam před spuštěním** - docs/SANDBOX_PRECHECK.md with comprehensive verification boxes
30. ✅ **First-Run Report Template / Template pro první report** - docs/REPORT_TEMPLATE.md with structured sections for backtest analysis
30. ✅ **First-Run Report Template / Template pro první report** - docs/REPORT_TEMPLATE.md with structured sections for backtest analysis
31. 🟢 **Metrics Extraction Script / Skript pro extrakci metrik** - scripts/metrics/extract_metrics.py (stub, docstring, function signatures)
32. 🟢 **Metrics Summary Template / Template pro shrnutí metrik** - docs/METRICS_SUMMARY_TEMPLATE.md
33. 🟢 **Threshold Diff Script / Skript pro diff prahů** - scripts/thresholds/diff_thresholds.py (stub, docstring, function signatures)
34. 🟢 **Threshold Diff Template / Template pro diff report** - docs/DIFF_REPORT_TEMPLATE.md
35. 🟢 **Workflow Documentation Updates / Aktualizace workflow dokumentace** - METRICS_CHECKLIST.md and THRESHOLDS_SETS.md updated to link scripts/templates
36. 🟢 **VS Code Echo Tasks / VS Code echo úlohy** - Added metrics-summary and thresholds-diff skeleton tasks to .vscode/tasks.json

## Current Report Link / Aktuální link na report
**Current report → [docs/REPORT_TEMPLATE.md](docs/REPORT_TEMPLATE.md) (to be filled after first run)**
## Next Steps / Další kroky
1. Fill REPORT_1, generate SUMMARY_1; pick TS_*
2. Run offline 2, fill REPORT_2, SUMMARY_2
3. Compute churn + stability, update STABILITY_RECAP
4. DIFF_TS between sets if changed
5. Decide keep/iterate TS

## Key Components / Klíčové komponenty
- **Pipeline breathing:** sensor(OHLCV) → feature(hooks) → trainer(FreqAI) → predict(hooks) → strategy(thresholds) → risk → execution(Freqtrade)
- **Sandbox Framework:** Complete offline backtesting with WFO blocks, threshold optimization, metrics collection
- **Threshold Methodology:** Systematic 3-step optimization (Grid Sweep → WFO Evaluation → Stability Check) + data-driven extraction
- **Metrics Priority:** Phase-based implementation (Essential → Validation → Risk → Advanced)  
- **FreqAI Integration:** Hooks-based feature/label generation with temporal integrity / Integrace založená na hooks s časovou integritou
- **Security Guardrails:** No API keys, no live trading, skeleton-only commands / Žádné API klíče, žádné live trading
- **Compatibility:** Freqtrade/FreqAI workflow and terminology / Kompatibilita s workflow a terminologií
- **Inspiration:** Superalgos node concepts (mental map only) / Inspirace koncepty uzlů (jen mentální mapa)

## Sandbox Implementation Roadmap / Roadmapa implementace sandbox
### Phase 1: Essential Metrics (Data Quality + Signal Behavior)
- Implement data quality validation (missing data %, feature coverage, OHLCV gaps)
- Add signal behavior tracking (trigger rates, holding periods, oscillations)
- Create console summary and JSON export functions

### Phase 2: Threshold Implementation  
- Implement UP/DOWN thresholds with hysteresis in strategy/core.py
- Add cooldown logic for signal stability
- Integrate with MatrixStrategy.py for FreqTrade compatibility

### Phase 3: WFO Validation
- Create WFO block execution framework
- Implement threshold grid sweep methodology
- Add stability analysis across multiple blocks

### Phase 4: Performance & Risk Validation
- Add basic performance metrics (Sharpe, drawdown, win rate)
- Implement risk guards (VaR, position concentration, exposure)
- Create backtest report generation

## TODO - Next Steps / Další kroky
1. **Run First Tiny Offline Window** - Execute first sandbox run with minimal local data and fill REPORT_TEMPLATE.md including new Thresholds Extraction section / Spustit první sandbox run s minimálními místními daty
2. **Propose Concrete UP/DN/Hysteresis/Cooldown** - Use data from REPORT Thresholds Extraction and THRESHOLDS.md Decision Rules to propose specific threshold values in PR description / Navrhnout konkrétní hodnoty prahů pomocí dat z reportu
3. **Plan Second Sandbox Run** - Design validation run using proposed thresholds to test effectiveness / Naplánovat validační run s navrženými prahy
4. **Define Minimal Logger Outputs** - Specify what distribution stats and metrics to capture automatically in future runs / Definovat minimální výstupy logeru pro automatické zachycování statistik
5. **Outline Simple WFO Summary Table Format** - Create template for comparing results across repeated sandbox runs / Vytvořit template pro porovnání výsledků opakovaných sandbox runs

## Latest Changes / Poslední změny
- **19.9.2025:** Added threshold set versioning and STABILITY_SCORE.md documentation for second sandbox run / Přidáno verzování threshold setů a dokumentace stability score pro druhý sandbox run
- **19.9.2025:** Created THRESHOLDS_SETS.md and example TS_YYYYMMDD_TEMPLATE.yml for threshold set management / Vytvořen THRESHOLDS_SETS.md a příklad TS_YYYYMMDD_TEMPLATE.yml pro správu threshold setů
- **19.9.2025:** Added STABILITY_SCORE.md with qualitative scoring components / Přidán STABILITY_SCORE.md s kvalitativními komponentami skóre
- **19.9.2025:** Updated REPORT_TEMPLATE.md with Chosen Threshold Set and Stability Score sections / Aktualizován REPORT_TEMPLATE.md o sekce Chosen Threshold Set a Stability Score
- **19.9.2025:** Enhanced strategy/core.py with TODOs for threshold set injection and provenance / Vylepšen strategy/core.py o TODOs pro injekci threshold setu a provenance
- **19.9.2025:** Added VS Code echo tasks for threshold selection, second run, and report fill / Přidány VS Code echo úlohy pro výběr threshold setu, druhý run a vyplnění reportu
- **Learned / Naučeno:** Threshold set versioning, stability scoring, provenance documentation, manual config-to-code handoff / Verzování threshold setů, skórování stability, dokumentace provenance, ruční předání config-to-code

## TODO - Next Steps / Další kroky
1. **Pick TS_* Threshold Set** - Select threshold set file for second sandbox run and document provenance / Vybrat threshold set pro druhý sandbox run
2. **Run 2nd Sandbox** - Execute second offline run with selected thresholds and fill new report sections / Spustit druhý offline run s vybranými prahy
3. **Compare Metrics vs 1st Run** - Analyze stability, trigger rates, and performance changes / Porovnat metriky se 1. runem
4. **Record Qualitative Stability** - Score stability using STABILITY_SCORE.md components / Ohodnotit stabilitu pomocí komponent STABILITY_SCORE.md
5. **Plan Minimal Automation for Metrics Extraction** - Outline steps for automating metric extraction in future runs / Navrhnout kroky pro automatizaci extrakce metrik

## Notes for Future Work / Poznámky pro další práci
- Všechny příkazy zatím jako SKELETON (echo příkazy) pro bezpečnost
- Potřeba vytvořit skutečné konfigurační soubory až při rozšiřování funkcionalit
- Udržovat kompatibilitu s oficiální Freqtrade dokumentací