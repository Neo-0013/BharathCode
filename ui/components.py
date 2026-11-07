"""
ROBOGUARD AI — UI Components Module
Reusable engineering components: observability stat strips, Linear-styled
finding rows, collapsible detail drawers, and AI Copilot callout panels.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from config.settings import UI_THEME, Severity

def render_header(title: str, subtitle: str, tag: str = "ROS 2 Jazzy Jalisco"):
    """Renders the top application breadcrumb and header."""
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; border-bottom: 1px solid {UI_THEME['border_subtle']}; padding-bottom: 0.75rem;">
        <div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                <span style="font-size: 0.8rem; font-weight: 600; color: {UI_THEME['accent_primary']}; letter-spacing: 0.05em; text-transform: uppercase;">ROBOGUARD AI</span>
                <span style="color: {UI_THEME['text_muted']};">/</span>
                <span style="font-size: 0.8rem; color: {UI_THEME['text_secondary']};">{title}</span>
            </div>
            <h1 style="font-size: 1.65rem; font-weight: 700; margin: 0; color: #FFFFFF; letter-spacing: -0.02em;">{title}</h1>
            <p style="font-size: 0.875rem; color: {UI_THEME['text_secondary']}; margin: 0.25rem 0 0 0;">{subtitle}</p>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; background-color: {UI_THEME['bg_surface']}; border: 1px solid {UI_THEME['border_subtle']}; padding: 0.35rem 0.75rem; border-radius: 9999px;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10B981; box-shadow: 0 0 6px #10B981;"></div>
            <span style="font-size: 0.75rem; font-weight: 500; color: {UI_THEME['text_primary']}; font-family: 'JetBrains Mono', monospace;">{tag}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_stat_strip(stats: Dict[str, Any]):
    """Renders the top observability telemetry strip matching AI Observability style."""
    total = stats.get("total_findings", 0)
    crit = stats.get("critical", 0)
    high = stats.get("high", 0)
    med_low = stats.get("medium", 0) + stats.get("low", 0)
    sec_score = stats.get("security_score", 100)
    sec_tier = stats.get("security_tier", "ASSESSED")

    st.markdown(f"""
    <div class="rg-stat-grid">
        <div class="rg-stat-card">
            <div class="rg-stat-label">Total Findings</div>
            <div class="rg-stat-value">
                {total}
                <span class="rg-stat-badge badge-cyan">Assessed</span>
            </div>
        </div>
        <div class="rg-stat-card">
            <div class="rg-stat-label">Critical Defects</div>
            <div class="rg-stat-value" style="color: {'#EF4444' if crit > 0 else '#10B981'};">
                {crit}
                <span class="rg-stat-badge {'badge-red' if crit > 0 else 'badge-green'}">{'Action Required' if crit > 0 else 'Zero Critical'}</span>
            </div>
        </div>
        <div class="rg-stat-card">
            <div class="rg-stat-label">High Severity Issues</div>
            <div class="rg-stat-value" style="color: {'#F97316' if high > 0 else '#10B981'};">
                {high}
                <span class="rg-stat-badge {'badge-orange' if high > 0 else 'badge-green'}">{'Needs Review' if high > 0 else 'Zero High'}</span>
            </div>
        </div>
        <div class="rg-stat-card">
            <div class="rg-stat-label">Medium & Low Warnings</div>
            <div class="rg-stat-value">
                {med_low}
                <span class="rg-stat-badge badge-cyan">Monitored</span>
            </div>
        </div>
        <div class="rg-stat-card">
            <div class="rg-stat-label">Security Posture Score</div>
            <div class="rg-stat-value" style="color: {'#10B981' if sec_score >= 80 else ('#F59E0B' if sec_score >= 60 else '#EF4444')};">
                {sec_score}%
                <span class="rg-stat-badge {'badge-green' if sec_score >= 80 else 'badge-orange'}">{sec_tier}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_severity_badge(severity: str) -> str:
    """Returns HTML for a styled severity pill."""
    sev = severity.upper()
    if sev == "CRITICAL":
        return '<span style="font-size: 0.7rem; font-weight: 700; color: #EF4444; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">CRITICAL</span>'
    elif sev == "HIGH":
        return '<span style="font-size: 0.7rem; font-weight: 700; color: #F97316; background: rgba(249, 115, 22, 0.15); border: 1px solid rgba(249, 115, 22, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">HIGH</span>'
    elif sev == "MEDIUM":
        return '<span style="font-size: 0.7rem; font-weight: 700; color: #F59E0B; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">MEDIUM</span>'
    elif sev == "LOW":
        return '<span style="font-size: 0.7rem; font-weight: 700; color: #10B981; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">LOW</span>'
    else:
        return '<span style="font-size: 0.7rem; font-weight: 700; color: #38BDF8; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); padding: 0.15rem 0.5rem; border-radius: 4px;">INFO</span>'

def render_finding_detail(finding: Dict[str, Any]):
    """Renders detailed finding breakdown inside an expander or drawer."""
    sev = finding.get("severity", "INFO")
    cat = finding.get("category", "General")
    fid = finding.get("id", "N/A")
    title = finding.get("title", "Finding")
    evidence = finding.get("evidence", "")
    rc = finding.get("root_cause") or finding.get("explanation", "")
    impact = finding.get("impact", "")
    mitigation = finding.get("mitigation", "")
    troubleshooting = finding.get("troubleshooting", [])
    validation_cmds = finding.get("validation_commands", [])

    st.markdown(f"### `{fid}` — {title}")
    st.markdown(f"**Severity:** {render_severity_badge(sev)} &nbsp;|&nbsp; **Category:** `{cat}` &nbsp;|&nbsp; **Confidence:** `{finding.get('status', 'Confirmed')}`", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Evidence snippet
    if evidence:
        st.markdown("**Empirical Evidence Extracted:**")
        st.code(evidence, language="text")

    # Probable Root Cause / Explanation
    if rc:
        st.markdown("**Root Cause Analysis:**")
        st.info(rc)

    # Impact if present
    if impact:
        st.markdown("**Operational & Security Impact:**")
        st.warning(impact)

    # Troubleshooting steps
    if troubleshooting:
        st.markdown("**Deterministic Remediation Steps:**")
        for i, step in enumerate(troubleshooting, 1):
            st.markdown(f"{i}. {step}")

    # Mitigation text
    if mitigation:
        st.markdown("**Security Hardening Procedure:**")
        st.markdown(mitigation)

    # Validation commands
    if validation_cmds:
        st.markdown("**Verification Commands (ROS 2 CLI):**")
        st.code("\n".join(validation_cmds), language="bash")
