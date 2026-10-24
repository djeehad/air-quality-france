"""English / French texts. Add a key here, then use t("key", **values) in the app.

Numbers written in static texts (hook, conclusions) come from the analysis of the
downloaded data (2024-01-01 → 2026-10-19, one day per week, 523 stations);
re-check them if the data is re-downloaded.
"""
import streamlit as st

TEXT = {
    # ---------------------------------------------------------------- sidebar
    "lang": {"en": "Language / Langue", "fr": "Language / Langue"},
    "filters": {"en": "Filters", "fr": "Filtres"},
    "pollutant": {"en": "Pollutant", "fr": "Polluant"},
    "pollutant_help": {"en": "NO2 = nitrogen dioxide (mostly road traffic) · PM10 / PM2.5 = particles under "
                             "10 / 2.5 µm (heating, traffic, industry, dust) · O3 = ozone (formed by sunlight, summer).",
                       "fr": "NO2 = dioxyde d'azote (surtout le trafic) · PM10 / PM2.5 = particules de moins de "
                             "10 / 2,5 µm (chauffage, trafic, industrie, poussières) · O3 = ozone (formé par le soleil, l'été)."},
    "dates": {"en": "Years", "fr": "Années"},
    "dates_help": {"en": "Indicators compare the last year with the first one, on the same months only.",
                   "fr": "Les indicateurs comparent la dernière année à la première, sur les mêmes mois uniquement."},
    "territory": {"en": "Territory", "fr": "Territoire"},
    "territory_opts": {"en": "All France|Mainland|Overseas", "fr": "Toute la France|Métropole|Outre-mer"},
    "territory_help": {"en": "Overseas = Guadeloupe, Martinique, Guyane, La Réunion, Mayotte.",
                       "fr": "Outre-mer = Guadeloupe, Martinique, Guyane, La Réunion, Mayotte."},
    "zone": {"en": "Zone", "fr": "Zone"},
    "zone_help": {"en": "Official monitoring zones: ZAG = urban area > 250,000 inhabitants, "
                        "ZAR = other urban area, ZR = rest of the region. Empty = all.",
                  "fr": "Zones de surveillance officielles : ZAG = agglomération > 250 000 habitants, "
                        "ZAR = autre agglomération, ZR = reste de la région. Vide = toutes."},
    "influence": {"en": "Station type", "fr": "Type de station"},
    "influence_help": {"en": "Trafic = next to a busy road · Fond (background) = away from direct sources, "
                             "represents what most people breathe · Industrielle = near industry.",
                       "fr": "Trafic = au bord d'un axe fréquenté · Fond = loin des sources directes, ce que respire "
                             "la majorité de la population · Industrielle = près d'un site industriel."},
    "choose": {"en": "Choose options", "fr": "Choisir"},
    "all_zones": {"en": "all zones", "fr": "toutes les zones"},
    "all_types": {"en": "all station types", "fr": "tous types de stations"},
    "selection": {"en": "Your selection", "fr": "Votre sélection"},
    "about": {"en": "About the data", "fr": "À propos des données"},
    "about_text": {"en": "{days} sampled days (one per week), {sites} stations, {d0} → {d1}.",
                   "fr": "{days} jours échantillonnés (un par semaine), {sites} stations, du {d0} au {d1}."},

    # ---------------------------------------------------------------- header / hook
    "title": {"en": "Not Cleaner Yet: Traffic in Winter, Ozone in Summer — France's Air, 2024–2026",
              "fr": "Pas encore plus propre : le trafic l'hiver, l'ozone l'été — l'air en France, 2024–2026"},
    "source": {"en": "Source", "fr": "Source"},
    "demo": {"en": "**Demo mode:** synthetic data. Run `python scripts/download_data.py` for real measurements.",
             "fr": "**Mode démo :** données fictives. Lancez `python scripts/download_data.py` pour les vraies mesures."},
    "hook": {"en": "Air pollution is not just a city nuisance: Santé publique France attributes about "
                   "**40,000 deaths a year** to fine particles (PM2.5) and about **7,000** to nitrogen dioxide "
                   "(estimates published in 2021). So, is the air we breathe getting cleaner? "
                   "**Not according to the stations:** comparing the same months, all four regulated pollutants "
                   "measured more in {y1} than in {y0}.",
             "fr": "La pollution de l'air n'est pas qu'une gêne urbaine : Santé publique France lui attribue environ "
                   "**40 000 décès par an** pour les particules fines (PM2.5) et environ **7 000** pour le dioxyde "
                   "d'azote (estimations publiées en 2021). L'air que nous respirons devient-il plus propre ? "
                   "**Pas selon les stations :** à mois comparables, les quatre polluants réglementés étudiés "
                   "sont plus élevés en {y1} qu'en {y0}."},
    "audience": {"en": "_For citizens, students and local decision-makers who want to know where and when "
                       "the air is most harmful, measured against WHO health guidelines._",
                 "fr": "_Pour les citoyens, étudiants et élus locaux qui veulent savoir où et quand l'air est le "
                       "plus nocif, au regard des recommandations sanitaires de l'OMS._"},
    "change": {"en": "{p}, {y0} → {y1}", "fr": "{p}, {y0} → {y1}"},
    "change_help": {"en": "Change of the mean over all stations, {m} of each year (same months).",
                    "fr": "Évolution de la moyenne de toutes les stations, {m} de chaque année (mêmes mois)."},

    # ---------------------------------------------------------------- KPIs
    "kpi_mean": {"en": "Mean {p}, {m} {y}", "fr": "{p} moyen, {m} {y}"},
    "kpi_mean_help": {"en": "Mean of valid daily station means. Delta vs the same months of {y0}.",
                      "fr": "Moyenne des moyennes journalières valides. Écart vs les mêmes mois de {y0}."},
    "kpi_above": {"en": "Days above WHO, {m} {y}", "fr": "Jours au-dessus de l'OMS, {m} {y}"},
    "kpi_above_help": {"en": "Share of station-days whose daily mean exceeds {w} µg/m³ (WHO 2021 24-hour guideline). "
                             "Delta in percentage points vs the same months of {y0}.",
                       "fr": "Part des jours-stations dont la moyenne dépasse {w} µg/m³ (recommandation OMS 2021 sur 24 h). "
                             "Écart en points vs les mêmes mois de {y0}."},
    "kpi_zone": {"en": "Most exposed zone, {y}", "fr": "Zone la plus exposée, {y}"},
    "kpi_zone_help": {"en": "Zone with the highest mean in the last year; the value below is that mean.",
                      "fr": "Zone à la moyenne la plus élevée la dernière année ; la valeur dessous est cette moyenne."},
    "vs": {"en": "vs", "fr": "vs"},
    "no_data": {"en": "No valid measurements for this selection — widen the filters.",
                "fr": "Aucune mesure valide pour cette sélection — élargissez les filtres."},

    # ---------------------------------------------------------------- sections
    "trend": {"en": "1. When is the air worst?", "fr": "1. Quand l'air est-il le plus pollué ?"},
    "where": {"en": "2. Where is exposure highest?", "fr": "2. Où l'exposition est-elle la plus forte ?"},
    "quality": {"en": "3. Data quality & limitations", "fr": "3. Qualité des données & limites"},
    "conclusions": {"en": "4. Key insights & next steps", "fr": "4. Points clés & suites"},
    "headline_label": {"en": "Headline", "fr": "À retenir"},
    "hl_traffic": {"en": "{p}: traffic stations average **{t:.1f} µg/m³** vs **{b:.1f}** at background stations, "
                         "and exceed the WHO guideline on **{at:.0f}%** of sampled days vs **{ab:.0f}%**.",
                   "fr": "{p} : les stations trafic mesurent en moyenne **{t:.1f} µg/m³** contre **{b:.1f}** en fond, "
                         "et dépassent le seuil OMS **{at:.0f} %** des jours échantillonnés contre **{ab:.0f} %**."},
    "hl_season": {"en": "{p} peaks in **{high}** (**{hv:.1f} µg/m³** on average) and is lowest in {low} ({lv:.1f}).",
                  "fr": "{p} culmine en **{high}** (**{hv:.1f} µg/m³** en moyenne) et est au plus bas en {low} ({lv:.1f})."},
    "hl_where": {"en": "**{zone}** is the most exposed zone for {p} over the selection ({v:.1f} µg/m³, "
                       "{a:.0f}% of days above the WHO guideline).",
                 "fr": "**{zone}** est la zone la plus exposée au {p} sur la sélection ({v:.1f} µg/m³, "
                       "{a:.0f} % des jours au-dessus du seuil OMS)."},
    "trend_note": {"en": "Dashed line = WHO 24-hour guideline. Each point is a monthly mean of the sampled days.",
                   "fr": "Ligne pointillée = seuil OMS sur 24 h. Chaque point est la moyenne mensuelle des jours échantillonnés."},
    "tab_map": {"en": "Map", "fr": "Carte"},
    "tab_rank": {"en": "Zone ranking", "fr": "Classement des zones"},
    "tab_season": {"en": "Seasons", "fr": "Saisons"},
    "map_note": {"en": "Map centred on mainland France; zoom out or pick 'Overseas' to see the overseas stations.",
                 "fr": "Carte centrée sur la métropole ; dézoomez ou choisissez « Outre-mer » pour voir les DROM."},
    "no_coords": {"en": "No station coordinates: add data/stations.csv (see README).",
                  "fr": "Pas de coordonnées : ajoutez data/stations.csv (voir README)."},
    "Winter": {"en": "winter", "fr": "hiver"}, "Spring": {"en": "spring", "fr": "printemps"},
    "Summer": {"en": "summer", "fr": "été"}, "Autumn": {"en": "autumn", "fr": "automne"},

    # ---------------------------------------------------------------- data quality
    "q_rows": {"en": "Station-day rows", "fr": "Lignes station-jour"},
    "q_dupes": {"en": "Duplicates removed", "fr": "Doublons supprimés"},
    "q_neg": {"en": "Negative values → missing", "fr": "Valeurs négatives → manquantes"},
    "q_short": {"en": "Days < 18 valid hours → missing", "fr": "Jours < 18 h valides → manquants"},
    "q_period": {"en": "Period: {d0} → {d1} · {days} sampled days · {sites} stations "
                       "({nc} without coordinates, kept out of the map only).",
                 "fr": "Période : {d0} → {d1} · {days} jours échantillonnés · {sites} stations "
                       "({nc} sans coordonnées, exclues de la carte uniquement)."},
    "q_missing_col": {"en": "Missing values by column (%)", "fr": "Valeurs manquantes par colonne (%)"},
    "q_missing_pol": {"en": "Missing daily values by pollutant (%)", "fr": "Valeurs journalières manquantes par polluant (%)"},
    "q_limits": {
        "en": """
**How the data was processed**
- Source files: one CSV per day with hourly values. Hours flagged invalid (`validité = -1`) are removed;
  validated (`1`) and not-yet-validated (`4`) hours are kept.
- A daily mean is kept only with at least 18 valid hours out of 24 (75 %, the EU convention).
- **Sampling:** one day per week (every Monday) from January 2024 — 147 days. It captures seasons and
  trends but can miss short pollution episodes.

**Limitations — read before concluding**
- *Real-time* data are **not yet validated** by the monitoring agencies and may be revised.
- **Three years is short** and weather drives pollution (heatwaves → ozone, cold anticyclones → particles):
  the rise since 2024 can be partly meteorological, not only a change in emissions.
- Stations are placed to watch hotspots (roads, industry): averages describe **monitored places**,
  not the exposure of the whole population.
- WHO guidelines are compared with daily means; for O₃ the WHO value is an 8-hour maximum, so ozone
  exceedances are **under-estimated** here.
- These are correlations: no causal effect of any policy is claimed.
""",
        "fr": """
**Comment les données ont été traitées**
- Fichiers source : un CSV par jour avec des valeurs horaires. Les heures marquées invalides (`validité = -1`)
  sont retirées ; les heures validées (`1`) et non encore validées (`4`) sont conservées.
- Une moyenne journalière n'est gardée qu'avec au moins 18 heures valides sur 24 (75 %, convention européenne).
- **Échantillonnage :** un jour par semaine (chaque lundi) depuis janvier 2024, soit 147 jours. Cela suffit
  pour les saisons et les tendances, mais peut manquer de courts épisodes de pollution.

**Limites — à lire avant de conclure**
- Les données *temps réel* **ne sont pas encore validées** par les associations de surveillance et peuvent être révisées.
- **Trois ans, c'est court** et la météo pèse lourd (canicules → ozone, anticyclones froids → particules) :
  la hausse depuis 2024 peut être en partie météorologique, pas seulement liée aux émissions.
- Les stations surveillent en priorité les points chauds (routes, industrie) : les moyennes décrivent
  **les lieux mesurés**, pas l'exposition de toute la population.
- Les seuils OMS sont comparés à des moyennes journalières ; pour l'O₃, la valeur OMS porte sur un maximum
  sur 8 heures, donc les dépassements d'ozone sont ici **sous-estimés**.
- Ce sont des corrélations : aucun effet causal d'une politique n'est affirmé.
"""},

    # ---------------------------------------------------------------- conclusions
    "insights": {
        "en": """
**What the data shows**
1. **The air is not getting cleaner.** Comparing January–October, every pollutant is higher in 2026 than in 2024:
   NO₂ +5 %, O₃ +11 %, PM2.5 +14 %, PM10 +16 %. The trend holds when only stations present all three years are kept.
2. **Traffic is the NO₂ problem.** Next to roads, NO₂ averages about twice the background level (21 vs 10 µg/m³)
   and exceeds the WHO guideline on **32 %** of sampled days, against **5 %** at background stations — about 6 times more often.
3. **Each season has its pollutant.** NO₂ and particles peak in **winter** (heating, cold still air);
   on the worst winter day sampled (17 Feb 2025), 84 % of PM2.5 stations were above the WHO guideline.
   Ozone peaks in **summer** with sunshine and heat: its share of days above the guideline went from
   0.6 % (2024) to 4.2 % (2026).
4. **Fine particles reach everyone.** Even background stations exceed the PM2.5 guideline on about 9 % of days.
5. **Geography differs by pollutant:** NO₂ is highest in large southern and eastern cities (Perpignan,
   Montpellier, Strasbourg, Paris), ozone in Corsica and Provence, PM10 in the overseas territories
   (Mayotte, Antilles), probably because of natural dust and sea salt.
""",
        "fr": """
**Ce que montrent les données**
1. **L'air ne devient pas plus propre.** De janvier à octobre, chaque polluant est plus élevé en 2026 qu'en 2024 :
   NO₂ +5 %, O₃ +11 %, PM2.5 +14 %, PM10 +16 %. La tendance se maintient si l'on ne garde que les stations présentes les trois années.
2. **Le trafic fait le problème du NO₂.** Au bord des routes, le NO₂ atteint environ le double du niveau de fond
   (21 contre 10 µg/m³) et dépasse le seuil OMS **32 %** des jours échantillonnés, contre **5 %** en fond, soit environ 6 fois plus souvent.
3. **Chaque saison a son polluant.** Le NO₂ et les particules culminent en **hiver** (chauffage, air froid et stable) ;
   lors du pire jour d'hiver échantillonné (17 février 2025), 84 % des stations PM2.5 dépassaient le seuil OMS.
   L'ozone culmine en **été** avec le soleil et la chaleur : sa part de jours au-dessus du seuil est passée de
   0,6 % (2024) à 4,2 % (2026).
4. **Les particules fines touchent tout le monde.** Même les stations de fond dépassent le seuil PM2.5 environ 9 % des jours.
5. **La géographie dépend du polluant :** le NO₂ est le plus élevé dans les grandes villes du Sud et de l'Est
   (Perpignan, Montpellier, Strasbourg, Paris), l'ozone en Corse et en Provence, les PM10 en outre-mer
   (Mayotte, Antilles), probablement à cause des poussières naturelles et du sel marin.
"""},
    "next_steps": {
        "en": """
**Implications & next steps**
- **Traffic measures** (low-emission zones, ZFE) target the clearest problem: NO₂ along busy roads.
- **Winter** calls for action on wood heating and particle-episode alerts; **summer** for ozone alerts,
  a risk likely to grow with heatwaves.
- **To go further:** add Météo-France weather data to separate weather from emissions, use the validated annual
  data once published, and extend the period beyond three years before talking about a lasting trend.
""",
        "fr": """
**Implications & suites**
- Les **mesures sur le trafic** (zones à faibles émissions, ZFE) visent le problème le plus net : le NO₂ le long des axes.
- L'**hiver** appelle des actions sur le chauffage au bois et des alertes particules ; l'**été**, des alertes ozone,
  un risque qui devrait augmenter avec les canicules.
- **Pour aller plus loin :** croiser avec les données météo de Météo-France pour séparer météo et émissions, utiliser
  les données annuelles validées une fois publiées, et allonger la période au-delà de trois ans avant de parler de tendance durable.
"""},
}


def t(key: str, **kw) -> str:
    lang = st.session_state.get("lang", "en")
    return TEXT[key][lang].format(**kw) if kw else TEXT[key][lang]
