"""
ROBOGUARD AI — Diagnostics Workspace Page
Primary working environment for uploading logs, pasting terminal output,
inspecting deterministic findings, and triggering grounded AI Copilot runbooks.
"""

import streamlit as st
import json
from config.settings import UI_THEME, Severity, DiagnosticCategory
from ui.components import render_header, render_severity_badge, render_finding_detail

def render_diagnostics_page(diagnostic_engine, explanation_engine):
    render_header("Diagnostics Workspace", "Investigate software failures, QoS incompatibilities, and coordinate frame errors.")

    # Input Section
    with st.expander("📥 Ingest ROS 2 Logs & Configuration Data", expanded=st.session_state.get("current_analysis") is None):
        tab_upload, tab_paste = st.tabs(["📁 Upload File (.log, .txt, .json, .yaml, .xml)", "📋 Paste Terminal / Console Output"])

        with tab_upload:
            uploaded_file = st.file_uploader(
                "Upload a ROS 2 log or diagnostic export file",
                type=["log", "txt", "json", "yaml", "yml", "xml"],
                help="Accepts raw ROS 2 console logs, JSON topic dumps, or DDS security XML files."
            )
            if uploaded_file is not None:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
                if st.button("Run Diagnostic Analysis on File", type="primary"):
                    with st.spinner("Executing deterministic diagnostic pipeline..."):
                        res = diagnostic_engine.parse_input_auto(content, uploaded_file.name)
                        st.session_state["current_analysis"] = res
                        st.session_state["current_scenario_meta"] = {
                            "name": uploaded_file.name,
                            "type": "Uploaded File"
                        }
                    st.success(f"Analysis complete! Detected {res['total_findings']} findings.")
                    st.rerun()

        with tab_paste:
            pasted_log = st.text_area(
                "Paste raw ROS 2 console log or Colcon build trace",
                height=160,
                placeholder="[ERROR] [1715420102.123] [amcl]: tf2.LookupException: \"base_link\" passed to lookupTransform argument target_frame does not exist..."
            )
            if st.button("Analyze Pasted Terminal Log", type="primary"):
                if pasted_log.strip():
                    with st.spinner("Analyzing log traces..."):
                        res = diagnostic_engine.parse_input_auto(pasted_log, "pasted_terminal.log")
                        st.session_state["current_analysis"] = res
                        st.session_state["current_scenario_meta"] = {
                            "name": "Pasted Terminal Session",
                            "type": "Manual Paste"
                        }
                    st.success(f"Analyzed log output. Detected {res['total_findings']} issues.")
                    st.rerun()
                else:
                    st.warning("Please paste log output before running analysis.")

    current_analysis = st.session_state.get("current_analysis", None)

    if not current_analysis or not current_analysis.get("findings"):
        st.markdown(f"""
        <div class="rg-card" style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: {UI_THEME['text_primary']}; margin-bottom: 0.5rem;">No Diagnostic Analysis Active</div>
            <div style="font-size: 0.85rem; color: {UI_THEME['text_secondary']}; max-width: 500px; margin: 0 auto 1.5rem auto;">
                Upload a log file above, paste terminal output, or launch one of the 5 interactive demo scenarios from the Command Center.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    findings = current_analysis.get("findings", [])
    
    # Filter Controls
    st.markdown("### Detected Findings & Root Cause Analysis")
    col_search, col_sev, col_cat = st.columns([1.5, 1.0, 1.2])

    with col_search:
        search_query = st.text_input("🔍 Search findings by keyword, node, or topic", "").lower()

    with col_sev:
        sev_filter = st.selectbox("Severity Filter", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"])

    with col_cat:
        cat_filter = st.selectbox("Category Filter", ["ALL"] + [c.value for c in DiagnosticCategory])

    # Filter findings
    filtered = []
    for f in findings:
        if sev_filter != "ALL" and f.get("severity") != sev_filter:
            continue
        if cat_filter != "ALL" and f.get("category") != cat_filter:
            continue
        if search_query:
            text_corpus = f"{f.get('title', '')} {f.get('evidence', '')} {f.get('id', '')} {f.get('category', '')}".lower()
            if search_query not in text_corpus:
                continue
        filtered.append(f)

    st.caption(f"Displaying {len(filtered)} of {len(findings)} findings")

    # Linear-style List of Findings
    for idx, f in enumerate(filtered):
        fid = f.get("id", f"ROBO-{idx+1:03d}")
        title = f.get("title", "Finding")
        sev = f.get("severity", "INFO")
        cat = f.get("category", "General")

        with st.expander(f"[{fid}] {title} — {sev}", expanded=idx == 0):
            render_finding_detail(f, explanation_engine)

    # Persistent Interactive Copilot Assistant Drawer
    st.markdown("<br>", unsafe_allow_html=True)
    from ui.components import render_copilot_chat_drawer
    render_copilot_chat_drawer(explanation_engine)
