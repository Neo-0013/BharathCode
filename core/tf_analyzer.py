"""
ROBOGUARD AI — TF2 Coordinate Transform Engine
Diagnoses TF2 transform tree disconnections, missing frames,
REP-105 convention violations, and Lookup/Extrapolation exceptions.
"""

from typing import Dict, Any, List, Set, Optional
import networkx as nx
import plotly.graph_objects as go
from config.settings import Severity, DiagnosticCategory, Confidence, UI_THEME

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

    def render_plotly_tree(self, edges: List[Dict[str, str]]) -> go.Figure:
        """Renders an interactive hierarchical TF2 transform tree figure in Plotly."""
        if not edges:
            fig = go.Figure()
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor=UI_THEME["bg_base"],
                plot_bgcolor=UI_THEME["bg_base"],
                annotations=[{
                    "text": "No TF2 transform edges available in this scenario.",
                    "xref": "paper", "yref": "paper",
                    "showarrow": False, "font": {"size": 14, "color": UI_THEME["text_muted"]}
                }]
            )
            return fig

        G = nx.DiGraph()
        for e in edges:
            p = e.get("parent")
            c = e.get("child")
            if p and c:
                G.add_edge(p, c)

        # Compute positions using spring or multipartite layout
        pos = nx.spring_layout(G, k=1.0, iterations=50, seed=42)

        # Roots
        roots = [n for n in G.nodes() if G.in_degree(n) == 0]
        has_multiple_roots = len(roots) > 1

        # Draw Edges
        edge_x, edge_y = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2.5, color="rgba(0, 229, 255, 0.45)"),
            hoverinfo='none',
            mode='lines'
        )

        # Draw Nodes
        node_x, node_y = [], []
        node_colors = []
        node_sizes = []
        node_labels = []
        hover_texts = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_labels.append(node)

            is_rep105 = node in self.REP_105_STANDARD_FRAMES
            is_root = node in roots

            if is_root and has_multiple_roots:
                node_colors.append("#EF4444")  # Disconnected root warning
                node_sizes.append(28)
            elif is_rep105:
                node_colors.append("#00E5FF")  # Cyan standard frame
                node_sizes.append(24)
            else:
                node_colors.append("#10B981")  # Emerald sensor frame
                node_sizes.append(20)

            parent = list(G.predecessors(node))
            children = list(G.successors(node))
            hover_texts.append(
                f"<b>Frame:</b> {node}<br>"
                f"<b>Convention:</b> {'REP-105 Canonical' if is_rep105 else 'Sensor/Attachment'}<br>"
                f"<b>Parent:</b> {parent[0] if parent else 'ROOT (No Parent)'}<br>"
                f"<b>Children:</b> {len(children)} frames"
            )

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_labels,
            textposition="bottom center",
            textfont=dict(size=11, color="#F8FAFC", family="monospace"),
            hoverinfo='text',
            hovertext=hover_texts,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color="#0B0D13")
            )
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                template="plotly_dark",
                paper_bgcolor=UI_THEME["bg_base"],
                plot_bgcolor=UI_THEME["bg_surface"],
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=20, r=20, t=30),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=450,
                title=dict(
                    text="<b>TF2 Coordinate Transform Tree (REP-105)</b>",
                    font=dict(size=14, color="#E2E8F0")
                )
            )
        )
        return fig
