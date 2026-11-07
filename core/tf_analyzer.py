"""
ROBOGUARD AI — TF2 Coordinate Transform Engine
Diagnoses TF2 transform tree disconnections, missing frames,
REP-105 convention violations, and Lookup/Extrapolation exceptions.
"""

from typing import Dict, Any, List, Set, Optional
from config.settings import Severity, DiagnosticCategory, Confidence

class TFAnalyzer:
    """Analyzes ROS 2 TF transform trees and frame connectivity."""

    REP_105_STANDARD_FRAMES = {"map", "odom", "base_link", "base_footprint"}

    def __init__(self):
        pass

    def analyze_tf_tree(self, edges: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        edges: list of {"parent": "odom", "child": "base_link", "is_static": bool}
        Returns tree analysis including root frames, disconnected trees,
        and standard REP-105 convention conformance.
        """
        all_frames: Set[str] = set()
        parents: Dict[str, str] = {}
        children_map: Dict[str, List[str]] = {}

        for edge in edges:
            p = edge.get("parent")
            c = edge.get("child")
            if p and c:
                all_frames.add(p)
                all_frames.add(c)
                parents[c] = p
                children_map.setdefault(p, []).append(c)

        # Roots are frames that have children but no parent
        roots = [f for f in all_frames if f not in parents]
        # Leaves are frames that have parents but no children
        leaves = [f for f in all_frames if f not in children_map]

        findings = []

        # 1. Multiple roots detection (Disconnected TF tree)
        if len(roots) > 1:
            findings.append({
                "id": "ROBO-TF-001",
                "title": f"Disconnected TF2 Tree: Multiple Root Frames Detected ({', '.join(roots)})",
                "category": DiagnosticCategory.TF2_TRANSFORM.value,
                "severity": Severity.CRITICAL.value,
                "status": Confidence.CONFIRMED.value,
                "evidence": (
                    f"Frames in tree: {len(all_frames)}\n"
                    f"Independent root frames: {roots}\n"
                    f"Nodes attempting transforms across disconnected roots will throw tf2.ConnectivityException."
                ),
                "entities": roots,
                "root_cause": (
                    "Coordinate transform tree has two or more disjoint subgraphs. "
                    "Typically occurs when map->odom transform is not published by SLAM/AMCL, "
                    "or sensor frames are detached from base_link."
                ),
                "troubleshooting": [
                    "Verify localization node (e.g. amcl or slam_toolbox) is running and publishing the 'map' -> 'odom' transform.",
                    "Ensure robot_state_publisher is active with a valid URDF.",
                    "Verify static_transform_publisher is launched for any standalone sensor frames."
                ],
                "validation_commands": [
                    "ros2 run tf2_tools view_frames",
                    "ros2 run tf2_ros tf2_echo map odom",
                    "ros2 run tf2_ros tf2_echo odom base_link"
                ]
            })

        # 2. Missing base_link check (REP-105 violation)
        if "base_link" not in all_frames and len(all_frames) > 0:
            findings.append({
                "id": "ROBO-TF-002",
                "title": "REP-105 Violation: Missing 'base_link' Reference Frame",
                "category": DiagnosticCategory.TF2_TRANSFORM.value,
                "severity": Severity.HIGH.value,
                "status": Confidence.CONFIRMED.value,
                "evidence": f"Active frames: {list(all_frames)[:10]}. The standard robot origin 'base_link' is absent.",
                "entities": ["base_link"],
                "root_cause": "The robot URDF or odometry driver is not broadcasting the fundamental 'base_link' coordinate frame.",
                "troubleshooting": [
                    "Check URDF root link name.",
                    "Ensure odometry publisher broadcasts 'odom' -> 'base_link' (or 'base_footprint')."
                ],
                "validation_commands": [
                    "ros2 run tf2_ros tf2_monitor"
                ]
            })

        return {
            "total_frames": len(all_frames),
            "roots": roots,
            "leaves": leaves,
            "all_frames": sorted(list(all_frames)),
            "findings": findings
        }
