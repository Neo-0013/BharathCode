"""
Unit tests for core.dynamic_graph_generator
Tests NetworkX directed graph generation, spring layout computation,
QoS error tagging, and JSON/Plotly export formats.
"""

import pytest
import networkx as nx
from core.dynamic_graph_generator import DynamicGraphGenerator


def test_build_networkx_graph_default():
    gen = DynamicGraphGenerator()
    G = gen.build_networkx_graph()
    
    assert isinstance(G, nx.DiGraph)
    assert len(G.nodes) > 0
    assert len(G.edges) > 0
    
    # Check that nodes and topics are distinct types
    nodes = [n for n, d in G.nodes(data=True) if d.get("type") == "node"]
    topics = [n for n, d in G.nodes(data=True) if d.get("type") == "topic"]
    
    assert len(nodes) >= 4
    assert len(topics) >= 3


def test_qos_incompatibility_edge_tagging():
    gen = DynamicGraphGenerator()
    scenario = {
        "nodes": [
            {"name": "/bad_pub", "state": "active"},
            {"name": "/strict_sub", "state": "active"}
        ],
        "topics": [
            {
                "name": "/telemetry",
                "type": "std_msgs/msg/String",
                "rate_hz": 10.0,
                "publishers": ["/bad_pub"],
                "subscribers": ["/strict_sub"]
            }
        ],
        "qos_evaluations": [
            {
                "topic": "/telemetry",
                "status": "INCOMPATIBLE"
            }
        ]
    }
    
    G = gen.build_networkx_graph(scenario)
    
    # Check that topic -> strict_sub edge is tagged as an error
    edge_data = G.get_edge_data("topic:/telemetry", "node:/strict_sub")
    assert edge_data is not None
    assert edge_data["error"] is True
    assert edge_data["qos_status"] == "INCOMPATIBLE"


def test_export_graph_json_structure():
    gen = DynamicGraphGenerator()
    data = gen.export_graph_json()
    
    assert "nodes" in data
    assert "edges" in data
    assert "stats" in data
    assert data["stats"]["total_nodes"] > 0
    assert data["stats"]["total_topics"] > 0
    
    # Verify node coordinate format
    first_node = data["nodes"][0]
    assert "x" in first_node
    assert "y" in first_node
    assert isinstance(first_node["x"], (int, float))
    assert isinstance(first_node["y"], (int, float))


def test_render_plotly_figure():
    gen = DynamicGraphGenerator()
    fig = gen.render_plotly_figure()
    
    assert fig is not None
    # 2 line traces (normal and error) + 1 marker trace
    assert len(fig.data) == 3
