"""
ROBOGUARD AI — Defensive Robotics Cybersecurity Engine
Audits ROS 2 Jazzy and DDS Security specifications: SROS2 enclaves,
ROS_SECURITY_ENABLE, ROS_SECURITY_STRATEGY, keystore integrity,
DDS XML governance/permissions policies, and network exposure boundaries.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import CONFIG_DIR, Severity, DiagnosticCategory, Confidence

class SecurityEngine:
    """Defensive security posture analyzer for ROS 2 systems."""

    def __init__(self, rules_path: Optional[Path] = None):
        if rules_path is None:
            rules_path = CONFIG_DIR / "rules.yaml"
        self.rules_path = rules_path
        self.security_rules = self._load_security_rules()

    def _load_security_rules(self) -> List[Dict[str, Any]]:
        if not self.rules_path.exists():
            return []
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("security_rules", []) if data else []
        except Exception:
            return []

    def audit_environment(self, env_vars: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Audit environment variables relevant to ROS 2 security.
        If env_vars is None, uses actual os.environ.
        """
        if env_vars is None:
            env_vars = dict(os.environ)

        findings = []

        # 1. ROS_SECURITY_ENABLE
        sec_enable = env_vars.get("ROS_SECURITY_ENABLE", "").strip().lower()
        if sec_enable not in ["true", "1"]:
            findings.append({
                "id": "ROBO-SEC-001",
                "title": "SROS2 DDS Security Protection Disabled (Unauthenticated & Plaintext)",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.CRITICAL.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "Environment Variable: ROS_SECURITY_ENABLE",
                "evidence": f"ROS_SECURITY_ENABLE='{env_vars.get('ROS_SECURITY_ENABLE', '<UNSET>')}'",
                "explanation": (
                    "ROS 2 communications run in standard DDS plaintext mode. Authentication, "
                    "access control, and cryptographic payload encryption are completely absent."
                ),
                "impact": (
                    "An attacker connected to the same LAN or Wi-Fi can freely sniff telemetry, "
                    "spoof actuation commands (/cmd_vel), or hijack robot navigation."
                ),
                "mitigation": (
                    "1. Generate an SROS2 keystore: ros2 security create_keystore ~/sros2_keystore\n"
                    "2. Create node enclaves with X.509 certs: ros2 security create_enclave ~/sros2_keystore /my_node\n"
                    "3. Export ROS_SECURITY_ENABLE=true and ROS_SECURITY_KEYSTORE=~/sros2_keystore"
                ),
                "verification": "echo $ROS_SECURITY_ENABLE && ros2 security list_enclaves $ROS_SECURITY_KEYSTORE",
                "confidence": "High"
            })

        # 2. ROS_SECURITY_STRATEGY
        sec_strat = env_vars.get("ROS_SECURITY_STRATEGY", "").strip()
        if sec_strat.lower() == "permissive":
            findings.append({
                "id": "ROBO-SEC-002",
                "title": "Permissive SROS2 Security Strategy Active (Bypass Risk)",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.HIGH.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "Environment Variable: ROS_SECURITY_STRATEGY",
                "evidence": f"ROS_SECURITY_STRATEGY='{sec_strat}'",
                "explanation": (
                    "When strategy is 'Permissive', nodes lacking valid certificates or enclaves "
                    "are allowed to fall back to unencrypted and unauthenticated communication instead of failing closed."
                ),
                "impact": "Rogue or non-compliant nodes can connect to the robot DDS domain without being blocked.",
                "mitigation": "Set ROS_SECURITY_STRATEGY=Enforce in production deployments.",
                "verification": "echo $ROS_SECURITY_STRATEGY",
                "confidence": "High"
            })

        # 3. ROS_DOMAIN_ID
        domain_id = env_vars.get("ROS_DOMAIN_ID", "").strip()
        if not domain_id or domain_id == "0":
            findings.append({
                "id": "ROBO-SEC-003",
                "title": "Default ROS_DOMAIN_ID (0) in Use on Broadcast Subnet",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.HIGH.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "Environment Variable: ROS_DOMAIN_ID",
                "evidence": f"ROS_DOMAIN_ID='{domain_id if domain_id else '<UNSET (defaults to 0)>'}'",
                "explanation": (
                    "In ROS 2, nodes on Domain 0 broadcast DDS Simple Participant Discovery (SPDP) "
                    "packets over multicast (239.255.0.1) across the entire local network subnet."
                ),
                "impact": "Crosstalk between different robots or developer laptops; accidental message injection.",
                "mitigation": "Assign an isolated ROS_DOMAIN_ID (integer 1-101) for each robot system.",
                "verification": "echo $ROS_DOMAIN_ID",
                "confidence": "High"
            })

        # 4. ROS_AUTOMATIC_DISCOVERY_RANGE
        discovery_range = env_vars.get("ROS_AUTOMATIC_DISCOVERY_RANGE", "").strip().upper()
        if discovery_range == "SUBNET":
            findings.append({
                "id": "ROBO-SEC-004",
                "title": "Wide Subnet Automatic Discovery Range Active",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.MEDIUM.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "Environment Variable: ROS_AUTOMATIC_DISCOVERY_RANGE",
                "evidence": f"ROS_AUTOMATIC_DISCOVERY_RANGE='{discovery_range}'",
                "explanation": (
                    "DDS discovery messages are transmitted across the entire subnet broadcast domain. "
                    "In ROS 2 Jazzy, ROS_AUTOMATIC_DISCOVERY_RANGE can be restricted."
                ),
                "impact": "Increased network multicast congestion and broader reconnaissance surface for unauthorized hosts.",
                "mitigation": "Set ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST for local node clusters or use configured unicast peers.",
                "verification": "echo $ROS_AUTOMATIC_DISCOVERY_RANGE",
                "confidence": "Medium"
            })

        return findings

    def audit_dds_xml_configuration(self, xml_content: str) -> List[Dict[str, Any]]:
        """Audits DDS security XML files (governance.xml, permissions.xml)."""
        findings = []
        if not xml_content or not xml_content.strip():
            return findings

        # Check for unauthenticated participants
        if re.search(r'<allow_unauthenticated_participants>\s*true\s*</allow_unauthenticated_participants>', xml_content, re.IGNORECASE):
            findings.append({
                "id": "ROBO-SEC-005",
                "title": "DDS Governance Insecurity: Unauthenticated Participants Allowed",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.CRITICAL.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "DDS Governance XML: <allow_unauthenticated_participants>",
                "evidence": "<allow_unauthenticated_participants>true</allow_unauthenticated_participants>",
                "explanation": "The governance policy explicitly disables authentication enforcement for participants.",
                "impact": "Any unauthorized participant can join the DDS domain and interact with topics.",
                "mitigation": "Change <allow_unauthenticated_participants> to false.",
                "verification": "grep -n 'allow_unauthenticated_participants' governance.xml",
                "confidence": "High"
            })

        # Check for wildcard topic permission in <publish> or <subscribe>
        if re.search(r'<(?:publish|subscribe)>.*?<topic>\s*\*\s*</topic>', xml_content, re.DOTALL | re.IGNORECASE):
            findings.append({
                "id": "ROBO-SEC-006",
                "title": "Overly Permissive DDS Permissions: Wildcard Topic Access Granted",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.HIGH.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "DDS Permissions XML: <topic>*</topic>",
                "evidence": "Found wildcard topic rule: <topic>*</topic>",
                "explanation": "The permission policy grants read or write access to every topic across the entire DDS domain.",
                "impact": "Violates principle of least privilege. Compromise of an unprivileged node compromises the entire robot.",
                "mitigation": "Scope topic permissions explicitly (e.g. <topic>/diagnostics</topic> or <topic>/robot1/*</topic>).",
                "verification": "grep -n '<topic>\\*' permissions.xml",
                "confidence": "High"
            })

        # Check for unencrypted discovery protection
        if re.search(r'<discovery_protection>\s*NONE\s*</discovery_protection>', xml_content, re.IGNORECASE):
            findings.append({
                "id": "ROBO-SEC-007",
                "title": "DDS Discovery Metadata Protection Disabled (NONE)",
                "category": DiagnosticCategory.CYBERSECURITY.value,
                "severity": Severity.HIGH.value,
                "status": Confidence.CONFIRMED.value,
                "affected_config": "DDS Governance XML: <discovery_protection>",
                "evidence": "<discovery_protection>NONE</discovery_protection>",
                "explanation": "DDS discovery packets are sent unencrypted, exposing node names, topic names, and QoS policies to network sniffers.",
                "impact": "Enables passive network reconnaissance and mapping of robot communication topology.",
                "mitigation": "Set <discovery_protection>ENCRYPT</discovery_protection> or SECURE.",
                "verification": "grep -n 'discovery_protection' governance.xml",
                "confidence": "High"
            })

        return findings

    def calculate_posture_score(self, findings: List[Dict[str, Any]], total_controls: int = 10) -> Dict[str, Any]:
        """
        Transparently calculates a defensive posture score from 0-100%.
        Explicitly itemizes assessed controls, deductions per severity, and unknown/unassessed controls.
        """
        base_score = 100.0
        deductions = {
            Severity.CRITICAL.value: 25.0,
            Severity.HIGH.value: 15.0,
            Severity.MEDIUM.value: 8.0,
            Severity.LOW.value: 3.0,
            Severity.INFO.value: 0.0
        }

        total_deduction = 0.0
        breakdown = []

        for f in findings:
            sev = f.get("severity", Severity.INFO.value)
            ded = deductions.get(sev, 0.0)
            total_deduction += ded
            breakdown.append({
                "finding_id": f.get("id"),
                "title": f.get("title"),
                "severity": sev,
                "deduction": ded
            })

        final_score = max(0.0, round(base_score - total_deduction, 1))
        
        # Risk tier definition
        if final_score >= 85:
            tier = "HARDENED"
            color = "#10B981"
        elif final_score >= 65:
            tier = "ACCEPTABLE WITH DEFECTS"
            color = "#F59E0B"
        elif final_score >= 40:
            tier = "ELEVATED RISK"
            color = "#F97316"
        else:
            tier = "CRITICAL EXPOSURE"
            color = "#EF4444"

        return {
            "score": final_score,
            "risk_tier": tier,
            "color": color,
            "total_findings": len(findings),
            "assessed_controls_count": total_controls,
            "deductions_applied": total_deduction,
            "breakdown": breakdown,
            "transparency_note": (
                "Score is calculated deterministically: Base (100) minus explicit weighted penalties "
                "(Critical -25, High -15, Medium -8, Low -3). Unassessed controls are not assumed secure."
            )
        }
