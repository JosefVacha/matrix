# MATRIX — Repo-instrukce pro Copilot (PRIORITNĚ ČTI PŘED KAŽDOU ODPOVĚDÍ)

## Mise
Tenká, modulární vrstva nad Freqtrade + FreqAI. Superalgos používáme jen jako mentální mapu uzlů (nodes/edges). Fáze = návrhová + skeleton; žádné live klíče ani exekuce na burzu.

## Role Copilota
- Drž se oficiální terminologie a workflow Freqtrade/FreqAI (strategie I/O, feature engineering, trén/inference, backtest).
- Před odpovědí vždy načti tento soubor + AGENTS.md (pokud existuje) + Knowledge/PROJECT_STATE.md.
- Když narazíš na rozpor, navrhni úpravu těchto souborů, po schválení je automaticky aktualizuj.

## Pipeline (kontraktová mapa)
sensor(OHLCV) → feature(gen) → trainer(FreqAI) → server(FreqAI.predict) → strategy → risk → execution(Freqtrade)
- I/O minimum:
  - OHLCV = DataFrame [date, open, high, low, close, volume], datetime index.
  - Features/labels zarovnané v čase (bez leakage), generované v rámci FreqAI-kompatibilních hooků.
  - Inference rozumná do ~1 s pro TF 5m (není tvrdý SLA, jen orientačně).
  - Backtest = statická pairlist pro reprodukovatelnost.

## Guardrails
- Walk-forward split (train/test), label s lookaheadem → žádné budoucí info v tréninku.
- Data hygiena: NaN policy, robustní škálování (median/IQR), volitelná PCA (variance-based), outliers (IQR/IF).
- Žádné úpravy základních OHLCV sloupců; featury drž v přehledném namespacu.
- Telemetrie: loguj latenci inference, %NaN po featurách, drift features, hit-rate labelu (jen návrh metrik).

## Workflow
1) Každou odpověď začni re-scanem: .github/copilot-instructions.md → AGENTS.md → Knowledge/PROJECT_STATE.md.
2) Když chybí kontext, zapiš návrh do Knowledge/RUNBOOK.md a vyžádej schválení.
3) Udržuj Knowledge/PROJECT_STATE.md (stav, TODO, poslední změna). Nezapomeň shrnout, co ses právě naučil.
4) Nikdy nespouštěj nic s API klíči/burzou. Návrhy ke skriptům dávej bezpečně a odděleně.

## Language & Terminology
- **Default language for ALL repo artifacts = English**:
  - Filenames, code identifiers, comments, doc files, VS Code tasks, commit messages, PR titles
  - Use official Freqtrade/FreqAI terms; avoid mixed-language terminology
- **Czech allowed only in**: Knowledge/PROJECT_STATE.md (bilingual OK) and ad-hoc notes (README_cs.md optional)
- **If user asks in Czech, answer in Czech, but produce code/docs/commits in English**

## Odkazy (pro orientaci v termínech)
- Freqtrade/FreqAI docs: https://www.freqtrade.io/
- Superalgos docs: https://superalgos.org/