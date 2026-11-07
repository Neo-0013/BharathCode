"""
ROBOGUARD AI — Master Diagnostic Engine
Orchestrates log parsing, QoS compatibility analysis, TF2 coordinate verification,
node/topic architecture inspection, and cybersecurity evaluation into a unified pipeline.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import Severity, DiagnosticCategory, Confidence
from core.log_parser import LogParser
from core.qos_analyzer import QoSAnalyzer
from core.tf_analyzer import TFAnalyzer
from core.node_analyzer import NodeAnalyzer
from core.security_engine import SecurityEngine

class DiagnosticEngine:
    """Master diagnostic aggregator and orchestrator."""

    def __init__(self):
        self.log_parser = LogParser()
        self.qos_analyzer = QoSAnalyzer()
        self.tf_analyzer = TFAnalyzer()
        self.node_analyzer = NodeAnalyzer()
        self.security_engine = SecurityEngine()

    def analyze_raw_log(self, text: str) -> List[Dict[str, Any]]:
        """Parses raw console log text and returns deterministic findings."""
        return self.log_parser.match_rules(text)

    def analyze_structured_scenario(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a complete, multi-faceted analysis on a structured input dictionary
        containing logs, nodes, topics, qos_pairs, tf_edges, and security_env.
        """
        findings: List[Dict[str, Any]] = []

        # 1. Parse raw log text if present
        log_text = data.get("raw_log", "")
        if log_text:
            log_findings = self.log_parser.match_rules(log_text)
            findings.extend(log_findings)

        # 2. Analyze QoS pairs
        qos_pairs = data.get("qos_pairs", [])
        if qos_pairs:
            evaluations = []
            for pair in qos_pairs:
                res = self.qos_analyzer.evaluate_pair(
                    topic=pair.get("topic", "unknown"),
                    pub_node=pair.get("publisher", "unknown_pub"),
                    sub_node=pair.get("subscriber", "unknown_sub"),
                    pub_qos=pair.get("pub_qos", {}),
                    sub_qos=pair.get("sub_qos", {})
                )
                evaluations.append(res)
            qos_findings = self.qos_analyzer.generate_findings(evaluations)
            findings.extend(qos_findings)

        # 3. Analyze TF frames
        tf_edges = data.get("tf_edges", [])
        if tf_edges:
            tf_res = self.tf_analyzer.analyze_tf_tree(tf_edges)
            findings.extend(tf_res.get("findings", []))

        # 4. Analyze Node and Topic topology
        nodes = data.get("nodes", [])
        topics = data.get("topics", [])
        if nodes or topics:
            node_res = self.node_analyzer.analyze_topology(nodes, topics)
            findings.extend(node_res.get("findings", []))

        # 5. Analyze Security environment & XML
        sec_env = data.get("security_env")
        sec_xml = data.get("security_xml", "")
        sec_findings = []
        if sec_env is not None:
            sec_findings.extend(self.security_engine.audit_environment(sec_env))
        if sec_xml:
            sec_findings.extend(self.security_engine.audit_dds_xml_configuration(sec_xml))
        findings.extend(sec_findings)

        # Calculate severity summary statistics
        severity_counts = {
            Severity.CRITICAL.value: 0,
            Severity.HIGH.value: 0,
            Severity.MEDIUM.value: 0,
            Severity.LOW.value: 0,
            Severity.INFO.value: 0
        }
        for f in findings:
            sev = f.get("severity", Severity.INFO.value)
            if sev in severity_counts:
                severity_counts[sev] += 1

        # Calculate security posture score
        security_score = self.security_engine.calculate_posture_score(sec_findings)

        return {
            "findings": findings,
            "total_findings": len(findings),
            "severity_counts": severity_counts,
            "security_score": security_score,
            "summary": {
                "critical": severity_counts[Severity.CRITICAL.value],
                "high": severity_counts[Severity.HIGH.value],
                "medium": severity_counts[Severity.MEDIUM.value],
                "low": severity_counts[Severity.LOW.value],
                "info": severity_counts[Severity.INFO.value]
            }
        }

    def parse_input_auto(self, raw_content: str, filename: str = "") -> Dict[str, Any]:
        """Automatically detects input format (JSON, YAML, XML, or Log text) and analyzes it."""
        raw_content = raw_content.strip()
        if not raw_content:
            return {"findings": [], "total_findings": 0, "severity_counts": {}, "security_score": self.security_engine.calculate_posture_score([])}

        # 1. Try parsing as JSON
        if (filename.endswith(".json") or raw_content.startswith("{")) and not filename.endswith(".xml"):
            try:
                data = json.loads(raw_content)
                if isinstance(data, dict):
                    return self.analyze_structured_scenario(data)
            except Exception:
                pass

        # 2. Try parsing as YAML
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            try:
                data = yaml.safe_load(raw_content)
                if isinstance(data, dict):
                    return self.analyze_structured_scenario(data)
            except Exception:
                pass

        # 3. Try parsing as XML (DDS security profile)
        if filename.endswith(".xml") or raw_content.startswith("<?xml") or "<dds" in raw_content.lower():
            sec_findings = self.security_engine.audit_dds_xml_configuration(raw_content)
            severity_counts = {s.value: 0 for s in Severity}
            for f in sec_findings:
                severity_counts[f.get("severity", Severity.INFO.value)] += 1
            return {
                "findings": sec_findings,
                "total_findings": len(sec_findings),
                "severity_counts": severity_counts,
                "security_score": self.security_engine.calculate_posture_score(sec_findings),
                "summary": severity_counts
            }

        # 4. Fallback to raw text log analysis
        log_findings = self.analyze_raw_log(raw_content)
        severity_counts = {s.value: 0 for s in Severity}
        for f in log_findings:
            severity_counts[f.get("severity", Severity.INFO.value)] += 1
        return {
            "findings": log_findings,
            "total_findings": len(log_findings),
            "severity_counts": severity_counts,
            "security_score": self.security_engine.calculate_posture_score([]),
            "summary": severity_counts
        }
