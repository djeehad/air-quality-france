"""Single place for every assumption the app relies on.

Change values here, never inline in the code, so the README and the app stay in sync.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DAILY_PARQUET = PROCESSED_DIR / "daily.parquet"
STATIONS_CSV = ROOT / "data" / "stations.csv"  

# --- Source -----------------------------------------------------------------
DATASET_TITLE = "Données « temps réel » de mesure des concentrations de polluants atmosphériques réglementés"
DATASET_URL = "https://www.data.gouv.fr/datasets/5b98b648634f415309d52a50"
PRODUCER = "LCSQA — Laboratoire Central de Surveillance de la Qualité de l'Air (Geod'air)"
LICENSE = "Licence Ouverte / Open Licence 2.0 (Etalab)"
# One CSV per day, e.g. .../temps-reel/2026/FR_E2_2026-10-20.csv
DAILY_FILE_URL = (
    "https://files.data.gouv.fr/ineris/lcsqa/"
    "concentrations-de-polluants-atmospheriques-reglementes/temps-reel/{year}/FR_E2_{date}.csv"
)

# Raw E2 column names -> internal names. Check against a real file and fix here.
COLUMN_MAP = {
    "Date de début": "start",
    "Organisme": "organisme",
    "Zas": "zone",
    "code site": "code_site",
    "nom site": "site",
    "type d'implantation": "setting",
    "type d'influence": "influence",
    "Polluant": "pollutant",
    "valeur": "value",
    "unité de mesure": "unit",
    "validité": "validity",
}

# --- Analysis assumptions ---------------------------------------------------
SEED = 42
POLLUTANTS = ["NO2", "PM10", "PM2.5", "O3"]
MIN_HOURS_PER_DAY = 18  # a daily mean needs >= 75 % of hours (EU convention)

# WHO 2021 air-quality guidelines, 24-hour levels, µg/m³ (O3 is an 8-h guideline;
# applied here to the daily mean as a simplification — say so in the app).
WHO_DAILY = {"NO2": 25, "PM10": 45, "PM2.5": 15, "O3": 100}
# EU annual limit values (Directive 2008/50/EC), µg/m³, for context lines.
EU_ANNUAL = {"NO2": 40, "PM10": 40, "PM2.5": 25}

# --- Header block (edit with your own details) -------------------------------
AUTHOR = {
    "name": "BIAO Ashley",
    "program": "Ing2-BIO",
    "year": "2026",
    "email": "ashley.biao@efrei.net",
    "linkedin": "https://www.linkedin.com/in/ashley-djeehad-biao-76b720330/",
    "github": "https://github.com/djeehad/djeehad",
    "course": "Data Visualization",
    "professor": "Prof. Mano Mathew",
    "professor_email": "mano.mathew@efrei.fr",
}
LOGO_PATH = ROOT / "assets" / "logo.png"  

# --- Display limits (the real data has ~70 monitoring zones) ------------------
TOP_N_ZONES = 15        # zone ranking: N most exposed zones
SMALL_MULTIPLES_N = 6   # seasonal small multiples: N most exposed zones
