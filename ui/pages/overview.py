"""
ROBOGUARD AI — Overview & Command Center Page
Executive monitoring dashboard featuring telemetry summary strips,
AI Copilot insight banners, demonstration scenario launcher, and quick actions.
"""

import streamlit as st
import json
from pathlib import Path
from config.settings import DEMO_DIR, UI_THEME, APP_NAME, APP_TAGLINE
from ui.components import render_header, render_stat_strip, render_severity_badge

def render_overview_page(diagnostic_engine, explanation_engine):
    render_header("Command Center", "Real-time robotics diagnostic health, QoS telemetry, and cybersecurity posture.")

    # Get current analysis state from session_state
    current_analysis = st.session_state.get("current_analysis", None)
    
    # Default stats if nothing loaded yet
    if current_analysis:
        summary = current_analysis.get("summary", {})
        sec_score = current_analysis.get("security_score", {})
        stats = {
            "total_findings": current_analysis.get("total_findings", 0),
            "critical": summary.get("CRITICAL", 0),
            "high": summary.get("HIGH", 0),
            "medium": summary.get("MEDIUM", 0),
            "low": summary.get("LOW", 0),
            "security_score": sec_score.get("score", 100),
            "security_tier": sec_score.get("risk_tier", "ASSESSED")
        }
    else:
        stats = {
            "total_findings": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "security_score": 100,
            "security_tier": "READY FOR ANALYSIS"
        }

    # Render Telemetry Strip
    render_stat_strip(stats)

    # AI Copilot Insight Card (Style matching reference Image 1)
    st.markdown(f"""
    <div class="rg-ai-banner">
        <div class="rg-ai-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{UI_THEME['accent_primary']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
            </svg>
            <span>AI Diagnostic Copilot & Observability Intelligence</span>
        </div>
        <div style="font-size: 0.875rem; color: #CBD5E1; line-height: 1.5;">
            ROBOGUARD AI integrates formal ROS 2 Jazzy deterministic rules with the 
            <b>BharatCode Model API</b>. All AI-generated root cause analyses and troubleshooting 
            steps are strictly grounded in empirical log traces, QoS profiles, and coordinate transform trees.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.6, 1.0])

    with col1:
        st.markdown("### Interactive Demonstration Scenarios")
        st.caption("Load pre-configured, evidence-rich synthetic scenarios for robotics judges and developers.")

        scenarios = [
            ("SCENARIO-01", "Missing ROS 2 Topic & Unconsumed Actuation", "scenario_1_missing_topic.json", "Nav2 AGV /cmd_vel missing subscriber and /scan sensor stall."),
            ("SCENARIO-02", "Nav2 & Perception QoS Incompatibility", "scenario_2_qos_mismatch.json", "Reliability and Durability DDS mismatches causing dropped costmap messages."),
            ("SCENARIO-03", "SLAM Disconnected TF2 Transform Tree", "scenario_3_tf_disconnected.json", "Disjoint coordinate trees with missing map->odom localization link."),
            ("SCENARIO-04", "Colcon Workspace Build & Launch Failure", "scenario_4_build_launch_failure.json", "Missing Python dependencies and CMake ament package errors."),
            ("SCENARIO-05", "Insecure Robotic Fleet DDS Multicast", "scenario_5_insecure_robot.json", "Unencrypted SROS2 on Domain 0 with permissive wildcard governance.")
        ]

        for sid, name, filename, desc in scenarios:
            with st.container():
                st.markdown(f"""
                <div style="background-color: {UI_THEME['bg_surface']}; border: 1px solid {UI_THEME['border_subtle']}; border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.65rem;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: {UI_THEME['accent_primary']};">{sid}</span>
                        <span style="font-size: 0.7rem; color: {UI_THEME['text_muted']};">Synthetic Ground Truth</span>
                    </div>
                    <div style="font-weight: 600; font-size: 0.95rem; color: #F8FAFC; margin-top: 0.2rem;">{name}</div>
                    <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.25rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Load & Analyze {sid}", key=f"btn_load_{sid}"):
                    filepath = DEMO_DIR / filename
                    if filepath.exists():
                        with open(filepath, "r", encoding="utf-8") as f:
                            demo_data = json.load(f)
                            res = diagnostic_engine.analyze_structured_scenario(demo_data)
                            st.session_state["current_analysis"] = res
                            st.session_state["current_scenario_meta"] = {
                                "id": sid,
                                "name": name,
                                "filename": filename,
                                "data": demo_data
                            }
                            st.success(f"Loaded and analyzed {name}! Found {res['total_findings']} issues.")
                            st.rerun()

    with col2:
        st.markdown("### System Quick Actions")
        
        with st.container():
            st.markdown(f"""
            <div class="rg-card">
                <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: {UI_THEME['text_secondary']}; margin-bottom: 0.5rem;">Workspace Navigation</div>
                <div style="font-size: 0.825rem; color: {UI_THEME['text_muted']}; margin-bottom: 1rem;">
                    Jump directly to diagnostic workspaces, cybersecurity audit tools, or the interactive graph explorer.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Open Diagnostics Workspace", use_container_width=True, type="primary"):
                st.session_state["nav_selection"] = "Diagnostics Workspace"
                st.rerun()

            if st.button("Inspect Cybersecurity Posture", use_container_width=True):
                st.session_state["nav_selection"] = "Cybersecurity Center"
                st.rerun()

            if st.button("Explore ROS Communication Graph", use_container_width=True):
                st.session_state["nav_selection"] = "ROS Graph Explorer"
                st.rerun()

            if st.button("Generate & Download Reports", use_container_width=True):
                st.session_state["nav_selection"] = "Reports & History"
                st.rerun()

        # Target Environment Card
        st.markdown(f"""
        <div class="rg-card" style="margin-top: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: {UI_THEME['text_secondary']};">Target Environment</div>
            <div style="margin-top: 0.5rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #E2E8F0;">
                <div>Distribution: <b>ROS 2 Jazzy Jalisco</b></div>
                <div>Middleware: <b>FastDDS / CycloneDDS</b></div>
                <div>DDS Security: <b>SROS2 (X.509 + AES-GCM)</b></div>
                <div>Engine Mode: <b>Dual Deterministic + AI</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
