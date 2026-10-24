# Not Cleaner Yet — Air quality in France, 2024–2026

**Streamlit data-storytelling dashboard** · EFREI Paris · Individual Student Project 2026 · Group BIO
**Author:** BIAO Ashley · Ing2-BIO · ashley.biao@efrei.net · [LinkedIn](https://www.linkedin.com/in/ashley-djeehad-biao-76b720330/)
**Course:** Data Visualization · **Project proposed by:** Prof. Mano Mathew (mano.mathew@efrei.fr)

**Deployed app:** https://air-quality-france-biao.streamlit.app/ · **Code:** https://github.com/djeehad/air-quality-france · **Storyboard:** [docs/STORYBOARD.md](docs/STORYBOARD.md) · 

---

## 1. The question
Santé publique France attributes about 40,000 deaths a year to fine particles and about 7,000 to NO₂
(estimates published in 2021). **Is the air we breathe in France getting cleaner — and where and when is it worst?**

**Audience:** citizens, students and local decision-makers.

**Questions answered**
1. How have the four main pollutants evolved since 2024?
2. When is the air worst (season, station type)?
3. Where is exposure highest (zones, map, mainland vs overseas)?
4. How often are WHO 2021 health guidelines exceeded?

## 2. Key findings
| # | Finding |
|---|---------|
| 1 | **Not cleaner:** January–October 2026 vs 2024, NO₂ +5 %, O₃ +11 %, PM2.5 +14 %, PM10 +16 % (robust on stations present all three years). |
| 2 | **Traffic drives NO₂:** 21 vs 10 µg/m³ at background stations; WHO guideline exceeded on 32 % vs 5 % of sampled days (~6×). |
| 3 | **Seasons:** NO₂ and particles peak in winter (17 Feb 2025: 84 % of PM2.5 stations above WHO); ozone peaks in summer, days above WHO 0.6 % → 4.2 %. |
| 4 | **Fine particles reach everyone:** even background stations exceed the PM2.5 guideline ~9 % of days. |
| 5 | **Geography:** NO₂ highest in large southern/eastern cities, O₃ in Corsica & Provence, PM10 overseas (natural dust, sea salt). |

## 3. Data
| | |
|---|---|
| Dataset | Données « temps réel » de mesure des concentrations de polluants atmosphériques réglementés |
| Producer | LCSQA — Laboratoire Central de Surveillance de la Qualité de l'Air (Geod'air database) |
| Portal | data.gouv.fr — https://www.data.gouv.fr/datasets/5b98b648634f415309d52a50 |
| Files | One CSV per day: `https://files.data.gouv.fr/ineris/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/<year>/FR_E2_<date>.csv` |
| Stations | Metadata "D" file (.xls, sheet `AirQualityStations`) on the same page → coordinates |
| License | Licence Ouverte / Open Licence 2.0 (Etalab) — free reuse with attribution |
| Used here | 2024-01-01 → 2026-10-19, one day per week (147 days), 523 stations, 71 zones, 181,169 station-day rows |

Processed files shipped in the repo (so the app starts instantly and deploys without re-downloading):
`data/processed/daily.parquet` (~0.9 MB) and `data/stations.csv`.

## 4. Run it
```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the data from scratch (optional):
```bash
python scripts/download_data.py --start 2024-01-01 --every 7     # ~15–30 min, one day per week
python scripts/build_stations.py path/to/fr-2026-d-xxxxxxxx.xls  # station coordinates
```
Without `data/processed/daily.parquet` the app runs on a clearly labelled synthetic demo sample.

## 5. Methods
- **Cleaning:** hours with `validité = -1` dropped (validated `1` and not-yet-validated `4` kept); daily mean kept only
  with ≥ 18 valid hours (EU 75 % rule); negative values → missing; duplicates on (date, station, pollutant) removed.
- **Feature engineering:** year, month, season, WHO threshold, `above_who` flag, `overseas` flag (station outside
  the mainland bounding box).
- **Fair comparisons:** year-on-year indicators use only the months present in the last year (Jan–Oct), so a missing
  winter does not bias the change.
- **Thresholds:** WHO 2021 24-hour guidelines — NO₂ 25, PM10 45, PM2.5 15 µg/m³; O₃ 100 µg/m³ (an 8-hour value,
  applied to daily means → ozone exceedances under-estimated).
- **Data quality section in the app:** row counts, duplicates, negative values, short days, missingness by column and pollutant.

## 6. Limitations
Real-time data are not yet validated · three years is short and weather drives pollution, so part of the rise may be
meteorological · stations are placed near hotspots, so averages describe monitored places, not population exposure ·
weekly sampling can miss short episodes · correlations only, no causal claim.

## 7. Project structure
```
app.py                     page config, cached loading, sidebar filters, section order
sections/header.py         student / course block (logo + details)
sections/overview.py       KPI row, hook, section 1 (when is the air worst?)
sections/deep_dives.py     section 2: map, zone ranking, seasonal small multiples
sections/quality.py        section 3: data quality checks & limitations
sections/conclusions.py    section 4: insights & next steps
utils/constants.py         every assumption: URLs, column map, thresholds, author details
utils/io.py                load processed data (+ station coordinates) or demo data
utils/prep.py              quality report, cleaning, features, filters, KPIs, aggregations
utils/viz.py               Plotly charts with one consistent, colour-blind-safe style
utils/i18n.py              English / French texts
scripts/download_data.py   download + reduce daily CSV files → data/processed/daily.parquet
scripts/build_stations.py  station metadata .xls → data/stations.csv
docs/                      storyboard, video script & explanation
```

## 8. Rubric checklist
Sidebar filters (pollutant, years, territory, zone, station type, language) · KPI row tied to filters ·
3+ interactive Plotly visuals with tooltips (line, map, bar ranking, small multiples) · map with real coordinates ·
data quality section · `st.cache_data` on loading and filtering · pre-aggregated parquet · alt text on every chart ·
colour-blind-safe palette, labelled axes and units · pinned `requirements.txt`.
