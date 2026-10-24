"""Cleaning, validation, feature engineering and pre-aggregation.

Pure functions (no Streamlit), so they can be tested and reused in notebooks.
"""
from __future__ import annotations

import calendar

import pandas as pd

from utils import constants as C

KEY = ["date", "code_site", "pollutant"]
SEASONS = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
           6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"}
# Bounding box of mainland France + Corsica; stations outside are overseas (DROM).
MAINLAND = {"lat": (41.0, 51.5), "lon": (-5.5, 10.0)}


# --------------------------------------------------------------------------- quality
def quality_report(df: pd.DataFrame) -> dict:
    """Checks shown in the Data Quality section. Run on the data BEFORE cleaning."""
    return {
        "rows": len(df),
        "duplicates": int(df.duplicated(subset=KEY).sum()),
        "missing_by_col": df.isna().mean().mul(100).round(1).rename("% missing"),
        "negative_values": int((df["value"] < 0).sum()),
        "short_days": int(((df["n_hours"] > 0) & (df["n_hours"] < C.MIN_HOURS_PER_DAY)).sum()),
        "date_min": df["date"].min(),
        "date_max": df["date"].max(),
        "days": df["date"].nunique(),
        "sites": df["code_site"].nunique(),
        "no_coords": int(df.loc[df["lat"].isna(), "code_site"].nunique()),
        "missing_by_pollutant": df.groupby("pollutant")["value"].apply(lambda s: s.isna().mean() * 100).round(1),
    }


# --------------------------------------------------------------------------- cleaning
def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=KEY).copy()
    df = df[df["pollutant"].isin(C.POLLUTANTS)]
    df["date"] = pd.to_datetime(df["date"])
    df.loc[df["value"] < 0, "value"] = pd.NA                          # physically impossible
    df.loc[df["n_hours"] < C.MIN_HOURS_PER_DAY, "value"] = pd.NA       # not representative of the day
    # Feature engineering
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["season"] = df["month_num"].map(SEASONS)
    df["who_limit"] = df["pollutant"].map(C.WHO_DAILY)
    df["above_who"] = df["value"] > df["who_limit"]
    inside = df["lat"].between(*MAINLAND["lat"]) & df["lon"].between(*MAINLAND["lon"])
    df["overseas"] = df["lat"].notna() & ~inside
    return df


def filter_df(df: pd.DataFrame, pollutant: str, zones: list[str], influences: list[str],
              start, end, territory: str = "all") -> pd.DataFrame:
    m = (df["pollutant"] == pollutant) & df["date"].between(pd.Timestamp(start), pd.Timestamp(end))
    if zones:
        m &= df["zone"].isin(zones)
    if influences:
        m &= df["influence"].isin(influences)
    if territory == "mainland":
        m &= ~df["overseas"]
    elif territory == "overseas":
        m &= df["overseas"]
    return df[m]


# --------------------------------------------------------------------------- comparisons
def comparable(valid: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Keep only the calendar months present in the last year, so that a partial last
    year (e.g. Jan–Oct) is compared with the same months of earlier years.
    Without this, a missing winter would make NO2/PM look lower and O3 higher."""
    last = valid["year"].max()
    months = sorted(valid.loc[valid["year"] == last, "month_num"].unique())
    label = f"{calendar.month_abbr[months[0]]}–{calendar.month_abbr[months[-1]]}" if months else ""
    return valid[valid["month_num"].isin(months)], label


def kpis(df: pd.DataFrame) -> dict | None:
    """Last year of the selection vs the first year, on the same months."""
    valid = df.dropna(subset=["value"])
    if valid.empty:
        return None
    same, months = comparable(valid)
    y0, y1 = int(same["year"].min()), int(same["year"].max())
    first, last = same[same["year"] == y0], same[same["year"] == y1]
    zones = last.groupby("zone")["value"].mean().sort_values()
    mean0, mean1 = first["value"].mean(), last["value"].mean()
    return {
        "y0": y0, "y1": y1, "months": months,
        "mean": mean1,
        "mean_pct": (mean1 / mean0 - 1) * 100 if y1 > y0 else None,
        "above": last["above_who"].mean() * 100,
        "above_pts": (last["above_who"].mean() - first["above_who"].mean()) * 100 if y1 > y0 else None,
        "top_zone": zones.index[-1],
        "top_zone_value": zones.iloc[-1],
    }


def change_by_pollutant(df: pd.DataFrame) -> pd.DataFrame:
    """National mean change first -> last year per pollutant, same months (for the hook)."""
    valid, months = comparable(df.dropna(subset=["value"]))
    y0, y1 = valid["year"].min(), valid["year"].max()
    m = valid[valid["year"].isin([y0, y1])].groupby(["pollutant", "year"])["value"].mean().unstack()
    out = pd.DataFrame({"pct": (m[y1] / m[y0] - 1) * 100}).reset_index()
    out["y0"], out["y1"], out["months"] = y0, y1, months
    return out.sort_values("pct")


def traffic_vs_background(df: pd.DataFrame) -> dict | None:
    """Means and WHO-exceedance shares for traffic vs background stations (headline 1)."""
    valid = df.dropna(subset=["value"])
    g = valid.groupby("influence").agg(mean=("value", "mean"), above=("above_who", "mean"))
    if not {"Trafic", "Fond"} <= set(g.index):
        return None
    t, b = g.loc["Trafic"], g.loc["Fond"]
    return {"traffic": t["mean"], "background": b["mean"],
            "above_t": t["above"] * 100, "above_b": b["above"] * 100,
            "ratio": t["above"] / b["above"] if b["above"] > 0 else None}


def peak_season(df: pd.DataFrame) -> dict | None:
    valid = df.dropna(subset=["value"])
    s = valid.groupby("season")["value"].mean()
    if len(s) < 2:
        return None
    return {"high": s.idxmax(), "high_v": s.max(), "low": s.idxmin(), "low_v": s.min()}


# --------------------------------------------------------------------------- chart tables
def make_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Pre-aggregations reused by the charts (df is already filtered)."""
    valid = df.dropna(subset=["value"])
    by_zone = (valid.groupby("zone", as_index=False)
                    .agg(mean=("value", "mean"), pct_above=("above_who", "mean"),
                         stations=("code_site", "nunique"))
                    .assign(pct_above=lambda t: t["pct_above"] * 100)
                    .sort_values("mean"))
    top_zones = by_zone["zone"].tail(C.SMALL_MULTIPLES_N)
    return {
        "timeseries": valid.groupby(["month", "influence"], as_index=False)["value"].mean(),
        "by_zone": by_zone.tail(C.TOP_N_ZONES),
        "geo": valid.dropna(subset=["lat", "lon"])
                    .groupby(["code_site", "site", "zone", "influence", "lat", "lon"], as_index=False)
                    .agg(mean=("value", "mean"), days_above=("above_who", "sum"), days=("value", "size")),
        "season": valid[valid["zone"].isin(top_zones)]
                       .groupby(["zone", "season"], as_index=False)["value"].mean(),
    }
