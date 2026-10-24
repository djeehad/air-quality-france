"""Section 4: insights and next steps (written from the analysis of the real data)."""
import streamlit as st

from utils.i18n import t


def render() -> None:
    st.subheader(t("conclusions"))
    st.success(t("insights"))
    st.info(t("next_steps"))
