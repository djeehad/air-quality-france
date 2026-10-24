"""Air quality in France, 2024–2026 — Streamlit data story.

Run:  streamlit run app.py
Data: python scripts/download_data.py  (see README.md)
"""
import streamlit as st

from sections import conclusions, deep_dives, header, overview, quality
from utils import constants as C
from utils import prep
from utils.i18n import t
from utils.io import load_data

st.set_page_config(page_title="Air Quality in France", layout="wide")


@st.cache_data(show_spinner="Loading data…")
def get_data():
    """Load + validate + clean once; cached across reruns and users."""
    raw, is_demo = load_data()
    df = prep.clean(raw)
    return prep.quality_report(raw), df, prep.change_by_pollutant(df), is_demo


@st.cache_data(show_spinner=False)
def get_tables(df, pollutant, zones, influences, start, end, territory):
    """Filter + pre-aggregate for the charts; cached per filter combination."""
    sub = prep.filter_df(df, pollutant, list(zones), list(influences), start, end, territory)
    return sub, prep.make_tables(sub)


report, df, changes, is_demo = get_data()

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    lang = st.radio(t("lang"), ["English", "Français"])
    st.session_state["lang"] = "fr" if lang == "Français" else "en"

    st.header(t("filters"))
    pollutant = st.selectbox(t("pollutant"), C.POLLUTANTS, help=t("pollutant_help"))
    y_min, y_max = int(df["year"].min()), int(df["year"].max())
    if y_min < y_max:
        years = st.slider(t("dates"), y_min, y_max, (y_min, y_max), help=t("dates_help"))
    else:  # a slider needs two distinct bounds
        years = (y_min, y_max)
        st.caption(f"{t('dates')}: {y_min}")
    labels = t("territory_opts").split("|")
    territory = dict(zip(labels, ["all", "mainland", "overseas"]))[
        st.radio(t("territory"), labels, horizontal=True, help=t("territory_help"))]
    zones = st.multiselect(t("zone"), sorted(df["zone"].dropna().unique()),
                           placeholder=t("choose"), help=t("zone_help"))
    influences = st.multiselect(t("influence"), sorted(df["influence"].dropna().unique()),
                                placeholder=t("choose"), help=t("influence_help"))
    st.divider()
    st.caption(f"**{t('about')}** — " + t("about_text", days=report["days"], sites=report["sites"],
                                           d0=f"{report['date_min']:%Y-%m-%d}", d1=f"{report['date_max']:%Y-%m-%d}"))

start, end = f"{years[0]}-01-01", f"{years[1]}-12-31"
sub, tables = get_tables(df, pollutant, tuple(zones), tuple(influences), start, end, territory)
who = C.WHO_DAILY[pollutant]

# ---------------------------------------------------------------- page
header.render()
st.title(t("title"))
st.caption(f"{t('source')}: {C.DATASET_TITLE} — {C.PRODUCER} — data.gouv.fr — {C.LICENSE}")
st.caption(f"{t('selection')}: {pollutant} · {years[0]}–{years[1]} · "
           f"{dict(zip(['all', 'mainland', 'overseas'], labels))[territory]} · "
           f"{', '.join(zones) or t('all_zones')} · {', '.join(influences) or t('all_types')}")
if is_demo:
    st.warning(t("demo"))

if overview.render_kpis(sub, pollutant, who):
    overview.render_hook(changes)
    overview.render_trend(sub, tables, pollutant, who)
    st.divider()
    deep_dives.render(tables, pollutant)
st.divider()
quality.render(report)
st.divider()
conclusions.render()
