"""
ROBOGUARD AI — 3D Robotics SOC Dashboard Page
Embeds the offline-first Three.js digital twin, cyberattack simulator and
the Python-computed (NetworkX) ROS 2 computational graph.
"""

import streamlit as st
import streamlit.components.v1 as components

from config.settings import UI_THEME
from core.dynamic_graph_generator import DynamicGraphGenerator
from ui.asset_loader import load_html_asset


def _graph_payload() -> dict:
    """Graph JSON for the active scenario (falls back to the default AMR stack)."""
    meta = st.session_state.get("current_scenario_meta", {}) or {}
    generator = DynamicGraphGenerator()
    scenario = generator.normalize_scenario(meta.get("data"))
    return generator.export_graph_json(scenario)


def render_soc_dashboard_page():
    """Renders the embedded 3D Robotics SOC & Cyber-Physical Defense Center."""
    meta = st.session_state.get("current_scenario_meta", {}) or {}
    scenario_name = meta.get("name", "Default AMR Navigation Stack")
    payload = _graph_payload()
    stats = payload["stats"]

    st.markdown(f"""
    <div style="margin-bottom: 0.5rem;">
        <h2 style="font-size: 1.4rem; font-weight: 800; color: {UI_THEME['text_primary']}; margin: 0; letter-spacing: -0.02em;">
            🛡️ 3D Robotics SOC &amp; Cyber-Physical Defense Center
        </h2>
        <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.2rem;">
            AMR 3D digital twin · SROS2 cyberattack simulator · live NetworkX computational graph
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Live KPI row, computed from the active analysis / scenario (not hard-coded)
    analysis = st.session_state.get("current_analysis") or {}
    summary = analysis.get("summary", {})
    sec = analysis.get("security_score", {})
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Active scenario", scenario_name[:28] + ("…" if len(scenario_name) > 28 else ""))
    k2.metric("Graph size", f"{stats['total_nodes']} nodes / {stats['total_topics']} topics")
    k3.metric("QoS-incompatible edges", stats["error_edges"],
              delta="needs fix" if stats["error_edges"] else "clean",
              delta_color="inverse" if stats["error_edges"] else "normal")
    k4.metric("Security posture", f"{sec.get('score', '—')}{'%' if sec else ''}",
              delta=f"{summary.get('CRITICAL', 0)} critical" if analysis else "run a scan",
              delta_color="inverse" if summary.get("CRITICAL", 0) else "off")

    try:
        html_code = load_html_asset("soc_dashboard.html", graph_data=payload)
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    # Standalone export is fully self-contained (vendored JS inlined, graph baked in)
    st.download_button(
        label="🌐 Export standalone offline HTML",
        data=html_code,
        file_name="roboguard_soc_dashboard_offline.html",
        mime="text/html",
        key="dl_soc_html",
    )
    components.html(html_code, height=1180, scrolling=True)
