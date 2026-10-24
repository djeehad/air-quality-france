# Storyboard — *Not Cleaner Yet: Traffic in Winter, Ozone in Summer*

**Author:** BIAO Ashley · Ing2-BIO · EFREI Paris · Data Visualization — project proposed by Prof. Mano Mathew
**App:** https://air-quality-france-biao.streamlit.app/ · **Code:** https://github.com/djeehad/air-quality-france

---

## 1. Framing

| | |
|---|---|
| **Problem** | Air pollution is a major health risk: Santé publique France attributes ~40,000 deaths a year to PM2.5 and ~7,000 to NO₂ (estimates published in 2021). Public debate assumes the air is improving. |
| **Main question** | Is the air we breathe in France getting cleaner — and when and where is it worst? |
| **Audience** | Citizens, students and local decision-makers. No technical background assumed: every term is explained in tooltips. |
| **Data** | LCSQA real-time hourly measurements (data.gouv.fr, Licence Ouverte 2.0), one day per week, Jan 2024 → Oct 2026: 147 days, 523 stations, 71 zones. Station coordinates from the LCSQA metadata file. |
| **Narrative pattern** | Change over time (before/after) + compare groups and regions (map, ranking, small multiples). |
| **Benchmark** | WHO 2021 24-hour guidelines: NO₂ 25 · PM10 45 · PM2.5 15 · O₃ 100 µg/m³. |

### Sub-questions → answers (the takeaways)
| # | Question | Takeaway |
|---|---|---|
| Q1 | Is it improving? | **No.** Jan–Oct 2026 vs 2024: NO₂ +5 %, O₃ +11 %, PM2.5 +14 %, PM10 +16 %. |
| Q2 | When is it worst? | **Traffic + winter** for NO₂ and particles; **summer** for ozone. |
| Q3 | Where is it worst? | Depends on the pollutant: NO₂ in large cities, O₃ in Corsica, PM10 overseas. |
| Q4 | How often is health at risk? | Traffic stations exceed the NO₂ guideline on 32 % of days vs 5 % for background. |

---

## 2. Story arc

```
 HOOK ──────────► CONTEXT ──────────► INSIGHTS ─────────────────────► IMPLICATIONS
 40,000 deaths    Who measures,       1. Not cleaner (all 4 up)        Traffic measures (ZFE),
 a year — is it   what, how; WHO      2. When: traffic, winter/summer  seasonal alerts,
 getting better?  thresholds          3. Where: map & ranking          add weather data
                                      + honesty: quality & limits
```

---

## 3. Page layout (wireframe)

```
┌──────────────┬───────────────────────────────────────────────────────────┐
│ SIDEBAR      │ [EFREI logo]  Name · Program · Year · LinkedIn · GitHub   │
│              │               Course · Project proposed by                │
│ Language     ├───────────────────────────────────────────────────────────┤
│ EN / FR      │ TITLE: Not Cleaner Yet: Traffic in Winter, Ozone in Summer│
│              │ Source · Your selection                                   │
│ Pollutant    │ [KPI mean] [KPI % days > WHO] [KPI most exposed zone]     │
│ Years slider ├───────────────────────────────────────────────────────────┤
│ Territory    │ HOOK text + audience    [NO2 +5%][O3 +11%][PM2.5][PM10]   │
│ Zone         ├───────────────────────────────────────────────────────────┤
│ Station type │ 1. When is the air worst?   Headline (computed)           │
│              │    [monthly line chart by station type + WHO line]        │
│ About the    ├───────────────────────────────────────────────────────────┤
│ data         │ 2. Where is exposure highest?   Headline (computed)       │
│              │    tabs: [Map] [Zone ranking] [Seasons small multiples]   │
│              ├───────────────────────────────────────────────────────────┤
│              │ 3. Data quality & limitations  (counters, tables, notes)  │
│              ├───────────────────────────────────────────────────────────┤
│              │ 4. Key insights & next steps                              │
└──────────────┴───────────────────────────────────────────────────────────┘
```

---

## 4. Scene by scene

### Scene 0 — Header & title
| | |
|---|---|
| **Purpose** | Identify author and course; state the answer immediately. |
| **Content** | Student/course block; headline title; source line; "Your selection" recap. |
| **Takeaway** | The title *is* the conclusion: the air is not cleaner yet. |

