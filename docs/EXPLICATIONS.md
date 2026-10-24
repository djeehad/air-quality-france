# Guide complet du projet — « Not Cleaner Yet »

Ce document t'explique tout le projet, pour que tu puisses le présenter, le défendre à l'oral et le modifier toi-même.

---

## 1. Le projet en une phrase

Une application web Streamlit qui raconte, à partir des mesures officielles de 523 stations, **si l'air en France devient plus propre depuis 2024, quand il est le plus pollué et où**, en comparant les concentrations aux seuils santé de l'OMS.

**Réponse :** non, l'air ne devient pas plus propre. Le trafic pose problème en hiver (NO₂), l'ozone en été.

---

## 2. Le récit (ce que le prof note à 25 %)

Le sujet demande la structure **accroche → contexte → constats → implications**. Voici comment l'app la suit, de haut en bas :

| Partie de l'app | Rôle dans le récit | Ce qu'elle dit |
|---|---|---|
| Titre | Le constat principal | « Pas encore plus propre : le trafic l'hiver, l'ozone l'été » |
| 3 indicateurs (KPI) | Les chiffres clés de la sélection | Moyenne, % de jours au-dessus de l'OMS, zone la plus exposée |
| Accroche | Pourquoi c'est important | 40 000 décès/an liés aux PM2.5 (Santé publique France) ; les 4 polluants ont augmenté depuis 2024 |
| 1. Quand l'air est-il le plus pollué ? | Analyse dans le temps | Trafic vs fond, hiver vs été |
| 2. Où l'exposition est-elle la plus forte ? | Analyse dans l'espace | Carte, classement des zones, saisons par zone |
| 3. Qualité des données & limites | Honnêteté | Ce qui a été nettoyé, ce que les données ne permettent pas de dire |
| 4. Points clés & suites | Conclusions et implications | 5 constats + recommandations |

**Public visé :** citoyens, étudiants, élus locaux.

---

## 3. Les 5 constats (à connaître par cœur pour la vidéo)

Tous calculés sur les vraies données, de janvier 2024 à octobre 2026.

1. **L'air ne devient pas plus propre.** De janvier à octobre, 2026 contre 2024 : NO₂ +5 %, ozone +11 %, PM2.5 +14 %, PM10 +16 %.
   - *Pourquoi « janvier à octobre » ?* Les données 2026 s'arrêtent en octobre. Si on comparait l'année 2024 complète (avec son hiver très pollué) à 2026 sans hiver, on fausserait le résultat. On compare donc **les mêmes mois**.
   - *Vérification :* le résultat tient si l'on garde uniquement les stations présentes les trois années (sinon, l'ouverture de nouvelles stations dans des zones polluées pourrait créer une fausse hausse).

2. **Le trafic fait le problème du NO₂.** Au bord des routes : 21 µg/m³ en moyenne, contre 10 en fond. Le seuil OMS est dépassé **32 %** des jours contre **5 %**, soit environ 6 fois plus souvent.

3. **Chaque saison a son polluant.**
   - Hiver : NO₂ et particules au plus haut (chauffage au bois, air froid et stable qui piège la pollution). Le 17 février 2025, 84 % des stations dépassaient le seuil OMS pour les PM2.5.
   - Été : l'ozone, qui se forme avec le soleil et la chaleur. Ses jours au-dessus du seuil sont passés de 0,6 % (2024) à 4,2 % (2026).

4. **Les particules fines touchent tout le monde :** même loin des routes, le seuil PM2.5 est dépassé environ 9 % des jours.

5. **La géographie dépend du polluant :** NO₂ dans les grandes villes (Perpignan, Montpellier, Strasbourg, Paris), ozone en Corse et en Provence (soleil), PM10 en outre-mer (Mayotte, Antilles), probablement à cause des poussières naturelles et du sel marin.

**Attention à l'oral :** ne dis jamais que la pollution augmente *à cause* de quelque chose. Trois ans, c'est court, et la météo (canicules, hivers froids) pèse beaucoup. Dis plutôt : « les mesures ne montrent pas d'amélioration ».

---

## 4. Les données

