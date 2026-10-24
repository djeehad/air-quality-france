"""KPI row, hook and section 1 (when is the air worst?)."""
import streamlit as st

from utils import prep, viz
from utils.i18n import t
from utils.viz import UNIT


def render_kpis(df, pollutant: str, who: float) -> bool:
    k = prep.kpis(df)
    if k is None:
        st.info(t("no_data"))
        return False
    c1, c2, c3 = st.columns(3)
    c1.metric(t("kpi_mean", p=pollutant, m=k["months"], y=k["y1"]), f"{k['mean']:.1f} {UNIT}",
              None if k["mean_pct"] is None else f"{k['mean_pct']:+.1f}% {t('vs')} {k['y0']}",
              delta_color="inverse", help=t("kpi_mean_help", y0=k["y0"]))
    c2.metric(t("kpi_above", m=k["months"], y=k["y1"]), f"{k['above']:.1f} %",
              None if k["above_pts"] is None else f"{k['above_pts']:+.1f} pts {t('vs')} {k['y0']}",
              delta_color="inverse", help=t("kpi_above_help", w=who, y0=k["y0"]))
    c3.metric(t("kpi_zone", y=k["y1"]), k["top_zone"], f"{k['top_zone_value']:.1f} {UNIT}",
              delta_color="off", help=t("kpi_zone_help"))
    return True


def render_hook(changes) -> None:
    """Hook: national change of every pollutant, same months, first vs last year (not filtered)."""
    st.divider()
    if changes.empty or changes["y0"].iloc[0] == changes["y1"].iloc[0]:
        return  # needs at least two years of data
    y0, y1, months = int(changes["y0"].iloc[0]), int(changes["y1"].iloc[0]), changes["months"].iloc[0]
    st.markdown(t("hook", y0=y0, y1=y1))
    st.markdown(t("audience"))
    cols = st.columns(len(changes))
    for col, (_, row) in zip(cols, changes.iterrows()):
        col.metric(t("change", p=row["pollutant"], y0=y0, y1=y1), f"{row['pct']:+.0f}%",
                   delta="▲" if row["pct"] > 0 else "▼", delta_color="inverse" if row["pct"] > 0 else "normal",
                   help=t("change_help", m=months))
    st.divider()


def render_trend(df, tables, pollutant: str, who: float) -> None:
    st.subheader(t("trend"))
    tvb, season = prep.traffic_vs_background(df), prep.peak_season(df)
    if tvb:
        st.markdown(f"**{t('headline_label')} —** " + t("hl_traffic", p=pollutant, t=tvb["traffic"],
                    b=tvb["background"], at=tvb["above_t"], ab=tvb["above_b"]))
    if season:
        st.markdown(("" if tvb else f"**{t('headline_label')} —** ") + t(
            "hl_season", p=pollutant, high=t(season["high"]), hv=season["high_v"],
            low=t(season["low"]), lv=season["low_v"]))
    st.plotly_chart(viz.line_chart(tables["timeseries"], pollutant, who), width="stretch")
    st.caption(t("trend_note") + f" Alt text: line chart of the monthly mean {pollutant} in {UNIT} by "
               f"station type, with a dashed reference line at the WHO guideline of {who} {UNIT}.")
