"""Section 2: where is exposure highest? (map, ranking, seasonal small multiples)."""
import streamlit as st

from utils import viz
from utils.i18n import t


def render(tables, pollutant: str) -> None:
    st.subheader(t("where"))
    zones = tables["by_zone"]
    if not zones.empty:
        top = zones.iloc[-1]
        st.markdown(f"**{t('headline_label')} —** " + t("hl_where", zone=top["zone"], p=pollutant,
                                                          v=top["mean"], a=top["pct_above"]))

    tab_map, tab_rank, tab_season = st.tabs([t("tab_map"), t("tab_rank"), t("tab_season")])
    with tab_map:
        if tables["geo"].empty:
            st.info(t("no_coords"))
        else:
            st.plotly_chart(viz.map_chart(tables["geo"], pollutant), width="stretch")
            st.caption(t("map_note") + f" Alt text: map of France, one dot per station, colour = mean "
                       f"{pollutant}, size = number of sampled days above the WHO guideline.")
    with tab_rank:
        st.plotly_chart(viz.bar_chart(zones, pollutant), width="stretch")
        st.caption("Alt text: horizontal bars ranking the most exposed zones by mean concentration; "
                   "colour shows the share of days above the WHO guideline.")
    with tab_season:
        st.plotly_chart(viz.season_small_multiples(tables["season"], pollutant), width="stretch")
        st.caption("Alt text: one small bar chart per zone (the most exposed ones) showing the mean by season.")
