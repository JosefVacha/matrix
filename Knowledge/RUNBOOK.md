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