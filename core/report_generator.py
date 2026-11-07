"""
ROBOGUARD AI — Engineering Report Generator Module
Generates production-grade Markdown and PDF diagnostic and cybersecurity reports.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config.settings import APP_NAME, APP_VERSION, APP_TAGLINE, TARGET_ROS_DISTRO, REPORTS_DIR

class ReportGenerator:
    """Generates structured Markdown and PDF reports from diagnostic and security results."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown(self, analysis_result: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
        """Generates a comprehensive Markdown report string."""
        meta = metadata or {}
        timestamp = meta.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        target_system = meta.get("system_name", "Autonomous Mobile Robot (ROS 2 Jazzy)")
        findings = analysis_result.get("findings", [])
        sec_score = analysis_result.get("security_score", {})
        severity_counts = analysis_result.get("severity_counts", {})

        md = []
        md.append(f"# {APP_NAME} — Technical Diagnostic & Cybersecurity Report")
        md.append(f"*{APP_TAGLINE}*  ")
        md.append(f"**Generated:** {timestamp} | **Target Environment:** {TARGET_ROS_DISTRO} | **System:** {target_system}\n")
        md.append("---\n")

        # Executive Summary
        md.append("## 1. Executive Summary\n")
        md.append(f"ROBOGUARD AI completed an automated dual-engine evaluation across computational logs, QoS profiles, transform trees, and DDS security configurations.\n")
        md.append("| Metric | Value | Status |")
        md.append("| :--- | :--- | :--- |")
        md.append(f"| Total Findings | **{len(findings)}** | Assessed |")
        md.append(f"| Critical Severity | **{severity_counts.get('CRITICAL', 0)}** | Action Required |")
        md.append(f"| High Severity | **{severity_counts.get('HIGH', 0)}** | Action Required |")
        md.append(f"| Medium Severity | **{severity_counts.get('MEDIUM', 0)}** | Attention |")
        md.append(f"| Low / Informational | **{severity_counts.get('LOW', 0) + severity_counts.get('INFO', 0)}** | Monitored |")
        if sec_score:
            md.append(f"| Defensive Security Posture | **{sec_score.get('score', 0)}%** | **{sec_score.get('risk_tier', 'UNASSESSED')}** |")
        md.append("\n")

        # Findings Detail
        md.append("## 2. Identified Engineering & Security Findings\n")
        if not findings:
            md.append("No defects or configuration vulnerabilities were detected in the evaluated input.\n")
        else:
            for i, f in enumerate(findings, 1):
                sev = f.get("severity", "INFO")
                md.append(f"### {i}. [{f.get('id', 'N/A')}] {f.get('title', 'Untitled Finding')}")
                md.append(f"- **Category:** {f.get('category', 'General')}")
                md.append(f"- **Severity:** `{sev}` | **Status:** `{f.get('status', 'Confirmed')}`")
                if f.get("affected_config"):
                    md.append(f"- **Affected Config:** `{f.get('affected_config')}`")
                md.append("\n**Empirical Evidence:**")
                md.append("```text")
                md.append(f.get("evidence", "No raw evidence provided."))
                md.append("```\n")

                if f.get("root_cause"):
                    md.append(f"**Probable Root Cause:**\n{f.get('root_cause')}\n")
                if f.get("explanation"):
                    md.append(f"**Technical Explanation:**\n{f.get('explanation')}\n")
                if f.get("impact"):
                    md.append(f"**Security & Operational Impact:**\n{f.get('impact')}\n")

                troubleshooting = f.get("troubleshooting", [])
                if troubleshooting:
                    md.append("**Recommended Remediation:**")
                    for step in troubleshooting:
                        md.append(f"1. {step}")
                    md.append("")

                validation_cmds = f.get("validation_commands", [])
                if validation_cmds:
                    md.append("**Validation Commands:**")
                    md.append("```bash")
                    for cmd in validation_cmds:
                        md.append(cmd)
                    md.append("```\n")
                md.append("---\n")

        # Disclaimers
        md.append("## 3. Scope & Disclaimers\n")
        md.append("- **Deterministic Basis:** All findings were derived deterministically from user-provided logs, configurations, and topic graphs.")
        md.append("- **AI Copilot Assistance:** Where AI explanations are rendered, they serve as advisory troubleshooting runbooks and require human engineering review before execution.")
        md.append("- **Defensive Posture:** ROBOGUARD AI conducts passive static analysis and does not perform active network penetration or exploit execution.")
        md.append(f"\n*Generated by {APP_NAME} v{APP_VERSION} (BharatCode Build League)*\n")

        return "\n".join(md)

    def generate_pdf(self, analysis_result: Dict[str, Any], filepath: Path,
                     metadata: Optional[Dict[str, Any]] = None) -> Path:
        """Generates a publication-grade PDF report using ReportLab."""
        meta = metadata or {}
        timestamp = meta.get("timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        findings = analysis_result.get("findings", [])
        sec_score = analysis_result.get("security_score", {})
        severity_counts = analysis_result.get("severity_counts", {})

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom Paragraph Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            leading=13,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=14
        )
        h2_style = ParagraphStyle(
            'Heading2Custom',
            parent=styles['Heading2'],
            fontSize=13,
            leading=17,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyCustom',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#334155'),
            spaceAfter=6
        )
        code_style = ParagraphStyle(
            'CodeCustom',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            fontName='Courier',
            textColor=colors.HexColor('#0F172A'),
            backColor=colors.HexColor('#F1F5F9'),
            spaceBefore=4,
            spaceAfter=6
        )

        story = []

        # Header Title
        story.append(Paragraph(f"{APP_NAME} — Technical Diagnostic Report", title_style))
        story.append(Paragraph(f"{APP_TAGLINE} | Generated: {timestamp} | Distro: {TARGET_ROS_DISTRO}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=12))

        # Executive Summary Table
        story.append(Paragraph("1. Executive Summary", h2_style))
        summary_data = [
            ["Metric", "Value", "Evaluation Status"],
            ["Total Findings Detected", str(len(findings)), "Analyzed"],
            ["Critical Severity Issues", str(severity_counts.get("CRITICAL", 0)), "Immediate Attention"],
            ["High Severity Issues", str(severity_counts.get("HIGH", 0)), "Action Required"],
            ["Medium / Low Issues", str(severity_counts.get("MEDIUM", 0) + severity_counts.get("LOW", 0)), "Review Recommended"],
            ["Security Posture Score", f"{sec_score.get('score', 0)}%", sec_score.get('risk_tier', 'N/A')]
        ]
        t = Table(summary_data, colWidths=[200, 100, 200])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ]))
        story.append(t)
        story.append(Spacer(1, 14))

        # Findings Detail
        story.append(Paragraph("2. Technical & Cybersecurity Findings", h2_style))
        if not findings:
            story.append(Paragraph("No defects or security misconfigurations identified.", body_style))
        else:
            for i, f in enumerate(findings[:15], 1): # Cap at 15 for PDF layout safety
                f_title = f"{i}. [{f.get('id', 'N/A')}] {f.get('title', 'Finding')}"
                sev_color = colors.HexColor('#EF4444') if f.get('severity') == 'CRITICAL' else colors.HexColor('#F97316')
                story.append(Paragraph(f"<b>{f_title}</b>", body_style))
                story.append(Paragraph(f"<b>Severity:</b> {f.get('severity')} | <b>Category:</b> {f.get('category')}", body_style))
                
                # Evidence snippet
                ev = f.get('evidence', '')[:250].replace('\n', ' ')
                story.append(Paragraph(f"<b>Evidence:</b> {ev}", code_style))
                
                # Root cause or explanation
                rc = f.get('root_cause') or f.get('explanation') or ''
                if rc:
                    story.append(Paragraph(f"<b>Root Cause:</b> {rc[:300]}", body_style))
                story.append(Spacer(1, 8))

        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=8))
        story.append(Paragraph("Defensive robotics engineering report generated by ROBOGUARD AI. No offensive scanning conducted.", subtitle_style))

        doc.build(story)
        return filepath
