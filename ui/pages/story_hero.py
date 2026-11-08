"""
ROBOGUARD AI — Storytelling Hero Landing Page
Cinematic GSAP ScrollTrigger 3D mission briefing (offline-first).
"""

import streamlit as st
import streamlit.components.v1 as components

from ui.asset_loader import load_html_asset

SOC_NAV_LABEL = "🛡️ 3D Robotics SOC"


def render_story_hero_page():
    """Renders the dedicated 3D Storytelling Hero Landing Page."""
    if st.query_params.get("nav") == "soc":
        try:
            st.query_params.clear()
        except Exception:
            pass
        st.session_state["nav_selection"] = SOC_NAV_LABEL
        st.rerun()

    # The iframe's "Enter SOC" buttons click this proxy button (same-origin).
    # It is visually collapsed so the page shows one clean CTA, not two.
    with st.container(key="hero_cta_proxy"):
        if st.button("Enter Enterprise Robotics SOC", type="primary", key="hero_cta_btn"):
            st.session_state["nav_selection"] = SOC_NAV_LABEL
            st.rerun()

    # The story page ships its own in-scene Sentinel dock; hide the global one here
    # so two floating assistants never overlap.
    st.markdown(
        "<style>div[data-testid='stPopover'], div:has(> div[data-testid='stPopover']) "
        "{ display: none !important; }</style>",
        unsafe_allow_html=True,
    )

    try:
        html_code = load_html_asset("story_hero.html")
    except FileNotFoundError as exc:
        st.error(str(exc))
        return
    components.html(html_code, height=1000, scrolling=True)
