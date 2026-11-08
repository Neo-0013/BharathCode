"""
ROBOGUARD AI — Reports & Export Page
Generates and downloads publication-grade Markdown and PDF diagnostic and cybersecurity reports.
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timezone
from config.settings import REPORTS_DIR, TARGET_ROS_DISTRO, UI_THEME
from core.report_generator import ReportGenerator
from ui.components import render_header

def render_reports_page():
    render_header("Reports & Export", "Export audit reports in Markdown and PDF formats with verified command runbooks.")

    current_analysis = st.session_state.get("current_analysis", None)
    scenario_meta = st.session_state.get("current_scenario_meta", {})

    if not current_analysis or not current_analysis.get("findings"):
        st.markdown(f"""
        <div class="rg-card" style="text-align: center; padding: 2.5rem 1rem;">
            <div style="font-size: 1.05rem; font-weight: 600; color: {UI_THEME['text_primary']}; margin-bottom: 0.5rem;">No Active Report to Generate</div>
            <div style="font-size: 0.85rem; color: {UI_THEME['text_secondary']}; max-width: 500px; margin: 0 auto;">
                Perform an analysis or load a demonstration scenario first before generating exportable engineering reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    report_gen = ReportGenerator()
    
    # Custom metadata input
    with st.expander("📝 Report Metadata & System Profile", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            system_name = st.text_input("Robot / System Identifier", scenario_meta.get("name", "Autonomous Mobile Robot #04"))
        with col2:
            operator_name = st.text_input("Lead Robotics Engineer / Auditor", "Antigravity Senior Product Engineer")

    meta = {
        "system_name": system_name,
        "operator": operator_name,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # Generate Markdown content
    md_content = report_gen.generate_markdown(current_analysis, meta)

    # Export Buttons
    col_dl_md, col_dl_pdf, col_dl_json = st.columns(3)

    with col_dl_md:
        st.download_button(
            label="📄 Download Markdown (.md)",
            data=md_content,
            file_name=f"roboguard_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_dl_pdf:
        # Generate temporary PDF
        pdf_filename = f"roboguard_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = REPORTS_DIR / pdf_filename
        report_gen.generate_pdf(current_analysis, pdf_path, meta)

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="📑 Download PDF Report (.pdf)",
            data=pdf_bytes,
            file_name=pdf_filename,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

    with col_dl_json:
        findings_json = json.dumps(current_analysis.get("findings", []), indent=2)
        st.download_button(
            label="💾 Export Findings (.json)",
            data=findings_json,
            file_name=f"roboguard_findings_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### Report Live Preview")
    st.markdown(md_content)