**Source :** jeu de données « Données temps réel de mesure des concentrations de polluants atmosphériques réglementés », publié par le **LCSQA** (le laboratoire national de référence) sur **data.gouv.fr**, sous **Licence Ouverte 2.0** (réutilisation libre en citant la source).

**Ce que contient un fichier :** un CSV par jour, avec une ligne par heure, par station et par polluant (environ 48 000 lignes et 12 Mo par jour).

**Ce qu'on a pris :** un jour par semaine (chaque lundi) de janvier 2024 à octobre 2026, soit 147 jours, 523 stations et 71 zones.
*Pourquoi pas tous les jours ?* Ça ferait 4 Go à télécharger. Un jour par semaine suffit pour voir les saisons et les tendances. C'est un **échantillonnage**, à mentionner comme limite.

**Les stations :** le CSV ne donne pas la position GPS. On l'a récupérée dans le fichier de métadonnées (.xls, onglet « AirQualityStations »). 521 stations sur 523 ont été retrouvées.

**Les 4 polluants étudiés :**
| Polluant | C'est quoi | Source principale | Seuil OMS (24 h) |
|---|---|---|---|
| NO₂ | Dioxyde d'azote, un gaz | Trafic routier | 25 µg/m³ |
| PM10 | Particules < 10 micromètres | Chauffage, trafic, poussières | 45 µg/m³ |
| PM2.5 | Particules fines < 2,5 µm (pénètrent dans les poumons) | Chauffage au bois, trafic | 15 µg/m³ |
| O₃ | Ozone | Se forme avec le soleil à partir d'autres polluants | 100 µg/m³ (sur 8 h) |

**Types de stations :** *Trafic* (au bord d'une route), *Fond* (loin des sources directes, ce que respire la majorité des gens), *Industrielle*.

**Zones :** ZAG = grande agglomération (plus de 250 000 habitants), ZAR = autre agglomération, ZR = reste de la région.

---

## 5. Le traitement des données (ce que le prof note à 25 %)

Dans l'ordre :

1. **Téléchargement** (`scripts/download_data.py`) : récupère un fichier par semaine.
2. **Nettoyage horaire :** on retire les heures marquées invalides (`validité = -1`). On garde les heures validées (`1`) et celles pas encore validées (`4`). Ces dernières représentent 13 % des données : les retirer aurait fait perdre beaucoup d'information.
3. **Agrégation :** les 24 valeurs horaires deviennent une moyenne par jour, par station et par polluant. Le fichier de 12 Mo se réduit à quelques Ko.
4. **Règle des 75 % :** une moyenne journalière n'est gardée que si au moins 18 heures sur 24 sont valides (convention européenne). 3 780 jours-stations ont été écartés ainsi.
5. **Contrôles :** 0 doublon, 136 valeurs négatives (physiquement impossibles, donc mises en manquant), environ 2 % de valeurs manquantes par polluant.
6. **Nouvelles variables (feature engineering) :** année, mois, saison, seuil OMS, « au-dessus de l'OMS » (oui/non), « outre-mer » (oui/non, d'après les coordonnées GPS).

Tout cela est affiché dans la **section 3** de l'app : c'est exactement ce que le sujet appelle la « Data quality section ».

---

## 6. L'application, partie par partie

### Barre latérale (filtres)
- **Langue** : anglais ou français.
- **Polluant** : NO₂, PM10, PM2.5, O₃.
- **Années** : curseur de 2024 à 2026.
- **Territoire** : toute la France, métropole ou outre-mer.
- **Zone** et **type de station** : sélection multiple (vide = tout).

Chaque filtre change les indicateurs, les phrases « À retenir » et les graphiques. Les phrases « À retenir » sont **calculées automatiquement** à partir de ta sélection : elles restent donc vraies quel que soit le filtre.

