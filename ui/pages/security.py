"""
ROBOGUARD AI — Cybersecurity Center Page
Audits ROS 2 Jazzy SROS2 enclaves, DDS security profiles, environment variable
trust boundaries, and generates defensive robotics hardening playbooks.
"""

import streamlit as st
from config.settings import UI_THEME, Severity
from ui.components import render_header, render_severity_badge, render_finding_detail

def render_security_page(diagnostic_engine, security_engine):
    render_header("Cybersecurity Center", "Defensive SROS2 security posture audit, DDS trust boundaries, and threat mitigation.")

    current_analysis = st.session_state.get("current_analysis", None)
    
    # Extract security findings
    sec_findings = []
    if current_analysis:
        sec_findings = [f for f in current_analysis.get("findings", []) if f.get("category") == "Robotics Cybersecurity & SROS2"]

    # Calculate posture score
    posture = security_engine.calculate_posture_score(sec_findings)

    # Top Security Score Overview
    col_score, col_meta = st.columns([1.2, 1.8])

    with col_score:
        st.markdown(f"""
        <div class="rg-card" style="text-align: center; border-color: {posture['color']};">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: {UI_THEME['text_secondary']};">Defensive Posture Score</div>
            <div style="font-size: 3rem; font-weight: 800; color: {posture['color']}; margin: 0.5rem 0;">
                {posture['score']}%
            </div>
            <div style="font-size: 0.85rem; font-weight: 700; color: {posture['color']}; background: rgba(255,255,255,0.05); padding: 0.25rem 0.75rem; border-radius: 9999px; display: inline-block;">
                {posture['risk_tier']}
            </div>
            <div style="font-size: 0.75rem; color: {UI_THEME['text_muted']}; margin-top: 0.75rem;">
                {posture['total_findings']} security issues detected
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_meta:
        st.markdown(f"""
        <div class="rg-card">
            <div style="font-size: 0.85rem; font-weight: 600; color: #F8FAFC; margin-bottom: 0.5rem;">Transparent Scoring Methodology</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; line-height: 1.5;">
                {posture['transparency_note']}
            </div>
            <div style="margin-top: 0.75rem; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: {UI_THEME['text_muted']};">
                Penalties: Critical (-25) | High (-15) | Medium (-8) | Total Deduction: -{posture['deductions_applied']} pts
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Defensive Cybersecurity Findings")
    if not sec_findings:
        st.info("No security defects detected in the active scenario, or no cybersecurity configuration has been evaluated yet.")
    else:
        for idx, f in enumerate(sec_findings):
            fid = f.get("id", f"ROBO-SEC-{idx+1:03d}")
            title = f.get("title", "Security Finding")
            sev = f.get("severity", "HIGH")
            with st.expander(f"[{fid}] {title} — {sev}", expanded=idx == 0):
                render_finding_detail(f)

    # Threat Model Summary (STRIDE for Robotics)
    st.markdown("---")
    st.markdown("### Robotics Threat Model (STRIDE for ROS 2 Jazzy)")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"""
        <div class="rg-card">
            <div style="font-weight: 600; color: #EF4444; font-size: 0.85rem;">1. Spoofing & Actuator Injection</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                Without SROS2 participant authentication, rogue DDS nodes can publish unauthorized Twist commands to <code>/cmd_vel</code>, hijacking robot locomotion.
            </div>
        </div>
        <div class="rg-card">
            <div style="font-weight: 600; color: #F97316; font-size: 0.85rem;">2. Tampering (Sensor Data Falsification)</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                Unauthenticated UDP RTPS packets can be spoofed or replayed to fake LiDAR distance readings, blinding obstacle avoidance algorithms.
            </div>
        </div>
        <div class="rg-card">
            <div style="font-weight: 600; color: #F59E0B; font-size: 0.85rem;">3. Repudiation & Auditability</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                Standard ROS 2 rosout logs do not contain cryptographic nonces or digital signatures, preventing verifiable provenance during incident investigation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown(f"""
        <div class="rg-card">
            <div style="font-weight: 600; color: #00E5FF; font-size: 0.85rem;">4. Information Disclosure (Passive Sniffing)</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                Plaintext DDS multicast broadcasts camera streams, SLAM maps, and odometry across the entire local Wi-Fi subnet.
            </div>
        </div>
        <div class="rg-card">
            <div style="font-weight: 600; color: #818CF8; font-size: 0.85rem;">5. Denial of Service (DDS Multicast Flood)</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                DDS SPDP discovery amplification attacks can saturate the robot's onboard Ethernet controller and starve real-time control loops.
            </div>
        </div>
        <div class="rg-card">
            <div style="font-weight: 600; color: #10B981; font-size: 0.85rem;">6. Elevation of Privilege (Wildcard Access)</div>
            <div style="font-size: 0.8rem; color: {UI_THEME['text_secondary']}; margin-top: 0.35rem;">
                Permissions XML policies with wildcard topic scopes grant untrusted utility nodes write access to safety-critical emergency stop topics.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Hardening Runbook
    st.markdown("### SROS2 Hardening Playbook")
    st.code("""# 1. Create SROS2 Keystore
ros2 security create_keystore ~/sros2_keystore

# 2. Generate signed X.509 enclaves for active nodes
ros2 security create_enclave ~/sros2_keystore /teleop_node
ros2 security create_enclave ~/sros2_keystore /motor_controller

# 3. Export required ROS 2 Jazzy security environment variables
export ROS_SECURITY_ENABLE=true
export ROS_SECURITY_STRATEGY=Enforce
export ROS_SECURITY_KEYSTORE=~/sros2_keystore
export ROS_DOMAIN_ID=42
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST""", language="bash")
