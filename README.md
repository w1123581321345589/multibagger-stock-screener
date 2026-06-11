# Multibagger Stock Screener

A stock screener built around two specific investment frameworks: the Yartseva (2025) multibagger research and the Compounding Quality methodology.

![Screener Dashboard](screenshots/screener-loaded.jpg)

---

## What it does

Pick a mode, set your filters, and it pulls live data from Yahoo Finance and scores every stock in the universe across 7 weighted factors. Bonus quality indicators add or subtract points on top. The output is a ranked list with a composite score, classification, and full factor breakdown.

**Multibagger Hunter** — targets 10x+ potential. Looks for small-cap, beaten-down, cash-generating companies trading below book value. Based on Yartseva's quantitative research.

**Quality Compounder** — targets consistent 15%+ CAGR. Looks for wide-moat businesses with owner-operators, high FCF conversion, and buyback programs.

---

## Scoring

### Core factors (Yartseva weights)

| Factor | Weight | What it checks |
|--------|--------|----------------|
| FCF Yield | 20% | Free cash flow relative to market cap |
| Book-to-Market | 15% | How undervalued vs book value |
| Entry Point | 14% | Distance from 52-week low (contrarian) |
| Size | 12% | Smaller = more room to run |
| Profitability | 12% | EBITDA margin + ROA |
| Investment Pattern | 12% | Is growth funded by EBITDA or debt? |
| Macro | 10% | Rate environment |

### Quality bonuses (Compounding Quality)

| Signal | Points |
|--------|--------|
| High FCF conversion | +8 / -8 |
| Strong FCF margin | +5 |
| Insider ownership | +8 (founder bonus +5) |
| Share buybacks | +6 / -6 |
| Moat (ROIC > 15% + GM > 40%) | +6 |

---

## Stack

- **Backend** — Python, FastAPI, yfinance
- **Frontend** — React, Vite, Tailwind CSS
- **Data** — Yahoo Finance (live), Financial Modeling Prep (universe expansion)

---

## Setup

```bash
# Backend
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
cd frontend
npm install
npm run dev
```

Optional: add a `FMP_API_KEY` environment variable to unlock the expanded stock universe (small-cap and mid-cap screening via FMP's free API).

---

## API

```
GET /api/screen?mode=multibagger&universe=small_cap&min_score=50
GET /api/stock/{ticker}?mode=compounder
GET /api/macro
GET /api/universe?source=small_cap
```

`mode` — `multibagger` or `compounder`  
`universe` — `default`, `small_cap`, `mid_cap`, or `expanded`  

---

## Screenshots

![Stock Cards](screenshots/screener-cards.jpg)

---

## Changelog

**v2** — Dual-mode screening, 5 bonus quality factors, expanded stock universe with FMP integration  
**v1** — Initial build, 7-factor Yartseva scoring, yfinance data
