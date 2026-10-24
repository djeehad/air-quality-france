import streamlit as st

from utils import constants as C


def render() -> None:
    """Header required by the course: logo on the left, student & course details on the right."""
    a = C.AUTHOR
    logo_col, info_col = st.columns([1, 2.5], vertical_alignment="center")
    if C.LOGO_PATH.exists():
        logo_col.image(str(C.LOGO_PATH), width=220)
    else:
        logo_col.caption("Add the EFREI logo as assets/logo.png")

    links = [f"[LinkedIn]({a['linkedin']})"]
    if a["github"]:
        links.append(f"[GitHub]({a['github']})")
    info_col.markdown(
        f"""
**{a['name']}** · [{a['email']}](mailto:{a['email']})
**Program:** {a['program']} · **Year:** {a['year']}
{' · '.join(links)}
**Course:** {a['course']}
**Project proposed by:** {a['professor']} · [{a['professor_email']}](mailto:{a['professor_email']})
        """
    )
    st.divider()
