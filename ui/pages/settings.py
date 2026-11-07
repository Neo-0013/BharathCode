"""
ROBOGUARD AI — Settings & Environment Diagnostics Page
Configures the official BharatCode Model API credentials, tests live connectivity,
toggles offline deterministic mode, and verifies ROS 2 Jazzy host environment.
"""

import os
import sys
import streamlit as st
from config.settings import (
    BHARATCODE_API_BASE, BHARATCODE_DEFAULT_MODEL,
    BHARATCODE_AVAILABLE_MODELS, TARGET_ROS_DISTRO, UI_THEME, APP_VERSION
)
from ai.client import BharatCodeClient
from ui.components import render_header

def render_settings_page(explanation_engine):
    render_header("Settings & Connectivity", "Configure BharatCode API credentials, test model endpoints, and audit host ROS 2 environment.")

    tab_api, tab_env, tab_privacy = st.tabs(["🤖 BharatCode AI Model API", "⚙️ ROS 2 Jazzy Host Environment", "🔒 Privacy & Security"])

    with tab_api:
        st.markdown("### BharatCode Model API Credentials")
        st.caption("Official model API endpoint for the BharatCode Build League 2026 hackathon.")

        # API Base
        api_base = st.text_input("API Base URL", value=BHARATCODE_API_BASE, disabled=True)

        # Model Selector
        model_options = [m["id"] for m in BHARATCODE_AVAILABLE_MODELS]
        model_names = [f"{m['name']} — {m['context_window']} context" for m in BHARATCODE_AVAILABLE_MODELS]
        
        current_model = st.session_state.get("selected_model", BHARATCODE_DEFAULT_MODEL)
        current_idx = model_options.index(current_model) if current_model in model_options else 0

        selected_idx = st.selectbox(
            "Target AI Model",
            range(len(model_options)),
            format_func=lambda i: model_names[i],
            index=current_idx
        )
        selected_model_id = model_options[selected_idx]
        st.session_state["selected_model"] = selected_model_id
        explanation_engine.client.model = selected_model_id

        # API Key
        current_key = st.session_state.get("bharatcode_api_key", os.getenv("BHARATCODE_API_KEY", ""))
        api_key = st.text_input(
            "BharatCode API Key (Bearer Token)",
            value=current_key,
            type="password",
            placeholder="Enter your BharatCode API key...",
            help="Stored only in session memory or read from BHARATCODE_API_KEY environment variable."
        )

        if api_key != current_key:
            st.session_state["bharatcode_api_key"] = api_key
            explanation_engine.client.api_key = api_key

        col_test, col_mode = st.columns([1.0, 1.2])

        with col_test:
            if st.button("🧪 Test API Connection", type="primary"):
                client = BharatCodeClient(api_key=api_key, model=selected_model_id)
                with st.spinner("Pinging BharatCode model endpoint..."):
                    res = client.test_connection()
                    if res["success"]:
                        st.success(f"✅ {res['message']}")
                    else:
                        st.error(f"❌ {res['message']}")

        with col_mode:
            offline_mode = st.checkbox(
                "Enforce Offline Diagnostic Mode",
                value=st.session_state.get("force_offline", False),
                help="When enabled, ROBOGUARD AI uses 100% deterministic local rule synthesis without calling cloud APIs."
            )
            st.session_state["force_offline"] = offline_mode

    with tab_env:
        st.markdown("### Host Robotics Environment Diagnostics")
        
        ros_distro = os.getenv("ROS_DISTRO", "Not Sourced")
        ros_path = os.getenv("AMENT_PREFIX_PATH", "None")
        python_ver = sys.version.split()[0]
        domain_id = os.getenv("ROS_DOMAIN_ID", "0 (Default)")
        sec_enable = os.getenv("ROS_SECURITY_ENABLE", "false")

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.markdown(f"""
            <div class="rg-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {UI_THEME['text_secondary']};">ROS 2 Distribution</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #10B981; margin-top: 0.25rem;">{ros_distro.upper()}</div>
                <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.5rem;">Target: {TARGET_ROS_DISTRO}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="rg-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {UI_THEME['text_secondary']};">Python Runtime</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #38BDF8; margin-top: 0.25rem;">{python_ver}</div>
                <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.5rem;">Executable: {sys.executable}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_e2:
            st.markdown(f"""
            <div class="rg-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {UI_THEME['text_secondary']};">DDS Network Domain ID</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #F59E0B; margin-top: 0.25rem;">{domain_id}</div>
                <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.5rem;">Multicast Simple Participant Discovery</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="rg-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; color: {UI_THEME['text_secondary']};">SROS2 Hardware Protection</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: {'#10B981' if sec_enable.lower() in ['true', '1'] else '#EF4444'}; margin-top: 0.25rem;">
                    {'ENABLED' if sec_enable.lower() in ['true', '1'] else 'DISABLED'}
                </div>
                <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.5rem;">ROS_SECURITY_ENABLE={sec_enable}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_privacy:
        st.markdown("### Privacy, Safety & Security Compliance")
        st.markdown(f"""
        - **Local Deterministic Processing:** All log parsing, QoS compatibility matrices, TF2 tree validation, and DDS security audits are computed entirely within your local execution environment.
        - **Zero Secret Exposure:** ROBOGUARD AI never commits, logs, or prints API keys or credentials.
        - **Human Oversight in AI Copilot Actions:** Recommended terminal commands are strictly formatted for human review; ROBOGUARD AI never executes arbitrary commands directly on the host or connected robot.
        - **No Passive Data Transmission:** External requests to the BharatCode API are initiated only when the user explicitly triggers an AI explanation request.
        """)
