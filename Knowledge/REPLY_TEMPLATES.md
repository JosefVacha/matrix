# REPLY TEMPLATES (CZ)

Tento dokument obsahuje oficiální šablonu pro odpovědi, které generuje Copilot‑style agent v tomto repozitáři. Vše je v češtině a psáno velmi jednoduše, krok za krokem. Používejte tuto šablonu při popisu změn, výsledků testů, návrhů dalších kroků a doporučení.

POVINNÉ: Před každou odpovědí spusťte `python3 scripts/qa/check_copilot_guardrails.py` a začněte odpověď přesnou auditní preface, kterou skript vyžaduje (viz .github/copilot-instructions.md). Tato preface musí být první dvě řádky odpovědi.

MANDATORY: Pokud uživatel píše v češtině, odpověz v češtině.

----

ŠABLONA ODPOVĚDI (používejte přesně tento formát)

1) Nadpis (1 věta)
- Co jsem udělal: <jedna věta, např. "Vygeneroval jsem SMOKE dataset a spustil lokální testy">.

2) Stručně, krok za krokem (velmi prostě)
- 1) <první krok>
- 2) <druhý krok>
- 3) <výsledek>

3) Kde je systém (artefakty)
- `dataset`: <cesta nebo "none">
- `trainer`: <cesta>
- `model_metadata`: <cesta nebo "none">
- `tests_run`: <seznam nebo "none">
- `env`: <volitelné; např. `/.venv` Python X.Y.Z>

4) Stav vs. guardrails (strojově čitelná sekce — přesné klíče)
- `guardrails_preface`: PASS|FAIL
- `tests`: PASS|FAIL (passed/total)
- `ci_ready`: true|false
- `roadmap_phase`: <např. M3.2>
- `notes`: <krátký text nebo "none">

5) Proběhlo podle podmínek systému?
- Yes/No — <krátký důvod>

6) Doporučení — tři možnosti (každá 1 věta + odhad práce)
- Volba A — <krátký návrh> (rychlé, nízké riziko)
- Volba B — <krátký návrh> (střední práce)
- Volba C — <krátký návrh> (větší změna)

7) Doporučená volba: <A|B|C> — krátký důvod

8) Pokud vybráno (quick checklist)
- 1) <krok 1>
- 2) <krok 2>
- 3) <krok 3>

9) Bezpečnostní poznámka
- <např. "Nezveřejňovat API klíče. Vše probíhat offline.">

10) (Volitelně) Machine digest (jednořádkové JSON) — použijte pouze pokud požadováno
- `{"guardrails_preface":"PASS","tests":"PASS(47/47)","ci_ready":false,"recommended":"A"}`

----

PŘÍKLAD (vyplněný)

- Nadpis: Vygeneroval jsem SMOKE dataset a spustil lokální testy.
- Stručně: 1) Spustil jsem `scripts/qa/generate_smoke_dataset.py` → `data/dataset_SMOKE.pkl`. 2) Spustil jsem `pytest` → všechny testy prošly. 3) Výstup: `outputs/smoke_summary.json`.
- Kde je systém:
  - `dataset`: `data/dataset_SMOKE.pkl`
  - `trainer`: `scripts/training/train_baseline.py`
  - `model_metadata`: `models/LOCAL_SMOKE/metadata.json`
  - `tests_run`: `tests/test_train_baseline_unit.py`, `tests/test_validators.py`
  - `env`: `/.venv` (Python 3.12.3)
- Stav vs. guardrails:
  - `guardrails_preface`: PASS
  - `tests`: PASS(47/47)
  - `ci_ready`: false
  - `roadmap_phase`: M3.2
  - `notes`: `fastparquet pinned; generator has stdlib fallback`
- Proběhlo podle podmínek systému? Yes — preface ok; testy OK; CI needs small tweak.
- Doporučení:
  - Volba A — (DOPORUČENO) Přidat pip install v CI validators job (rychlé)
  - Volba B — Rozšířit unit testy (střední práce)
  - Volba C — Nasadit pre-commit + Makefile (větší práce)
- Doporučená volba: A — rychlé a sníží chybovost v CI.
- Quick checklist:
  1) Upravit `.github/workflows/smoke-validators.yml` a přidat pip install -r requirements-dev.txt před testem.
  2) Spustit validators job na PR.
  3) Opravit případné chyby.
- Bezpečnost: nerozdávat žádné klíče nebo secrety; vše offline.

----

USAGE NOTES
- Upravuj tento soubor v PR; pokud chceš změnit strukturu, aktualizuj i `copilot-instructions.md` a `Knowledge/PROJECT_STATE.md`.
- Doporučuji zachovat pole ve `Stav vs. guardrails` pro lepší parsování a přehlednost.
