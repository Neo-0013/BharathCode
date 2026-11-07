"""
ROBOGUARD AI — QoS Compatibility Engine
Implements formal ROS 2 Jazzy QoS (Quality of Service) compatibility matrices
for Publisher-Subscriber communication pairs in DDS.
"""

from typing import Dict, Any, List, Optional
from config.settings import Severity, DiagnosticCategory, Confidence

class QoSPolicyCompatibility:
    # Reliability: Pub offered vs Sub requested
    # Rule: Offered >= Requested
    # Ranking: RELIABLE (2) > BEST_EFFORT (1)
    RELIABILITY_LEVELS = {
        "BEST_EFFORT": 1,
        "RELIABLE": 2
    }

    # Durability: Pub offered vs Sub requested
    # Rule: Offered >= Requested
    # Ranking: TRANSIENT_LOCAL (2) > VOLATILE (1)
    DURABILITY_LEVELS = {
        "VOLATILE": 1,
        "TRANSIENT_LOCAL": 2
    }

    # Liveliness
    # Ranking: MANUAL_BY_TOPIC (3) > MANUAL_BY_PARTICIPANT (2) > AUTOMATIC (1)
    LIVELINESS_LEVELS = {
        "AUTOMATIC": 1,
        "MANUAL_BY_PARTICIPANT": 2,
        "MANUAL_BY_TOPIC": 3
    }

