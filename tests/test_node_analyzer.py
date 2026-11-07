"""
Unit tests for NodeAnalyzer in ROBOGUARD AI.
"""

import pytest
from core.node_analyzer import NodeAnalyzer

def test_unconsumed_critical_topic_cmd_vel():
    analyzer = NodeAnalyzer()
    nodes = [{"name": "/teleop_twist_keyboard", "state": "active", "is_lifecycle": False}]
    topics = [
        {
            "name": "/cmd_vel",
            "type": "geometry_msgs/msg/Twist",
            "publishers": ["/teleop_twist_keyboard"],
            "subscribers": []
        }
    ]
    res = analyzer.analyze_topology(nodes, topics)
    assert res["total_nodes"] == 1
    assert res["total_topics"] == 1
    assert len(res["findings"]) == 1
    f = res["findings"][0]
    assert "Critical Topic Unconsumed" in f["title"]
    assert f["severity"] == "CRITICAL"

def test_starved_subscriber_scan():
    analyzer = NodeAnalyzer()
    nodes = [{"name": "/slam_toolbox", "state": "active", "is_lifecycle": True}]
    topics = [
        {
            "name": "/scan",
            "type": "sensor_msgs/msg/LaserScan",
            "publishers": [],
            "subscribers": ["/slam_toolbox"]
        }
    ]
    res = analyzer.analyze_topology(nodes, topics)
    assert len(res["findings"]) == 1
    f = res["findings"][0]
    assert "Starved Subscriber" in f["title"]
    assert f["severity"] == "HIGH"

def test_inactive_lifecycle_node():
    analyzer = NodeAnalyzer()
    nodes = [
        {"name": "/controller_server", "state": "inactive", "is_lifecycle": True}
    ]
    topics = []
    res = analyzer.analyze_topology(nodes, topics)
    assert len(res["findings"]) == 1
    f = res["findings"][0]
    assert "Inactive Lifecycle Node" in f["title"]
    assert f["severity"] == "HIGH"
