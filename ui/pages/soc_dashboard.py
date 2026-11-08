"""
ROBOGUARD AI — 3D Robotics SOC Dashboard Page
Embedded interactive Three.js 3D AMR Robot Hero Viewport, Cyberattack
Simulator, Hardware Teardown, and Dynamic Physics Computational Graph.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from config.settings import UI_THEME


def render_soc_dashboard_page():
    """Renders the embedded 3D Robotics SOC & Cyber-Physical Defense Center."""
    
    st.markdown(f"""
    <div style="margin-bottom: 0.75rem;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h2 style="font-size: 1.4rem; font-weight: 800; color: {UI_THEME['text_primary']}; margin: 0; letter-spacing: -0.02em;">
                    🛡️ 3D Robotics SOC &amp; Cyber-Physical Defense Center
                </h2>
                <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.2rem;">
                    Hardware-Engineered AMR 3D Digital Twin · SROS2 Cyberattack Tackling Simulator · Dynamic Python Computational Graph
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar
    col1, col2, col3 = st.columns([1.5, 1, 1])
    
    with col1:
        st.caption("Active Target: **AMR Rover (ROBOGUARD-X1)** · Three.js WebGL Engine")

    with col2:
        zip_path = "stitch_roboguard_ai_soc_dashboard_pro.zip"
        if os.path.exists(zip_path):
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Download Offline SOC (.zip)",
                    data=f.read(),
                    file_name="roboguard_ai_soc_dashboard_pro.zip",
                    mime="application/zip",
                    width="stretch"
                )

    with col3:
        html_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "soc_dashboard.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                st.download_button(
                    label="🌐 Export Standalone HTML",
                    data=f.read(),
                    file_name="soc_dashboard.html",
                    mime="text/html",
                    width="stretch"
                )

    # Read and embed the high-fidelity HTML/WebGL application
    html_file = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "soc_dashboard.html")
    
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_code = f.read()

        # Render full-screen interactive component
        components.html(html_code, height=920, scrolling=True)
    else:
        st.error(f"SOC Dashboard asset not found at {html_file}")
