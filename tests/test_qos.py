"""
Unit tests for QoSAnalyzer in ROBOGUARD AI.
"""

import pytest
from core.qos_analyzer import QoSAnalyzer

def test_qos_reliability_compatible():
    analyzer = QoSAnalyzer()
    # RELIABLE pub can serve RELIABLE sub
    res = analyzer.evaluate_pair(
        topic="/odom",
        pub_node="/wheel_odom",
        sub_node="/ekf_filter",
        pub_qos={"reliability": "RELIABLE", "durability": "VOLATILE"},
        sub_qos={"reliability": "RELIABLE", "durability": "VOLATILE"}
    )
    assert res["is_compatible"] is True
    assert len(res["violations"]) == 0

def test_qos_reliability_incompatible():
    analyzer = QoSAnalyzer()
    # BEST_EFFORT pub CANNOT serve RELIABLE sub
    res = analyzer.evaluate_pair(
        topic="/scan",
        pub_node="/lidar_driver",
        sub_node="/slam_toolbox",
        pub_qos={"reliability": "BEST_EFFORT", "durability": "VOLATILE"},
        sub_qos={"reliability": "RELIABLE", "durability": "VOLATILE"}
    )
    assert res["is_compatible"] is False
    assert len(res["violations"]) == 1
    assert res["violations"][0]["policy"] == "Reliability"

def test_qos_durability_incompatible():
    analyzer = QoSAnalyzer()
    # VOLATILE pub CANNOT serve TRANSIENT_LOCAL sub
    res = analyzer.evaluate_pair(
        topic="/map",
        pub_node="/map_server",
        sub_node="/nav2_costmap",
        pub_qos={"reliability": "RELIABLE", "durability": "VOLATILE"},
        sub_qos={"reliability": "RELIABLE", "durability": "TRANSIENT_LOCAL"}
    )
    assert res["is_compatible"] is False
    assert len(res["violations"]) == 1
    assert res["violations"][0]["policy"] == "Durability"

def test_generate_findings_from_evaluations():
    analyzer = QoSAnalyzer()
    evals = [
        analyzer.evaluate_pair(
            topic="/cmd_vel",
            pub_node="/teleop",
            sub_node="/diff_controller",
            pub_qos={"reliability": "BEST_EFFORT"},
            sub_qos={"reliability": "RELIABLE"}
        )
    ]
    findings = analyzer.generate_findings(evals)
    assert len(findings) == 1
    assert findings[0]["severity"] == "CRITICAL"
    assert "/cmd_vel" in findings[0]["title"]
