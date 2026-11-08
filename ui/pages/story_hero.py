"""
ROBOGUARD AI — Storytelling Hero Landing Page
Cinematic 3D mission briefing, real-time threat simulation, and automated tackling.
"""

import os
import streamlit as st
import streamlit.components.v1 as components


def render_story_hero_page():
    """Renders the dedicated 3D Storytelling Hero Landing Page."""
    
    # Check if iframe requested navigation via query params or postMessage
    if st.query_params.get("nav") == "soc":
        try:
            st.query_params.clear()
        except Exception:
            pass
        st.session_state["nav_selection"] = "🛡️ 3D Robotics SOC"
        st.rerun()

    # CTA Banner connecting into the Enterprise SOC Dashboard
    col_txt, col_btn = st.columns([3, 1])
    with col_txt:
        st.markdown("""
        <div style="padding: 0.25rem 0;">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #2563EB; font-weight: 800;">
                ● MISSION BRIEFING · 3D DIGITAL TWIN · SROS2 CYBER-PHYSICAL DEFENSE
            </div>
            <div style="font-size: 0.875rem; color: #475569; margin-top: 0.15rem;">
                Explore real-time robotics kinematics, simulate cyber threats, and transition seamlessly to the Enterprise SOC.
            </div>
        </div>
        <script>
            window.addEventListener('message', function(event) {
                if (event.data && event.data.type === 'ROBOGUARD_NAVIGATE') {
                    const btn = window.document.querySelector('button[kind="primary"]');
                    if (btn) btn.click();
                }
            });
        </script>
        """, unsafe_allow_html=True)
    with col_btn:
        if st.button("🚀 Enter Enterprise Robotics SOC", type="primary", use_container_width=True):
            st.session_state["nav_selection"] = "🛡️ 3D Robotics SOC"
            st.rerun()

    # Load and render the high-craft HTML/WebGL storytelling application
    hero_html_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "story_hero.html")
    
    if os.path.exists(hero_html_path):
        with open(hero_html_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=980, scrolling=True)
    else:
        st.error(f"Hero asset not found at {hero_html_path}")