### Scene 1 — KPIs (react to filters)
| | |
|---|---|
| **Question** | What does my selection look like right now? |
| **Visual** | 3 metric tiles: mean concentration (last year, same months), % station-days above WHO, most exposed zone — each with change vs first year. |
| **Interaction** | Every sidebar filter updates them. Red delta = worse. |
| **Design choice** | Comparison restricted to the same months (Jan–Oct) so the missing 2026 winter does not bias the result. |

### Scene 2 — Hook
| | |
|---|---|
| **Question** | Why should I care, and is it improving? |
| **Visual** | Short text with the health figure + 4 tiles: change of each pollutant 2024 → 2026. |
| **Takeaway** | All four pollutants went up. |
| **Transition** | "So when is the air at its worst?" |

### Scene 3 — Section 1: When is the air worst?
| | |
|---|---|
| **Question** | Which situations and seasons are most harmful? |
| **Visual** | Line chart: monthly mean by station type (traffic / background / industrial), dashed WHO reference line with label. |
| **Why this chart** | Time on the x-axis shows seasonality; one line per station type shows the traffic gap; the threshold line turns values into health meaning. |
| **Interaction** | Hover for exact values; click legend to hide a series; change pollutant. |
| **Computed headline** | e.g. NO₂: traffic 21.3 vs background 10.3 µg/m³; WHO exceeded 32 % vs 5 % of days. O₃: peaks in summer (67 vs 44 µg/m³ in winter). |
| **Transition** | "When is clear — now, where?" |

### Scene 4 — Section 2: Where is exposure highest?
| | |
|---|---|
| **Question** | Which places are most exposed? |
| **Visual A — Map** | One dot per station; colour = mean concentration (sequential yellow→red), size = days above WHO. |
| **Visual B — Ranking** | Horizontal bars: 15 most exposed zones, coloured by % days above WHO (top/bottom-N pattern). |
| **Visual C — Small multiples** | Seasonal profile of the 6 most exposed zones, same y-axis to compare. |
| **Interaction** | Tabs; zoom/hover map; Territory filter (mainland / overseas); zone and station-type filters. |
| **Computed headline** | Most exposed zone and its share of days above WHO, e.g. ZAR Perpignan for NO₂, ZR Corse for O₃, ZR Mayotte for PM10. |
| **Transition** | "Can we trust these numbers?" |

### Scene 5 — Section 3: Data quality & limitations
| | |
|---|---|
| **Purpose** | Transparency (rubric: data work + communication). |
| **Content** | Counters: 181,169 rows, 0 duplicates, 136 negative values set to missing, 3,780 days with < 18 valid hours removed; missingness by column and pollutant (~2 %); processing steps; limitations. |
| **Key caveats** | Unvalidated real-time data; 3 years is short and weather matters; stations sit near hotspots; weekly sampling; O₃ guideline is 8-hour; no causal claim. |

### Scene 6 — Section 4: Insights & next steps
| | |
|---|---|
| **Content** | 5 insights (not cleaner; traffic & NO₂; seasons; PM2.5 everywhere; geography by pollutant) + implications. |
| **Implications** | Traffic measures (low-emission zones) target the clearest problem; winter heating and summer ozone alerts; next: add Météo-France data, use validated annual data, extend the period. |

---

## 5. Visual design rules
- **Colour:** Okabe-Ito categorical palette (colour-blind safe); sequential palettes for magnitudes (yellow→red on the map, oranges on the ranking).
- **Annotation:** WHO reference line labelled on the chart; units (µg/m³) on every axis.
- **Accessibility:** alt text under every chart; tooltips explain every term; EN/FR switch.
- **Honesty:** bar charts start at zero; comparisons on equal periods; limitations shown before conclusions.

---

## 6. Demo video flow (3 min 30)
| Time | Scene | On screen |
|---|---|---|
| 0:00 | Intro + hook | Header, title |
| 0:25 | Data | Source line, "About the data" |
| 0:45 | Main answer | 4 change tiles |
| 1:15 | When | NO₂ line chart → switch to O₃ |
| 1:55 | Where | Map → ranking → Overseas + PM10 |
| 2:35 | Quality | Section 3 |
| 3:05 | Conclusion | Section 4, language switch |
