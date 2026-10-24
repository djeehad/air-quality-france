"""Loading: processed parquet if present, otherwise a clearly labelled demo sample."""
from __future__ import annotations

import numpy as np
import pandas as pd

from utils import constants as C


def load_data() -> tuple[pd.DataFrame, bool]:
    """Return (daily dataframe, is_demo).

    Real data is produced by `python scripts/download_data.py`.
    Until then the app runs on a synthetic sample with the same schema so the
    whole pipeline can be developed and tested from a clean checkout.
    """
    if C.DAILY_PARQUET.exists():
        df = pd.read_parquet(C.DAILY_PARQUET)
        if C.STATIONS_CSV.exists():
            stations = pd.read_csv(C.STATIONS_CSV, dtype={"code_site": str})
            df = df.drop(columns=["lat", "lon"], errors="ignore").merge(
                stations[["code_site", "lat", "lon"]], on="code_site", how="left"
            )
        for col in ("lat", "lon"):  # no coordinates yet -> the map tab shows a message
            if col not in df:
                df[col] = float("nan")
        return df, False
    return make_demo_data(), True


def make_demo_data(n_sites: int = 40, days: int = 730) -> pd.DataFrame:
    """Deterministic synthetic daily means. NOT real measurements."""
    rng = np.random.default_rng(C.SEED)
    zones = ["ZAG Paris", "ZAG Lyon", "ZAG Marseille-Aix", "ZAG Lille", "ZR Bretagne", "ZR Occitanie"]
    centers = {
        "ZAG Paris": (48.86, 2.35), "ZAG Lyon": (45.76, 4.84), "ZAG Marseille-Aix": (43.30, 5.37),
        "ZAG Lille": (50.63, 3.06), "ZR Bretagne": (48.11, -1.68), "ZR Occitanie": (43.60, 1.44),
    }
    base = {"NO2": 22, "PM10": 18, "PM2.5": 10, "O3": 55}
    dates = pd.date_range(end=pd.Timestamp.today().normalize() - pd.Timedelta(days=1), periods=days)
    doy = dates.dayofyear.to_numpy()

    rows = []
    for i in range(n_sites):
        zone = zones[i % len(zones)]
        setting = rng.choice(["Urbaine", "Périurbaine", "Rurale"], p=[0.6, 0.25, 0.15])
        influence = rng.choice(["Trafic", "Fond", "Industrielle"], p=[0.35, 0.55, 0.10])
        lat, lon = centers[zone]
        lat, lon = lat + rng.normal(0, 0.12), lon + rng.normal(0, 0.15)
        for pol, b in base.items():
            winter = np.cos(2 * np.pi * (doy - 15) / 365)
            season = winter if pol != "O3" else -winter  # O3 peaks in summer
            mult = 1.8 if (influence == "Trafic" and pol == "NO2") else 1.0
            trend = np.linspace(1.0, 0.9, days)  # gentle decline
            v = b * mult * trend * (1 + 0.35 * season) * rng.lognormal(0, 0.3, days)
            v[rng.random(days) < 0.04] = np.nan  # missing days
            rows.append(pd.DataFrame({
                "date": dates, "code_site": f"FR{10000 + i}", "site": f"Station {i:02d}",
                "zone": zone, "setting": setting, "influence": influence,
                "pollutant": pol, "value": v.round(1), "unit": "µg-m3",
                "n_hours": np.where(np.isnan(v), 0, 24), "lat": lat, "lon": lon,
            }))
    df = pd.concat(rows, ignore_index=True)
    return pd.concat([df, df.sample(25, random_state=C.SEED)], ignore_index=True)  # a few duplicates to detect
