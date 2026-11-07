"""
Unit tests for TFAnalyzer in ROBOGUARD AI.
"""

import pytest
from core.tf_analyzer import TFAnalyzer

def test_healthy_tf_tree():
    analyzer = TFAnalyzer()
    edges = [
        {"parent": "map", "child": "odom"},
        {"parent": "odom", "child": "base_link"},
        {"parent": "base_link", "child": "laser"}
    ]
    res = analyzer.analyze_tf_tree(edges)
    assert res["total_frames"] == 4
    assert res["roots"] == ["map"]
    assert len(res["findings"]) == 0

def test_disconnected_tf_tree():
    analyzer = TFAnalyzer()
    # map and odom are two independent roots (disjoint trees)
    edges = [
        {"parent": "map", "child": "map_anchor"},
        {"parent": "odom", "child": "base_link"},
        {"parent": "base_link", "child": "laser"}
    ]
    res = analyzer.analyze_tf_tree(edges)
    assert len(res["roots"]) == 2
    assert len(res["findings"]) == 1
    assert "Disconnected TF2 Tree" in res["findings"][0]["title"]
    assert res["findings"][0]["severity"] == "CRITICAL"

def test_missing_base_link_convention():
    analyzer = TFAnalyzer()
    edges = [
        {"parent": "odom", "child": "chassis"}
    ]
    res = analyzer.analyze_tf_tree(edges)
    assert any("REP-105" in f["title"] for f in res["findings"])