class QoSAnalyzer:
    """Evaluates ROS 2 publisher and subscriber QoS profile compatibility."""

    @staticmethod
    def normalize_value(val: Any) -> str:
        if val is None:
            return "UNKNOWN"
        return str(val).strip().upper().replace(" ", "_").replace("RMW_QOS_POLICY_RELIABILITY_", "").replace("RMW_QOS_POLICY_DURABILITY_", "")

    def evaluate_pair(self, topic: str, pub_node: str, sub_node: str,
                      pub_qos: Dict[str, Any], sub_qos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate compatibility between a specific publisher and subscriber endpoint.
        Returns a structured dictionary with compatibility boolean and detailed violations.
        """
        pub_rel = self.normalize_value(pub_qos.get("reliability", "RELIABLE"))
        sub_rel = self.normalize_value(sub_qos.get("reliability", "RELIABLE"))
        pub_dur = self.normalize_value(pub_qos.get("durability", "VOLATILE"))
        sub_dur = self.normalize_value(sub_qos.get("durability", "VOLATILE"))

        violations = []
        warnings = []

        # 1. Reliability Check
        pub_rel_rank = QoSPolicyCompatibility.RELIABILITY_LEVELS.get(pub_rel, 0)
        sub_rel_rank = QoSPolicyCompatibility.RELIABILITY_LEVELS.get(sub_rel, 0)

        if pub_rel_rank > 0 and sub_rel_rank > 0:
            if pub_rel_rank < sub_rel_rank:
                violations.append({
                    "policy": "Reliability",
                    "offered": pub_rel,
                    "requested": sub_rel,
                    "detail": f"Subscriber '{sub_node}' requests RELIABLE, but Publisher '{pub_node}' offers BEST_EFFORT. Messages will be dropped by DDS middleware."
                })

        # 2. Durability Check
        pub_dur_rank = QoSPolicyCompatibility.DURABILITY_LEVELS.get(pub_dur, 0)
        sub_dur_rank = QoSPolicyCompatibility.DURABILITY_LEVELS.get(sub_dur, 0)

        if pub_dur_rank > 0 and sub_dur_rank > 0:
            if pub_dur_rank < sub_dur_rank:
                violations.append({
                    "policy": "Durability",
                    "offered": pub_dur,
                    "requested": sub_dur,
                    "detail": f"Subscriber '{sub_node}' requests TRANSIENT_LOCAL (historical latching), but Publisher '{pub_node}' offers VOLATILE. Late-joining subscribers will miss state messages."
                })

        # 3. History & Depth heuristic check (Warning)
        pub_depth = pub_qos.get("depth", 10)
        sub_depth = sub_qos.get("depth", 10)
        if isinstance(pub_depth, int) and isinstance(sub_depth, int):
            if pub_depth < 2 and pub_rel == "RELIABLE":
                warnings.append({
                    "policy": "History Depth",
                    "offered": pub_depth,
                    "requested": sub_depth,
                    "detail": f"Publisher '{pub_node}' depth is {pub_depth} with RELIABLE policy. In high-throughput topics, queue overflows may cause buffer stalling."
                })

        is_compatible = len(violations) == 0

        return {
            "topic": topic,
            "publisher": pub_node,
            "subscriber": sub_node,
            "is_compatible": is_compatible,
            "violations": violations,
            "warnings": warnings,
            "pub_qos": {"reliability": pub_rel, "durability": pub_dur, "depth": pub_depth},
            "sub_qos": {"reliability": sub_rel, "durability": sub_dur, "depth": sub_depth}
        }

    def generate_findings(self, evaluations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Converts raw QoS evaluation results into standardized DiagnosticFinding objects."""
        findings = []
        counter = 1

        for eval_res in evaluations:
            if not eval_res["is_compatible"]:
                for v in eval_res["violations"]:
                    finding = {
                        "id": f"ROBO-QOS-{counter:03d}",
                        "title": f"QoS Incompatibility on '{eval_res['topic']}': {v['policy']} Mismatch",
                        "category": DiagnosticCategory.QOS_COMPATIBILITY.value,
                        "severity": Severity.CRITICAL.value,
                        "status": Confidence.CONFIRMED.value,
                        "evidence": (
                            f"Topic: {eval_res['topic']}\n"
                            f"Publisher [{eval_res['publisher']}]: Offered {v['policy']} = {v['offered']}\n"
                            f"Subscriber [{eval_res['subscriber']}]: Requested {v['policy']} = {v['requested']}\n"
                            f"DDS Error: {v['detail']}"
                        ),
                        "entities": [eval_res["topic"], eval_res["publisher"], eval_res["subscriber"]],
                        "root_cause": (
                            f"Incompatible DDS QoS policies between publisher and subscriber. "
                            f"ROS 2 Jazzy middleware requires Offered {v['policy']} >= Requested {v['policy']}."
                        ),
                        "troubleshooting": [
                            f"Reconfigure subscriber '{eval_res['subscriber']}' to match offered policy ({v['offered']}).",
                            f"Or reconfigure publisher '{eval_res['publisher']}' to satisfy requested policy ({v['requested']}).",
                            "Review launch parameters or C++/Python QoS profile instantiation in node source."
                        ],
                        "validation_commands": [
                            f"ros2 topic info -v {eval_res['topic']}",
                            f"ros2 node info {eval_res['publisher']}",
                            f"ros2 node info {eval_res['subscriber']}"
                        ]
                    }
                    findings.append(finding)
                    counter += 1

            for w in eval_res.get("warnings", []):
                finding = {
                    "id": f"ROBO-QOS-WARN-{counter:03d}",
                    "title": f"QoS Configuration Caution on '{eval_res['topic']}': {w['policy']}",
                    "category": DiagnosticCategory.QOS_COMPATIBILITY.value,
                    "severity": Severity.MEDIUM.value,
                    "status": Confidence.CONFIRMED.value,
                    "evidence": (
                        f"Topic: {eval_res['topic']}\n"
                        f"Publisher [{eval_res['publisher']}]: Depth {w['offered']}\n"
                        f"Detail: {w['detail']}"
                    ),
                    "entities": [eval_res["topic"], eval_res["publisher"]],
                    "root_cause": "Potentially constrained QoS queue depth on high-frequency topic.",
                    "troubleshooting": [
                        "Monitor topic latency and message drop rate.",
                        "Increase queue depth if message loss occurs during traffic bursts."
                    ],
                    "validation_commands": [
                        f"ros2 topic hz {eval_res['topic']}"
                    ]
                }
                findings.append(finding)
                counter += 1

        return findings
