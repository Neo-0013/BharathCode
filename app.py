"""
ROBOGUARD AI — Main Application Entrypoint
Explainable ROS 2 Diagnostics & Cybersecurity Copilot
Official Submission for the BharatCode Build League 2026
"""

import os
import streamlit as st
from config.settings import (
    APP_NAME, APP_VERSION, APP_TAGLINE, TARGET_ROS_DISTRO,
    BHARATCODE_DEFAULT_MODEL, UI_THEME
)
from core.diagnostic_engine import DiagnosticEngine
from core.security_engine import SecurityEngine
from ai.client import BharatCodeClient
from ai.explanation_engine import ExplanationEngine
from ui.styles import inject_custom_styles

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} — Explainable ROS 2 Diagnostics & Cybersecurity",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom High-Fidelity Design Tokens & CSS
inject_custom_styles()

# Initialize Global Session State
if "current_analysis" not in st.session_state:
    st.session_state["current_analysis"] = None
if "current_scenario_meta" not in st.session_state:
    st.session_state["current_scenario_meta"] = {}
if "selected_provider" not in st.session_state:
    st.session_state["selected_provider"] = "ollama"
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = "qwen2.5-coder:3b"
if "force_offline" not in st.session_state:
    st.session_state["force_offline"] = False
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "Command Center"

# Instantiate Backend Engine Singletons
@st.cache_resource
def get_engines():
    diag_engine = DiagnosticEngine()
    sec_engine = SecurityEngine()
    ai_client = BharatCodeClient(
        provider=st.session_state.get("selected_provider", "ollama"),
        model=st.session_state.get("selected_model", "qwen2.5-coder:3b")
    )
    expl_engine = ExplanationEngine(client=ai_client)
    return diag_engine, sec_engine, expl_engine

diagnostic_engine, security_engine, explanation_engine = get_engines()

# Sync active provider credentials from session state
explanation_engine.client.provider = st.session_state.get("selected_provider", "ollama")
explanation_engine.client.model = st.session_state.get("selected_model", "qwen2.5-coder:3b")
if st.session_state.get("selected_provider") == "gemini":
    explanation_engine.client.api_key = st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))
elif st.session_state.get("selected_provider") == "bharatcode":
    explanation_engine.client.api_key = st.session_state.get("bharatcode_api_key", os.getenv("BHARATCODE_API_KEY", ""))
else:
    explanation_engine.client.api_key = "ollama"

# Sidebar Navigation (Linear Ergonomics)
with st.sidebar:
    # Branding
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid {UI_THEME['border_subtle']}; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            <div style="background: linear-gradient(135deg, #0284C7 0%, #00E5FF 100%); width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);">
                🛡️
            </div>
            <div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF; letter-spacing: -0.01em;">{APP_NAME}</div>
                <div style="font-size: 0.7rem; color: {UI_THEME['text_secondary']};">v{APP_VERSION} · {TARGET_ROS_DISTRO}</div>
            </div>
        </div>
        <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.6rem; line-height: 1.35;">
            {APP_TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    nav_options = [
        "Command Center",
        "Diagnostics Workspace",
        "Cybersecurity Center",
        "ROS Graph Explorer",
        "Reports & History",
        "Settings & Connectivity"
    ]

    selected_nav = st.radio(
        "Workspace Navigation",
        nav_options,
        index=nav_options.index(st.session_state["nav_selection"]) if st.session_state["nav_selection"] in nav_options else 0,
        label_visibility="collapsed"
    )
    st.session_state["nav_selection"] = selected_nav

    st.markdown("---")

    # Current Assessment Status Pill
    curr = st.session_state.get("current_analysis")
    if curr:
        crit_count = curr.get("summary", {}).get("CRITICAL", 0)
        sec_score = curr.get("security_score", {}).get("score", 100)
        scenario_name = st.session_state.get("current_scenario_meta", {}).get("name", "Active Session")
        st.markdown(f"""
        <div class="rg-card" style="padding: 0.75rem;">
            <div style="font-size: 0.7rem; text-transform: uppercase; color: {UI_THEME['text_muted']};">Active Session</div>
            <div style="font-weight: 600; font-size: 0.8rem; color: #F1F5F9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 0.2rem;">
                {scenario_name}
            </div>
            <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
                <span class="rg-stat-badge {'badge-red' if crit_count > 0 else 'badge-green'}" style="font-size: 0.65rem;">
                    {crit_count} Critical
                </span>
                <span class="rg-stat-badge badge-cyan" style="font-size: 0.65rem;">
                    {sec_score}% Security
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Bottom Footer
    curr_prov = st.session_state.get("selected_provider", "ollama")
    curr_model = st.session_state.get("selected_model", "qwen2.5-coder:3b")
    prov_label = "Local Ollama" if curr_prov == "ollama" else ("Google Gemini" if curr_prov == "gemini" else "BharatCode Model API")
    st.markdown(f"""
    <div style="font-size: 0.7rem; color: {UI_THEME['text_muted']}; margin-top: 2rem;">
        Active AI Copilot: <b>{prov_label}</b><br>
        <code>{curr_model}</code>
    </div>
    """, unsafe_allow_html=True)

# Page Routing
from ui.pages.overview import render_overview_page
from ui.pages.diagnostics import render_diagnostics_page
from ui.pages.security import render_security_page
from ui.pages.graph_explorer import render_graph_explorer_page
from ui.pages.reports import render_reports_page
from ui.pages.settings import render_settings_page

if st.session_state["nav_selection"] == "Command Center":
    render_overview_page(diagnostic_engine, explanation_engine)
elif st.session_state["nav_selection"] == "Diagnostics Workspace":
    render_diagnostics_page(diagnostic_engine, explanation_engine)
elif st.session_state["nav_selection"] == "Cybersecurity Center":
    render_security_page(diagnostic_engine, security_engine)
elif st.session_state["nav_selection"] == "ROS Graph Explorer":
    render_graph_explorer_page(diagnostic_engine)
elif st.session_state["nav_selection"] == "Reports & History":
    render_reports_page()
elif st.session_state["nav_selection"] == "Settings & Connectivity":
    render_settings_page(explanation_engine)
