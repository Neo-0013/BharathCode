"""
ROBOGUARD AI — Dynamic Python Computational Graph Engine
Generates interactive, physics-based directed graphs (NetworkX + Plotly)
modeling ROS 2 node topologies, topic pipelines, QoS contract compatibility,
and live packet flow rates.
"""

from typing import Dict, Any, List, Optional
import networkx as nx
import plotly.graph_objects as go
from config.settings import UI_THEME


class DynamicGraphGenerator:
    """Computes dynamic ROS 2 computational graph topologies and physics layouts."""

    def __init__(self):
        self.theme = UI_THEME

    def build_networkx_graph(self, scenario_data: Optional[Dict[str, Any]] = None) -> nx.DiGraph:
        """
        Builds a NetworkX DiGraph representing ROS 2 nodes, topics, and directional edges.
        Evaluates QoS policies between publishers and subscribers to flag incompatible edges.
        """
        G = nx.DiGraph()

        if not scenario_data:
            scenario_data = self._get_default_scenario_data()

        nodes_data = scenario_data.get("nodes", [])
        topics_data = scenario_data.get("topics", [])
        qos_evals = scenario_data.get("qos_evaluations", [])

        # 1. Add Node vertices
        for node in nodes_data:
            node_id = f"node:{node['name']}"
            G.add_node(
                node_id,
                label=node["name"],
                type="node",
                state=node.get("state", "active"),
                lifecycle=node.get("lifecycle", False),
                enclave=node.get("enclave", "default"),
                compromised=node.get("compromised", False),
                color="#059669" if node.get("state") == "active" else ("#DC2626" if node.get("compromised") else "#D97706")
            )

        # 2. Add Topic vertices
        for topic in topics_data:
            topic_id = f"topic:{topic['name']}"
            is_unconsumed = topic.get("subscribers_count", 1) == 0
            is_starved = topic.get("publishers_count", 1) == 0
            
            topic_color = "#0284C7"
            if is_unconsumed or is_starved:
                topic_color = "#DC2626"

            G.add_node(
                topic_id,
                label=topic["name"],
                type="topic",
                msg_type=topic.get("type", "std_msgs/msg/Header"),
                rate_hz=topic.get("rate_hz", 10.0),
                unconsumed=is_unconsumed,
                starved=is_starved,
                color=topic_color
            )

            # Add publisher edges: Node -> Topic
            for pub in topic.get("publishers", []):
                pub_node_id = f"node:{pub}"
                if not G.has_node(pub_node_id):
                    G.add_node(pub_node_id, label=pub, type="node", state="active", color="#059669")
                G.add_edge(pub_node_id, topic_id, edge_type="publishes", error=False, qos_status="COMPATIBLE")

            # Add subscriber edges: Topic -> Node
            for sub in topic.get("subscribers", []):
                sub_node_id = f"node:{sub}"
                if not G.has_node(sub_node_id):
                    G.add_node(sub_node_id, label=sub, type="node", state="active", color="#059669")
                
                # Check for QoS incompatibility on this topic
                has_qos_error = any(
                    q.get("topic") == topic["name"] and q.get("status") == "INCOMPATIBLE"
                    for q in qos_evals
                )
                G.add_edge(
                    topic_id, 
                    sub_node_id, 
                    edge_type="subscribes", 
                    error=has_qos_error,
                    qos_status="INCOMPATIBLE" if has_qos_error else "COMPATIBLE"
                )

        return G

    def compute_spring_layout(self, G: nx.DiGraph) -> Dict[str, List[float]]:
        """Calculates 2D spring force-directed layout coordinates for graph vertices."""
        if len(G.nodes) == 0:
            return {}
        pos = nx.spring_layout(G, k=1.8, iterations=60, seed=42)
        # Normalize coordinates into 0-1000 viewport range
        x_vals = [p[0] for p in pos.values()]
        y_vals = [p[1] for p in pos.values()]
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        range_x = max_x - min_x if max_x != min_x else 1.0
        range_y = max_y - min_y if max_y != min_y else 1.0

        normalized_pos = {}
        for node_id, (x, y) in pos.items():
            norm_x = 80 + ((x - min_x) / range_x) * 840
            norm_y = 60 + ((y - min_y) / range_y) * 480
            normalized_pos[node_id] = [round(norm_x, 1), round(norm_y, 1)]

        return normalized_pos

    def export_graph_json(self, scenario_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Exports graph nodes, edges, and computed positions as a structured JSON dict
        for real-time consumption by the frontend physics simulation.
        """
        G = self.build_networkx_graph(scenario_data)
        pos = self.compute_spring_layout(G)

        nodes_list = []
        for n_id, attrs in G.nodes(data=True):
            p = pos.get(n_id, [500, 300])
            nodes_list.append({
                "id": n_id,
                "label": attrs.get("label", n_id),
                "type": attrs.get("type", "node"),
                "state": attrs.get("state", "active"),
                "color": attrs.get("color", "#059669"),
                "rate_hz": attrs.get("rate_hz", 0),
                "msg_type": attrs.get("msg_type", ""),
                "x": p[0],
                "y": p[1]
            })

        edges_list = []
        for u, v, attrs in G.edges(data=True):
            edges_list.append({
                "from": u,
                "to": v,
                "type": attrs.get("edge_type", "publishes"),
                "error": attrs.get("error", False),
                "qos_status": attrs.get("qos_status", "COMPATIBLE")
            })

        return {
            "nodes": nodes_list,
            "edges": edges_list,
            "stats": {
                "total_nodes": sum(1 for n in nodes_list if n["type"] == "node"),
                "total_topics": sum(1 for n in nodes_list if n["type"] == "topic"),
                "total_edges": len(edges_list),
                "error_edges": sum(1 for e in edges_list if e["error"])
            }
        }

    def render_plotly_figure(self, scenario_data: Optional[Dict[str, Any]] = None) -> go.Figure:
        """Renders an interactive Plotly dynamic computational graph for Streamlit."""
        G = self.build_networkx_graph(scenario_data)
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

        # Edge traces (Normal vs Error)
        normal_edge_x, normal_edge_y = [], []
        error_edge_x, error_edge_y = [], []

        for u, v, data in G.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            if data.get("error"):
                error_edge_x.extend([x0, x1, None])
                error_edge_y.extend([y0, y1, None])
            else:
                normal_edge_x.extend([x0, x1, None])
                normal_edge_y.extend([y0, y1, None])

        edge_trace_normal = go.Scatter(
            x=normal_edge_x, y=normal_edge_y,
            line=dict(width=1.5, color='#334155'),
            hoverinfo='none',
            mode='lines'
        )

        edge_trace_error = go.Scatter(
            x=error_edge_x, y=error_edge_y,
            line=dict(width=3, color='#EF4444', dash='dash'),
            hoverinfo='none',
            mode='lines'
        )

        # Node traces
        node_x, node_y, node_color, node_text, node_symbol, node_size = [], [], [], [], [], []

        for node_id, data in G.nodes(data=True):
            x, y = pos[node_id]
            node_x.append(x)
            node_y.append(y)
            is_topic = data.get("type") == "topic"
            
            node_symbol.append("diamond" if is_topic else "circle")
            node_size.append(18 if is_topic else 24)
            node_color.append(data.get("color", "#059669"))
            
            hover_text = (
                f"<b>{'Topic' if is_topic else 'Node'}:</b> {data.get('label')}<br>"
                f"Type: {data.get('msg_type', 'ROS Node')}<br>"
                f"Status: {data.get('state', 'Active')}"
            )
            node_text.append(hover_text)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=node_text,
            text=[G.nodes[n].get("label", n).split('/')[-1] for n in G.nodes()],
            textposition="top center",
            textfont=dict(family="JetBrains Mono", size=10, color="#0F172A"),
            marker=dict(
                size=node_size,
                color=node_color,
                symbol=node_symbol,
                line=dict(width=1.5, color="#CBD5E1")
            )
        )

        fig = go.Figure(
            data=[edge_trace_normal, edge_trace_error, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=20, r=20, t=30),
                paper_bgcolor='rgba(11,13,19,0)',
                plot_bgcolor='rgba(11,13,19,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=480
            )
        )
        return fig

    def _get_default_scenario_data(self) -> Dict[str, Any]:
        """Provides default AMR navigation scenario data if none is loaded."""
        return {
            "nodes": [
                {"name": "/teleop_keyboard", "state": "active", "enclave": "/teleop_enclave"},
                {"name": "/planner_server", "state": "active", "enclave": "/nav_enclave"},
                {"name": "/controller_server", "state": "active", "lifecycle": True, "enclave": "/nav_enclave"},
                {"name": "/diff_drive_base", "state": "active", "enclave": "/hardware_enclave"},
                {"name": "/lidar_driver", "state": "active", "enclave": "/sensors_enclave"},
                {"name": "/camera_driver", "state": "active", "enclave": "/sensors_enclave"},
                {"name": "/sros2_sentinel", "state": "active", "enclave": "/sec_enclave"}
            ],
            "topics": [
                {
                    "name": "/cmd_vel",
                    "type": "geometry_msgs/msg/Twist",
                    "rate_hz": 20.0,
                    "publishers": ["/teleop_keyboard", "/planner_server"],
                    "subscribers": ["/controller_server", "/diff_drive_base"],
                    "publishers_count": 2,
                    "subscribers_count": 2
                },
                {
                    "name": "/scan",
                    "type": "sensor_msgs/msg/LaserScan",
                    "rate_hz": 15.0,
                    "publishers": ["/lidar_driver"],
                    "subscribers": ["/planner_server"],
                    "publishers_count": 1,
                    "subscribers_count": 1
                },
                {
                    "name": "/camera/image_raw",
                    "type": "sensor_msgs/msg/Image",
                    "rate_hz": 30.0,
                    "publishers": ["/camera_driver"],
                    "subscribers": [],
                    "publishers_count": 1,
                    "subscribers_count": 0
                },
                {
                    "name": "/tf",
                    "type": "tf2_msgs/msg/TFMessage",
                    "rate_hz": 50.0,
                    "publishers": ["/diff_drive_base"],
                    "subscribers": ["/planner_server", "/controller_server"],
                    "publishers_count": 1,
                    "subscribers_count": 2
                }
            ],
            "qos_evaluations": [
                {
                    "topic": "/cmd_vel",
                    "offered_reliability": "BEST_EFFORT",
                    "requested_reliability": "RELIABLE",
                    "status": "INCOMPATIBLE"
                }
            ]
        }
