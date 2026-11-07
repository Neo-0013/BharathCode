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
    BHARATCODE_AVAILABLE_MODELS, TARGET_ROS_DISTRO, UI_THEME, APP_VERSION,
    AI_PROVIDERS
)
from ai.client import BharatCodeClient
from ui.components import render_header

def render_settings_page(explanation_engine):
    render_header("Settings & Connectivity", "Configure AI Copilot providers (Local Ollama, Gemini API, BharatCode), test connectivity, and audit ROS 2 Jazzy environment.")

    tab_api, tab_env, tab_privacy = st.tabs(["🤖 AI Model Providers", "⚙️ ROS 2 Jazzy Host Environment", "🔒 Privacy & Security"])

    with tab_api:
        st.markdown("### AI Copilot Engine Provider")
        st.caption("Select your preferred AI engine: Run 100% free locally with Ollama, connect via Google Gemini, or use the official BharatCode API.")

        # Provider Selection
        prov_keys = ["ollama", "gemini", "bharatcode"]
        prov_labels = [
            "🟢 Local Ollama (100% Free / Localhost — Recommended)",
            "🔷 Google Gemini API (Generous Free Tier)",
            "🇮🇳 BharatCode Model API (Competition Official)"
        ]

        current_prov = st.session_state.get("selected_provider", "ollama")
        prov_idx = prov_keys.index(current_prov) if current_prov in prov_keys else 0

        selected_prov_label = st.radio(
            "Select AI Provider",
            prov_labels,
            index=prov_idx,
            label_visibility="collapsed"
        )
        selected_prov = prov_keys[prov_labels.index(selected_prov_label)]
        st.session_state["selected_provider"] = selected_prov
        explanation_engine.client.provider = selected_prov

        prov_info = AI_PROVIDERS[selected_prov]
        available_models = prov_info.get("models", [])
        model_ids = [m["id"] for m in available_models]
        model_names = [f"{m['name']} ({m.get('context_window', '32k')})" for m in available_models]

        st.markdown("<br>", unsafe_allow_html=True)
        col_url, col_model = st.columns([1.2, 1.8])

        with col_url:
            api_base = st.text_input("Endpoint Base URL", value=prov_info["base_url"])
            explanation_engine.client.base_url = api_base

        with col_model:
            current_model = st.session_state.get("selected_model", prov_info["default_model"])
            current_model_idx = model_ids.index(current_model) if current_model in model_ids else 0
            
            selected_model_idx = st.selectbox(
                "Model Identifier",
                range(len(model_ids)),
                format_func=lambda i: model_names[i],
                index=current_model_idx
            )
            selected_model_id = model_ids[selected_model_idx]
            st.session_state["selected_model"] = selected_model_id
            explanation_engine.client.model = selected_model_id

        # API Key Input (if required)
        api_key = ""
        if prov_info.get("requires_key", True):
            if selected_prov == "gemini":
                saved_key = st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))
                api_key = st.text_input(
                    "Google Gemini API Key",
                    value=saved_key,
                    type="password",
                    placeholder="AIzaSy...",
                    help="Get a free Gemini API key from Google AI Studio: https://aistudio.google.com/app/apikey"
                )
                if api_key != saved_key:
                    st.session_state["gemini_api_key"] = api_key
                explanation_engine.client.api_key = api_key

                st.caption("👉 Need a free Gemini API key? [Get one in 10 seconds at Google AI Studio](https://aistudio.google.com/app/apikey)")

            elif selected_prov == "bharatcode":
                saved_key = st.session_state.get("bharatcode_api_key", os.getenv("BHARATCODE_API_KEY", ""))
                api_key = st.text_input(
                    "BharatCode API Key (Bearer Token)",
                    value=saved_key,
                    type="password",
                    placeholder="Enter your BharatCode API key...",
                    help="From bharatcode.ai platform"
                )
                if api_key != saved_key:
                    st.session_state["bharatcode_api_key"] = api_key
                explanation_engine.client.api_key = api_key
        else:
            api_key = "ollama"
            explanation_engine.client.api_key = "ollama"
            st.info("💡 **Local Ollama detected at localhost:11434.** Zero API key required, zero external network traffic, zero payment errors.")

        col_test, col_mode = st.columns([1.0, 1.2])

        with col_test:
            if st.button("🧪 Test API Connection", type="primary"):
                client = BharatCodeClient(
                    api_key=api_key,
                    base_url=api_base,
                    model=selected_model_id,
                    provider=selected_prov
                )
                with st.spinner(f"Testing connectivity to {prov_info['name']}..."):
                    res = client.test_connection()
                    if res["success"]:
                        st.success(f"✅ {res['message']}")
                    elif res.get("status_code") == 402 or res.get("is_payment_required"):
                        st.warning(f"⚠️ {res['message']}")
                        st.markdown(f"""
                        <div class="rg-card" style="border-color: #F59E0B; margin-top: 0.75rem;">
                            <div style="font-weight: 600; color: #F59E0B; font-size: 0.85rem;">🎓 BharatCode Plan & Student Tier Guidance</div>
                            <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 0.4rem; line-height: 1.45;">
                                BharatCode API access requires an active plan or student verification:
                                <ul>
                                    <li><b>Student Free Tier:</b> Students with a verified college email (<code>.edu</code> or <code>.ac.in</code>) get <b>10M free tokens</b> on <b>Qwen 3.8 27B</b>. Select <code>qwen-3.8-27b</code> above!</li>
                                    <li><b>Switch to Local Ollama:</b> Select <b>Local Ollama</b> above to run 100% free on your local machine with pre-installed <code>qwen2.5-coder:3b</code>!</li>
                                    <li><b>Switch to Gemini API:</b> Select <b>Google Gemini API</b> for 15 RPM free cloud inference.</li>
                                </ul>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
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