### Les graphiques (tous interactifs : survol, zoom, légende cliquable)
1. **Courbe mensuelle par type de station**, avec la ligne pointillée du seuil OMS. On y voit l'écart trafic/fond et le rythme des saisons.
2. **Carte** : un point par station ; la couleur indique la concentration moyenne et la taille le nombre de jours au-dessus de l'OMS.
3. **Classement des 15 zones les plus exposées** (barres horizontales colorées selon le % de jours au-dessus de l'OMS).
4. **Petits graphiques par saison** pour les 6 zones les plus exposées (les « small multiples » demandés par le sujet).

### Choix de design (à mentionner, c'est noté)
- Palette **Okabe-Ito**, lisible par les daltoniens.
- Axes et unités toujours indiqués (µg/m³).
- **Texte alternatif** sous chaque graphique (accessibilité).
- Ligne de référence OMS sur la courbe (annotation, comme le demande le sujet).

---

## 7. Le code (ce que le prof note à 15 %)

| Fichier | Rôle |
|---|---|
| `app.py` | Point d'entrée : filtres, chargement, ordre des sections |
| `sections/*.py` | Une partie de la page par fichier |
| `utils/constants.py` | **Tous les réglages** au même endroit : adresses, seuils OMS, tes infos |
| `utils/io.py` | Chargement des données (+ coordonnées des stations) |
| `utils/prep.py` | Nettoyage, contrôles, calculs des indicateurs |
| `utils/viz.py` | Les 4 graphiques, avec un style commun |
| `utils/i18n.py` | Tous les textes en anglais et en français |
| `scripts/` | Téléchargement des données et création du fichier des stations |

**Performance :** `@st.cache_data` garde en mémoire les données chargées et les calculs par filtre, ce qui rend l'app rapide. Les données sont pré-agrégées dans un fichier `.parquet` de 0,9 Mo.

**Reproductibilité :** les versions des bibliothèques sont fixées dans `requirements.txt`, et les scripts permettent de tout reconstruire depuis la source.

---

## 8. Ce qu'il te reste à faire

### a) Remplacer ton dossier par la version finale
1. Arrête l'app (`Ctrl + C`).
2. Décompresse le nouveau zip et copie son contenu **par-dessus** ton dossier (« Remplacer les fichiers »).
3. Relance avec `streamlit run app.py`.

### b) Ajouter le logo EFREI
Enregistre le logo officiel sous `assets/logo.png`.

### c) Mettre l'app en ligne (obligatoire : « URL to deployed app »)
1. Crée un compte sur **github.com**.
2. Crée un nouveau dépôt **public**, par exemple `air-quality-france`.
3. Clique sur *Add file → Upload files* et glisse **tout le contenu** du dossier du projet, **sauf** `.venv`, `data/raw` et `data/processed/days`.
4. Va sur **share.streamlit.io**, connecte-toi avec GitHub, puis *Create app*. Choisis ton dépôt, la branche `main` et le fichier `app.py`, et clique sur *Deploy*.
5. Ajoute l'adresse obtenue dans le README, et ton lien GitHub dans `utils/constants.py` (ligne `"github"`).

### d) Enregistrer la vidéo (2 à 4 minutes)
Suis le script dans `docs/SCRIPT_VIDEO.md`. Sur Windows, `Windows + Alt + R` lance l'enregistrement de l'écran avec la Xbox Game Bar.

### e) Rendre le zip
Renomme le dossier et le zip avec ton numéro étudiant : `StApp26_<numéro>_BIAO_BIO.zip`. Il doit contenir le code, le README et le lien du dataset (déjà inclus).

---

## 9. Questions que le prof peut poser (et réponses)

- **Pourquoi un jour par semaine ?** Pour limiter le volume (4 Go sinon) tout en couvrant toutes les saisons. La limite est qu'on peut manquer de courts épisodes de pollution.
- **Pourquoi comparer janvier–octobre ?** Parce que 2026 n'a pas encore de novembre ni de décembre ; comparer des années incomplètes biaiserait le résultat.
- **La hausse est-elle due aux politiques publiques ?** On ne peut pas le dire : la météo joue beaucoup, et trois ans, c'est court. Il faudrait croiser avec les données de Météo-France.
- **Pourquoi l'ozone n'a pas de station trafic ?** L'ozone se forme loin des sources, avec le soleil ; près des routes, il est même détruit par le NO. On le mesure donc en fond.
- **Pourquoi l'outre-mer a autant de PM10 ?** Probablement des sources naturelles (poussières du Sahara aux Antilles, sel marin). C'est une hypothèse, pas une certitude.
- **Pourquoi garder les données « non validées » ?** Elles représentent 13 % des mesures. Les retirer aurait créé des trous ; c'est indiqué comme limite.
