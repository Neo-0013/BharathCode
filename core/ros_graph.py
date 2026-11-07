"""
ROBOGUARD AI — ROS 2 Communication Architecture Graph Engine
Builds NetworkX directed multigraphs from ROS 2 topology data and renders
interactive Plotly visualizations showing nodes, topics, publishers, subscribers,
isolated components, and QoS mismatch warning edges.
"""

import networkx as nx
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Tuple
from config.settings import UI_THEME

class ROSGraphBuilder:
    """Builds and analyzes ROS 2 computational graph topologies."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_data(self, nodes: List[Dict[str, Any]], topics: List[Dict[str, Any]],
                        qos_incompatibilities: Optional[List[Dict[str, Any]]] = None) -> nx.DiGraph:
        """
        Builds a directed NetworkX graph:
        Node -> Topic (publishes)
        Topic -> Node (subscribes)
        """
        self.graph.clear()
        qos_incompatibilities = qos_incompatibilities or []

        # Add ROS Nodes
        for n in nodes:
            node_name = n.get("name", "")
            if not node_name:
                continue
            is_lifecycle = n.get("is_lifecycle", False)
            state = n.get("state", "active").lower()
            self.graph.add_node(
                node_name,
                node_type="ros_node",
                is_lifecycle=is_lifecycle,
                state=state,
                namespace=n.get("namespace", "/")
            )

        # Set of incompatible (pub, sub, topic) triples
        incompat_pairs = set()
        for inc in qos_incompatibilities:
            t = inc.get("topic")
            p = inc.get("publisher")
            s = inc.get("subscriber")
            if t and p and s:
                incompat_pairs.add((p, t, s))

        # Add Topics and Edges
        for t in topics:
            topic_name = t.get("name", "")
            if not topic_name:
                continue
            msg_type = t.get("type", "unknown_type")
            self.graph.add_node(
                topic_name,
                node_type="ros_topic",
                msg_type=msg_type
            )

            # Publishers: Node -> Topic
            for pub in t.get("publishers", []):
                if pub not in self.graph:
                    self.graph.add_node(pub, node_type="ros_node", state="active", is_lifecycle=False)
                self.graph.add_edge(pub, topic_name, edge_type="publishes")

            # Subscribers: Topic -> Node
            for sub in t.get("subscribers", []):
                if sub not in self.graph:
                    self.graph.add_node(sub, node_type="ros_node", state="active", is_lifecycle=False)
                has_qos_err = any((p, topic_name, sub) in incompat_pairs for p in t.get("publishers", []))
                self.graph.add_edge(topic_name, sub, edge_type="subscribes", qos_error=has_qos_err)

        return self.graph

    def get_topology_statistics(self) -> Dict[str, Any]:
        """Calculates graph metrics and disconnected components."""
        if len(self.graph) == 0:
            return {"total_nodes": 0, "total_topics": 0, "disconnected_components": 0, "orphaned_nodes": []}

        ros_nodes = [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == "ros_node"]
        ros_topics = [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == "ros_topic"]

        # Undirected view for connected components
        undirected = self.graph.to_undirected()
        components = list(nx.connected_components(undirected))
        
        # Isolated / orphaned entities (degree 0)
        orphaned = [n for n in self.graph.nodes() if self.graph.degree(n) == 0]

        return {
            "total_nodes": len(ros_nodes),
            "total_topics": len(ros_topics),
            "total_edges": self.graph.number_of_edges(),
            "connected_components_count": len(components),
            "orphaned_entities": orphaned
        }

    def render_plotly(self) -> go.Figure:
        """Renders an interactive Plotly graph figure with dark telemetry styling."""
        if len(self.graph) == 0:
            fig = go.Figure()
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor=UI_THEME["bg_base"],
                plot_bgcolor=UI_THEME["bg_base"],
                annotations=[{
                    "text": "No ROS 2 graph data available. Upload a log or load a demonstration scenario.",
                    "xref": "paper", "yref": "paper",
                    "showarrow": False, "font": {"size": 14, "color": UI_THEME["text_muted"]}
                }]
            )
            return fig

        # Compute Spring Layout
        pos = nx.spring_layout(self.graph, k=0.8, iterations=60, seed=42)

        # Build Edges
        edge_x_normal, edge_y_normal = [], []
        edge_x_error, edge_y_error = [], []

        for u, v, d in self.graph.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            if d.get("qos_error", False):
                edge_x_error.extend([x0, x1, None])
                edge_y_error.extend([y0, y1, None])
            else:
                edge_x_normal.extend([x0, x1, None])
                edge_y_normal.extend([y0, y1, None])

        edge_trace_normal = go.Scatter(
            x=edge_x_normal, y=edge_y_normal,
            line=dict(width=1.5, color="rgba(100, 116, 139, 0.45)"),
            hoverinfo='none',
            mode='lines'
        )

        edge_trace_error = go.Scatter(
            x=edge_x_error, y=edge_y_error,
            line=dict(width=3.0, color="#EF4444", dash="dot"),
            hoverinfo='none',
            mode='lines',
            name="QoS Incompatibility Edge"
        )

        # Build Nodes
        node_x, node_y = [], []
        node_colors = []
        node_symbols = []
        node_sizes = []
        node_hover_texts = []
        node_labels = []

        for node, d in self.graph.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            ntype = d.get("node_type", "ros_node")
            
            if ntype == "ros_node":
                state = d.get("state", "active")
                is_lifecycle = d.get("is_lifecycle", False)
                node_symbols.append("circle")
                node_sizes.append(26)
                node_labels.append(node.split("/")[-1] or node)

                if state == "active":
                    node_colors.append("#10B981")  # Emerald green
                elif state in ["inactive", "unconfigured"]:
                    node_colors.append("#F59E0B")  # Amber warning
                else:
                    node_colors.append("#EF4444")  # Red error

                node_hover_texts.append(
                    f"<b>Node:</b> {node}<br>"
                    f"<b>Type:</b> ROS 2 Executable Node<br>"
                    f"<b>Lifecycle:</b> {'Yes' if is_lifecycle else 'Standard'}<br>"
                    f"<b>State:</b> {state.upper()}<br>"
                    f"<b>Connections:</b> {self.graph.degree(node)}"
                )
            else:  # ros_topic
                node_symbols.append("diamond")
                node_sizes.append(20)
                node_colors.append("#00E5FF")  # Telemetry cyan
                node_labels.append(node.split("/")[-1] or node)
                node_hover_texts.append(
                    f"<b>Topic:</b> {node}<br>"
                    f"<b>Type:</b> {d.get('msg_type', 'unknown')}<br>"
                    f"<b>Publishers:</b> {self.graph.in_degree(node)}<br>"
                    f"<b>Subscribers:</b> {self.graph.out_degree(node)}"
                )

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_labels,
            textposition="bottom center",
            textfont=dict(size=10, color="#CBD5E1", family="monospace"),
            hoverinfo='text',
            hovertext=node_hover_texts,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                symbol=node_symbols,
                line=dict(width=1.5, color="#0B0D13")
            )
        )

        fig = go.Figure(
            data=[edge_trace_normal, edge_trace_error, node_trace],
            layout=go.Layout(
                template="plotly_dark",
                paper_bgcolor=UI_THEME["bg_base"],
                plot_bgcolor=UI_THEME["bg_surface"],
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=20, r=20, t=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=560
            )
        )

        return fig
