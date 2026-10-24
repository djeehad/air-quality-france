"""Section 3: data quality checks and limitations."""
import streamlit as st

from utils.i18n import t


def render(report: dict) -> None:
    st.subheader(t("quality"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("q_rows"), f"{report['rows']:,}")
    c2.metric(t("q_dupes"), report["duplicates"])
    c3.metric(t("q_neg"), report["negative_values"])
    c4.metric(t("q_short"), f"{report['short_days']:,}")
    st.caption(t("q_period", d0=f"{report['date_min']:%Y-%m-%d}", d1=f"{report['date_max']:%Y-%m-%d}",
                 days=report["days"], sites=report["sites"], nc=report["no_coords"]))

    left, right = st.columns(2)
    left.markdown(f"**{t('q_missing_col')}**")
    left.dataframe(report["missing_by_col"], width="stretch")
    right.markdown(f"**{t('q_missing_pol')}**")
    right.dataframe(report["missing_by_pollutant"].rename("%"), width="stretch")
    st.info(t("q_limits"))
