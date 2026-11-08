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
from ui.components import render_live_floating_copilot

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

# Robust Query Parameter & Default Landing Resolution
if "nav" in st.query_params:
    qp = str(st.query_params["nav"]).lower()
    if "soc" in qp:
        st.session_state["nav_selection"] = "🛡️ 3D Robotics SOC"
    elif "story" in qp or "hero" in qp:
        st.session_state["nav_selection"] = "📖 Mission Story & 3D Twin"
elif "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "🛡️ 3D Robotics SOC"

if "active_attack_event" not in st.session_state:
    st.session_state["active_attack_event"] = None

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

# Navigation Menu Options (Clean, consistent iconography & Tremor Light System)
nav_options = [
    "📖 Mission Story & 3D Twin",
    "🛡️ 3D Robotics SOC",
    "📊 Command Center",
    "🔬 Diagnostics Workspace",
    "🔐 Cybersecurity Center",
    "🕸️ ROS Graph Explorer",
    "📋 Reports & History",
    "⚙️ Settings & Connectivity"
]

# Robust Nav Normalization: match by exact string or keyword
current_raw_nav = st.session_state.get("nav_selection", nav_options[0])
active_nav_index = 0
for idx, opt in enumerate(nav_options):
    if current_raw_nav == opt or current_raw_nav in opt or opt in current_raw_nav:
        active_nav_index = idx
        break

# Sidebar Navigation (Linear Ergonomics & Tremor Classic Light System)
with st.sidebar:
    # Branding Header
    st.markdown(f"""
    <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 0.65rem;">
            <div style="background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%); width: 38px; height: 38px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);">
                🛡️
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.12rem; color: #0F172A; letter-spacing: -0.02em;">{APP_NAME}</div>
                <div style="font-size: 0.72rem; color: #059669; font-weight: 700; display: flex; align-items: center; gap: 0.35rem; margin-top: 1px;">
                    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #059669; box-shadow: 0 0 6px #059669;"></span>
                    v{APP_VERSION} · {TARGET_ROS_DISTRO}
                </div>
            </div>
        </div>
        <div style="font-size: 0.76rem; color: #475569; margin-top: 0.65rem; line-height: 1.45;">
            {APP_TAGLINE}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Section Header
    st.markdown("""
    <div style="font-size: 0.68rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.06em; color: #64748B; margin-bottom: 0.4rem; padding-left: 0.2rem;">
        Workspaces &amp; Digital Twin
    </div>
    """, unsafe_allow_html=True)

    selected_nav = st.radio(
        "Workspace Navigation",
        nav_options,
        index=active_nav_index,
        label_visibility="collapsed"
    )
    st.session_state["nav_selection"] = selected_nav

    hero_url = os.getenv("ROBOGUARD_HERO_URL", "http://localhost:8000")
    st.markdown(f"""
    <a href="{hero_url}" target="_blank" style="text-decoration: none;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.75rem; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; margin-top: 0.45rem; transition: all 0.2s ease;">
            <div style="display: flex; align-items: center; gap: 0.45rem;">
                <span style="font-size: 0.85rem;">🌐</span>
                <span style="font-size: 0.73rem; font-weight: 700; color: #1D4ED8;">Fullscreen Hero Page</span>
            </div>
            <span style="font-size: 0.7rem; color: #2563EB; font-family: monospace;">:8000 ↗</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Current Assessment Status Card (Tremor-style Elevated Card with Progress Bar)
    curr = st.session_state.get("current_analysis")
    crit_count = curr.get("summary", {}).get("CRITICAL", 0) if curr else 0
    sec_score = curr.get("security_score", {}).get("score", 100) if curr else 95
    scenario_name = st.session_state.get("current_scenario_meta", {}).get("name", "Nominal Fleet Operation")

    bar_color = "#059669" if sec_score >= 80 else ("#D97706" if sec_score >= 50 else "#DC2626")

    st.markdown(f"""
    <div class="rg-card" style="padding: 0.85rem; margin-top: 0.25rem; background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 0.68rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.05em; color: #64748B;">Active Session</div>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: {bar_color};">{sec_score}% SECURE</span>
        </div>
        <div style="font-weight: 700; font-size: 0.85rem; color: #0F172A; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 0.25rem;">
            {scenario_name}
        </div>
        <div class="tremor-progress-track">
            <div class="tremor-progress-fill" style="width: {sec_score}%; background: {bar_color};"></div>
        </div>
        <div style="display: flex; gap: 0.45rem; margin-top: 0.65rem;">
            <span class="rg-stat-badge {'badge-red' if crit_count > 0 else 'badge-green'}" style="font-size: 0.65rem;">
                {crit_count} Critical Defect{'s' if crit_count != 1 else ''}
            </span>
            <span class="rg-stat-badge badge-cyan" style="font-size: 0.65rem;">
                🔒 SROS2 Ready
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active Copilot Telemetry Footer
    curr_prov = st.session_state.get("selected_provider", "ollama")
    curr_model = st.session_state.get("selected_model", "qwen2.5-coder:3b")
    prov_label = "Local Ollama" if curr_prov == "ollama" else ("Google Gemini" if curr_prov == "gemini" else "BharatCode Model API")
    st.markdown(f"""
    <div style="font-size: 0.72rem; color: #64748B; margin-top: 1.5rem; padding: 0.75rem; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
            <span style="font-weight: 700; color: #0F172A;">Copilot: <b>{prov_label}</b></span>
            <span style="color: #059669; font-weight: 700;">14ms</span>
        </div>
        <code style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #2563EB;">{curr_model}</code>
    </div>
    """, unsafe_allow_html=True)

# Page Routing with Substring Safety
from ui.pages.story_hero import render_story_hero_page
from ui.pages.soc_dashboard import render_soc_dashboard_page
from ui.pages.overview import render_overview_page
from ui.pages.diagnostics import render_diagnostics_page
from ui.pages.security import render_security_page
from ui.pages.graph_explorer import render_graph_explorer_page
from ui.pages.reports import render_reports_page
from ui.pages.settings import render_settings_page

current_selection = st.session_state.get("nav_selection", nav_options[0])

if "Mission Story" in current_selection:
    render_story_hero_page()
elif "3D Robotics SOC" in current_selection:
    render_soc_dashboard_page()
elif "Command Center" in current_selection:
    render_overview_page(diagnostic_engine, explanation_engine)
elif "Diagnostics Workspace" in current_selection:
    render_diagnostics_page(diagnostic_engine, explanation_engine)
elif "Cybersecurity Center" in current_selection:
    render_security_page(diagnostic_engine, security_engine)
elif "ROS Graph Explorer" in current_selection:
    render_graph_explorer_page(diagnostic_engine)
elif "Reports" in current_selection:
    render_reports_page()
elif "Settings" in current_selection:
    render_settings_page(explanation_engine)
else:
    render_story_hero_page()

# Persistent Live Floating AI Sentinel Widget (Reactive Attack Pop-Up & Hover Assistance)
render_live_floating_copilot(explanation_engine)
