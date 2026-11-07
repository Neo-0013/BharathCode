"""
ROBOGUARD AI — AI Copilot Prompts
Defensive, evidence-grounded prompt engineering templates for ROS 2 Jazzy
engineering diagnostics and robotics cybersecurity runbooks.
"""

import json
from typing import Dict, Any, List

SYSTEM_PROMPT = """You are ROBOGUARD AI, a Senior Autonomous Systems Diagnostic & Cybersecurity Copilot specializing in ROS 2 Jazzy and DDS middleware.

Your mission is to provide explainable, evidence-grounded troubleshooting guidance for robotics software engineers and cybersecurity researchers.

STRICT OPERATIONAL RULES:
1. GROUNDING: Reference only the explicit findings, log traces, topics, nodes, and QoS parameters provided in the prompt. Never invent imaginary telemetry, nonexistent topics, or fabricated test results.
2. DISTINCTION: Clearly distinguish between Confirmed Observations (empirical evidence), Likely Root Causes (engineering deduction), and Advisory Recommendations (suggested actions).
3. ROS 2 JAZZY CONFORMANCE: Apply official ROS 2 Jazzy standards (REP-105 for coordinate frames, standard QoS compatibility rules, SROS2 enclave best practices).
4. SAFETY FIRST: Never generate destructive shell commands (e.g. 'rm -rf /', kill -9 on unknown PIDs, or unauthenticated open network scripts).
5. STRUCTURE: Respond with clear, structured sections:
   - Executive Analysis
   - Root Cause Hierarchy
   - Architectural Explanation (DDS/ROS 2 mechanics)
   - Step-by-Step Remediation
   - Exact Validation Commands
"""

def build_finding_explanation_prompt(finding: Dict[str, Any]) -> str:
    """Creates a grounded prompt for a single diagnostic or cybersecurity finding."""
    return f"""Analyze the following detected ROS 2 engineering finding and provide an explainable troubleshooting runbook.

FINDING DETAILS:
- ID: {finding.get('id', 'N/A')}
- Title: {finding.get('title', 'Unknown')}
- Category: {finding.get('category', 'General')}
- Severity: {finding.get('severity', 'INFO')}
- Status: {finding.get('status', 'Confirmed')}
- Affected Entities: {', '.join(finding.get('entities', [])) if finding.get('entities') else 'Not specified'}

EMPIRICAL EVIDENCE EXTRACTED FROM SYSTEM:
{finding.get('evidence', 'No raw snippet provided.')}

DETERMINISTIC ROOT CAUSE:
{finding.get('root_cause', finding.get('explanation', 'Not specified.'))}

PRELIMINARY TROUBLESHOOTING STEPS:
{json.dumps(finding.get('troubleshooting', []), indent=2)}

REQUEST:
Please synthesize a deep engineering explanation. Explain WHY this failure occurs under ROS 2 Jazzy DDS mechanics, what risks it poses to robot autonomy/safety, and provide copy-pasteable ROS 2 CLI commands to verify and fix the issue.
"""

def build_full_system_synthesis_prompt(findings: List[Dict[str, Any]], security_score: Dict[str, Any]) -> str:
    """Creates a holistic synthesis prompt across all detected findings in the system."""
    summary_findings = []
    for f in findings[:10]: # Top 10 findings to stay within token budget
        summary_findings.append({
            "id": f.get("id"),
            "title": f.get("title"),
            "severity": f.get("severity"),
            "category": f.get("category"),
            "summary_evidence": f.get("evidence", "")[:180]
        })

    return f"""Synthesize an Executive Diagnostic & Cybersecurity Assessment for the analyzed autonomous robot.

OVERALL METRICS:
- Total Identified Issues: {len(findings)}
- Defensive Security Posture Score: {security_score.get('score', 'N/A')}% ({security_score.get('risk_tier', 'UNASSESSED')})
- Deductions: {security_score.get('deductions_applied', 0)} points

TOP DETECTED FINDINGS:
{json.dumps(summary_findings, indent=2)}

REQUEST:
Provide an Executive Engineering Briefing:
1. Overall Robot Health & Mission Readiness Assessment
2. Primary Failure Chain (How individual findings might cascade into complete mission failure)
3. High-Priority Remediation Order (Which issue to patch first, second, third)
4. Key ROS 2 Jazzy Best Practices for this system
"""
