"""
ROBOGUARD AI — Explanation Engine Module
Coordinates online BharatCode AI model responses and offline deterministic
troubleshooting runbooks. Ensures robust, grounded explanations regardless of
network connectivity or API key availability.
"""

from typing import Dict, Any, List, Optional
from ai.client import BharatCodeClient
from ai.prompts import SYSTEM_PROMPT, build_finding_explanation_prompt, build_full_system_synthesis_prompt
from ai.response_validator import ResponseValidator

class ExplanationEngine:
    """Provides grounded AI and deterministic explanations for ROS 2 findings."""

    def __init__(self, client: Optional[BharatCodeClient] = None):
        self.client = client or BharatCodeClient()
        self.validator = ResponseValidator()

    def explain_finding(self, finding: Dict[str, Any], force_offline: bool = False) -> Dict[str, Any]:
        """
        Generates an in-depth engineering explanation for a specific finding.
        Uses BharatCode API if configured, otherwise falls back seamlessly to deterministic engine.
        """
        finding_id = finding.get("id", "UNKNOWN")

        # Use online BharatCode API if available and not forced offline
        if not force_offline and self.client.is_configured():
            prompt = build_finding_explanation_prompt(finding)
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            api_res = self.client.generate_chat_completion(messages)
            if api_res.get("success"):
                raw_content = api_res["content"]
                is_safe, sanitized, warnings = self.validator.validate_and_sanitize(raw_content, finding_id)
                prov_title = "Ollama Local AI" if getattr(self.client, "provider", "") == "ollama" else ("Google Gemini AI" if getattr(self.client, "provider", "") == "gemini" else "BharatCode AI Copilot")
                return {
                    "source": prov_title,
                    "model": api_res.get("model", self.client.model),
                    "explanation": sanitized,
                    "is_safe": is_safe,
                    "warnings": warnings,
                    "offline": False
                }
            # If API call failed, fall back to offline mode with warning
            offline_expl = self._generate_offline_explanation(finding)
            offline_expl["api_error"] = api_res.get("error")
            return offline_expl

        # Deterministic Offline Mode
        return self._generate_offline_explanation(finding)

    def synthesize_system_assessment(self, findings: List[Dict[str, Any]], security_score: Dict[str, Any],
                                    force_offline: bool = False) -> Dict[str, Any]:
        """Synthesizes high-level executive assessment across all detected findings."""
        if not force_offline and self.client.is_configured():
            prompt = build_full_system_synthesis_prompt(findings, security_score)
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            api_res = self.client.generate_chat_completion(messages)
            if api_res.get("success"):
                raw_content = api_res["content"]
                is_safe, sanitized, warnings = self.validator.validate_and_sanitize(raw_content)
                return {
                    "source": "BharatCode AI Copilot",
                    "model": api_res.get("model", self.client.model),
                    "summary": sanitized,
                    "offline": False
                }

        # Deterministic Offline Synthesis
        return self._generate_offline_synthesis(findings, security_score)

    def _generate_offline_explanation(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a rich, deterministic engineering runbook without external API calls."""
        finding_id = finding.get("id", "UNKNOWN")
        title = finding.get("title", "Detected Anomaly")
        category = finding.get("category", "General")
        severity = finding.get("severity", "INFO")
        evidence = finding.get("evidence", "No snippet available.")
        root_cause = finding.get("root_cause") or finding.get("explanation", "Standard ROS 2 defect.")
        troubleshooting = finding.get("troubleshooting", [])
        validation_cmds = finding.get("validation_commands", [])

        # Construct structured runbook
        sections = []
        sections.append(f"### Executive Diagnostic Runbook: [{finding_id}] {title}")
        sections.append(f"**Classification:** `{severity}` Severity | **Domain:** `{category}` | **Reasoning:** Deterministic Engineering Rules")
        sections.append(f"\n#### 1. Empirical Evidence\n```text\n{evidence}\n```")
        sections.append(f"\n#### 2. Root Cause Analysis\n{root_cause}")

        if category == "QoS Profile Compatibility":
            sections.append(
                "\n#### 3. ROS 2 Jazzy DDS Compatibility Law\n"
                "In ROS 2 DDS middleware (FastDDS, CycloneDDS), the Publisher's Offered QoS must be greater than "
                "or equal to the Subscriber's Requested QoS. If a subscriber requests RELIABLE delivery or TRANSIENT_LOCAL "
                "state, but the publisher offers BEST_EFFORT or VOLATILE, the DDS participant discovery will negotiate "
                "an incompatible QoS match and drop all communication silently."
            )
        elif category == "TF2 Coordinate Transforms":
            sections.append(
                "\n#### 3. ROS 2 Coordinate Frame Mechanics (REP-105)\n"
                "ROS 2 navigation and perception pipelines require a continuous, connected transform tree without cycles. "
                "When a frame lookup fails, Nav2 costmaps fail to clear, robot localization diverges, and obstacle "
                "avoidance emergency stop may trigger."
            )
        elif category == "Robotics Cybersecurity & SROS2":
            sections.append(
                "\n#### 3. Cybersecurity & DDS Attack Surface\n"
                "ROS 2 uses DDS RTPS protocol over UDP. Without SROS2 cryptographic enclaves, all topic communications "
                "traverse the physical network unencrypted and unauthenticated, permitting trivial packet sniffing, "
                "false command injection (/cmd_vel), or denial-of-service on the robot."
            )

        if troubleshooting:
            sections.append("\n#### 4. Actionable Remediation Steps")
            for idx, step in enumerate(troubleshooting, 1):
                sections.append(f"{idx}. {step}")

        if validation_cmds:
            sections.append("\n#### 5. Verification Commands\nRun the following commands in your robot terminal:")
            sections.append("```bash")
            for cmd in validation_cmds:
                sections.append(cmd)
            sections.append("```")

        content = "\n".join(sections)
        return {
            "source": "Deterministic Engineering Engine (Offline)",
            "model": "ROBOGUARD Rule-Based Synthesis",
            "explanation": content,
            "is_safe": True,
            "warnings": [],
            "offline": True
        }

    def _generate_offline_synthesis(self, findings: List[Dict[str, Any]], security_score: Dict[str, Any]) -> Dict[str, Any]:
        """Generates high-level deterministic summary."""
        crit = sum(1 for f in findings if f.get("severity") == "CRITICAL")
        high = sum(1 for f in findings if f.get("severity") == "HIGH")
        sec = security_score.get("score", 100)
        tier = security_score.get("risk_tier", "ASSESSED")

        text = (
            f"### Executive Health & Readiness Assessment\n\n"
            f"- **Mission Critical Issues:** {crit} Critical, {high} High defects detected.\n"
            f"- **Security Posture Score:** **{sec}%** ({tier})\n"
            f"- **System State:** {'DEGRADED — Mission abort recommended until critical issues are resolved.' if crit > 0 else 'FUNCTIONAL WITH WARNINGS'}\n\n"
            f"**Recommended Action Hierarchy:**\n"
            f"1. Resolve any Critical QoS mismatches and TF2 tree disconnections to restore node communication.\n"
            f"2. Fix missing Python or CMake dependencies preventing package startup.\n"
            f"3. Enable SROS2 encryption (`ROS_SECURITY_ENABLE=true`) and isolate `ROS_DOMAIN_ID` from shared Wi-Fi networks."
        )

        return {
            "source": "Deterministic Engineering Engine (Offline)",
            "model": "ROBOGUARD System Synthesizer",
            "summary": text,
            "offline": True
        }
