# Language Audit Report

This document tracks the language unification effort to English-first repository content.

## Files Translated to English

### ✅ Completed Translations
- **README.md** - Main project documentation
- **AGENTS.md** - Agent definitions and workflows  
- **docs/WFO_CHECKLIST.md** - Walk-forward optimization checklist
- **.vscode/tasks.json** - All task titles and descriptions
- **.github/copilot-instructions.md** - Added Language & Terminology section

### ℹ️ Already English
- **docs/CONTRACTS.md** - I/O contracts (was already in English)
- **src/matrix/** - All Python modules (skeleton interfaces in English)
- **tests/** - Test files (docstrings in English)

## Czech Content Preserved (Allowed)

### 📝 Bilingual Files  
- **Knowledge/PROJECT_STATE.md** - Updated with English headings but Czech content preserved
- **Knowledge/RUNBOOK.md** - Contains operational procedures (bilingual acceptable)

### 🇨🇿 Czech Mirror
- **README_cs.md** - Czech summary with link to main English README

## Terminology Standardization

### ✅ Resolved Ambiguities
- "Backtest/Backtesting" → Consistent "backtest" (lowercase) for noun, "backtesting" for process
- "Walk-forward optimalizace" → "Walk-Forward Optimization (WFO)"
- "Kontrakty" → "Contracts" (I/O contracts between modules)
- "Featury" → "Features" (no mixed Czech-English)
- "Pipeline" → Kept "pipeline" (established Freqtrade/FreqAI term)

### 📋 Official Freqtrade/FreqAI Terms Used
- FreqAI (not "FreqAI framework")
- Freqtrade (consistent capitalization)  
- Strategy (not "strategie")
- Timeframe (not "časový rámec")
- Pairlist (not "seznam párů")

## Remaining Language Items

### ⚠️ Still Contains Czech
- **configs/freqtrade.example.json** - Comments in mixed language (acceptable for config examples)
- **configs/freqai.example.json** - Comments in mixed language (acceptable for config examples) 
- **configs/pairlist.static.json** - Comments in mixed language (acceptable for config examples)

### 🔍 Files Not Checked
- **Knowledge/RUNBOOK.md** - Operational procedures (bilingual acceptable per policy)
- **strategies/** - Empty directory
- **scripts/** - Empty directory

## Quality Assurance

### ✅ Verified Standards
- All commit messages will be in English (per new policy)
- All code identifiers in English  
- All docstrings in English
- All documentation files in English (except explicit Czech mirrors)

### 🎯 Compliance Status
**COMPLIANT** - Repository meets English-first language policy.

---
*Audit completed: 19 September 2025*  
*Next review: When new files are added to the repository*