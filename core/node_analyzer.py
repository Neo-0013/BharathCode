"""
ROBOGUARD AI — Node & Topic Architecture Analyzer
Inspects node states, topic connectivity, orphaned endpoints,
and publisher/subscriber mismatches across the ROS 2 computational graph.
"""

from typing import Dict, Any, List, Set, Optional
from config.settings import Severity, DiagnosticCategory, Confidence

class NodeAnalyzer:
    """Analyzes ROS 2 nodes, topics, and publisher/subscriber parity."""

    CRITICAL_TOPICS = {
        "/cmd_vel": "Robot Velocity Actuation Command",
        "/scan": "2D LiDAR LaserScan Stream",
        "/tf": "Dynamic Coordinate Transform Tree",
        "/tf_static": "Static URDF Coordinate Transforms",
        "/odom": "Wheel/Visual Odometry Feed"
    }

    def analyze_topology(self, nodes: List[Dict[str, Any]], topics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        nodes: [{"name": "/teleop_twist_keyboard", "namespace": "/", "state": "active", ...}]
        topics: [{"name": "/cmd_vel", "type": "geometry_msgs/msg/Twist", "publishers": ["/teleop"], "subscribers": []}]
        """
        findings = []
        counter = 1

        active_nodes = {n.get("name") for n in nodes if n.get("name")}
        
        # 1. Topic Parity & Orphan Analysis
        for t in topics:
            name = t.get("name", "")
            pubs = t.get("publishers", [])
            subs = t.get("subscribers", [])
            pub_count = len(pubs)
            sub_count = len(subs)

            # Check critical topic without subscriber
            if name in self.CRITICAL_TOPICS:
                desc = self.CRITICAL_TOPICS[name]
                if pub_count > 0 and sub_count == 0:
                    findings.append({
                        "id": f"ROBO-TOPIC-{counter:03d}",
                        "title": f"Critical Topic Unconsumed: '{name}' has 0 Subscribers",
                        "category": DiagnosticCategory.NODE_TOPIC.value,
                        "severity": Severity.CRITICAL.value if name == "/cmd_vel" else Severity.HIGH.value,
                        "status": Confidence.CONFIRMED.value,
                        "evidence": f"Topic: {name} ({desc})\nPublishers: {pubs}\nSubscribers: NONE (0)",
                        "entities": [name] + pubs,
                        "root_cause": (
                            f"Messages on critical control topic '{name}' are being published into the void. "
                            f"The expected motor controller or navigation consumer node is either unlaunched or crashed."
                        ),
                        "troubleshooting": [
                            f"Verify that the actuator driver / base controller node is running.",
                            f"Check if topic remapping was applied (e.g. diff_drive_controller expecting /diff_cont/cmd_vel instead of {name}).",
                            "Inspect node launch file for namespace prefixes."
                        ],
                        "validation_commands": [
                            f"ros2 topic info {name}",
                            "ros2 node list",
                            f"ros2 topic echo {name} --once"
                        ]
                    })
                    counter += 1

                elif pub_count == 0 and sub_count > 0:
                    findings.append({
                        "id": f"ROBO-TOPIC-{counter:03d}",
                        "title": f"Starved Subscriber: Topic '{name}' has 0 Publishers",
                        "category": DiagnosticCategory.NODE_TOPIC.value,
                        "severity": Severity.HIGH.value,
                        "status": Confidence.CONFIRMED.value,
                        "evidence": f"Topic: {name} ({desc})\nPublishers: NONE (0)\nSubscribers: {subs}",
                        "entities": [name] + subs,
                        "root_cause": f"Subscribers are waiting for messages on '{name}', but no active node is publishing data.",
                        "troubleshooting": [
                            "Check that sensor drivers or upstream generators are actively publishing.",
                            "Verify topic name spelling and remap configurations in the subscriber node."
                        ],
                        "validation_commands": [
                            f"ros2 topic info {name}",
                            f"ros2 topic hz {name}"
                        ]
                    })
                    counter += 1

        # 2. Lifecycle Node State Analysis
        for n in nodes:
            name = n.get("name", "")
            state = n.get("state", "").lower()
            lifecycle = n.get("is_lifecycle", False)

            if lifecycle and state in ["unconfigured", "inactive", "finalized", "error"]:
                severity = Severity.HIGH.value if state in ["unconfigured", "inactive"] else Severity.CRITICAL.value
                findings.append({
                    "id": f"ROBO-NODE-{counter:03d}",
                    "title": f"Inactive Lifecycle Node: '{name}' in State [{state.upper()}]",
                    "category": DiagnosticCategory.NODE_TOPIC.value,
                    "severity": severity,
                    "status": Confidence.CONFIRMED.value,
                    "evidence": f"Node: {name}\nLifecycle State: {state.upper()}\nExpected: ACTIVE",
                    "entities": [name],
                    "root_cause": (
                        f"Lifecycle node '{name}' has not reached ACTIVE state. "
                        f"In ROS 2 Jazzy, inactive lifecycle nodes do not publish topic data or process execution loops."
                    ),
                    "troubleshooting": [
                        f"Check nav2_lifecycle_manager or custom lifecycle supervisor launch config.",
                        f"Trigger manual transition: ros2 lifecycle set {name} configure && ros2 lifecycle set {name} activate."
                    ],
                    "validation_commands": [
                        f"ros2 lifecycle get {name}",
                        f"ros2 lifecycle set {name} activate"
                    ]
                })
                counter += 1

        return {
            "total_nodes": len(nodes),
            "total_topics": len(topics),
            "findings": findings
        }
