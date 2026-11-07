"""
Unit tests for LogParser in ROBOGUARD AI.
"""

import pytest
from core.log_parser import LogParser, LogEntry

def test_parse_standard_ros2_log_lines():
    parser = LogParser()
    raw = (
        "[INFO] [1715420100.123] [nav2_bringup]: Starting Nav2 bringup\n"
        "[ERROR] [1715420102.456] [controller_server]: Lifecycle node failed to activate"
    )
    entries = parser.parse_lines(raw)
    assert len(entries) == 2
    assert entries[0].level == "INFO"
    assert entries[0].logger == "nav2_bringup"
    assert "Starting Nav2" in entries[0].message
    assert entries[1].level == "ERROR"
    assert entries[1].logger == "controller_server"

def test_multiline_traceback_parsing():
    parser = LogParser()
    raw = (
        "Traceback (most recent call last):\n"
        "  File \"test.py\", line 4, in <module>\n"
        "    import missing_pkg\n"
        "ModuleNotFoundError: No module named 'missing_pkg'"
    )
    entries = parser.parse_lines(raw)
    assert len(entries) >= 1
    assert any("ModuleNotFoundError" in e.message for e in entries)

def test_match_tf_lookup_exception():
    parser = LogParser()
    raw = '[ERROR] [1715420102.110] [amcl]: tf2.LookupException: "base_link" passed to lookupTransform argument target_frame does not exist'
    findings = parser.match_rules(raw)
    assert len(findings) >= 1
    f = findings[0]
    assert f["id"] == "LOG-TF-001"
    assert f["severity"] == "HIGH"
    assert "base_link" in f["entities"]

def test_match_qos_reliability_mismatch_log():
    parser = LogParser()
    raw = "[ERROR] [1715420105.340] [rmw_fastrtps_cpp]: New subscription discovered on topic '/cmd_vel' requesting RELIABLE reliability but offered BEST_EFFORT reliability. QoS profiles are incompatible."
    findings = parser.match_rules(raw)
    assert len(findings) >= 1
    f = findings[0]
    assert f["id"] == "LOG-QOS-001"
    assert f["severity"] == "CRITICAL"

def test_empty_log_handling():
    parser = LogParser()
    assert parser.parse_lines("") == []
    assert parser.match_rules("") == []
    assert parser.parse_lines("   \n\n  ") == []
