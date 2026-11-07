"""
Unit tests for the master DiagnosticEngine in ROBOGUARD AI.
"""

import pytest
import json
from pathlib import Path
from core.diagnostic_engine import DiagnosticEngine
from config.settings import DEMO_DIR

def test_analyze_raw_log():
    engine = DiagnosticEngine()
    log = (
        "[ERROR] [1715420102.110] [amcl]: tf2.LookupException: \"base_link\" passed to lookupTransform argument target_frame does not exist\n"
        "[ERROR] [1715420105.340] [rmw_fastrtps_cpp]: New subscription discovered on topic '/cmd_vel' requesting RELIABLE reliability but offered BEST_EFFORT reliability. QoS profiles are incompatible."
    )
    res = engine.parse_input_auto(log, "test.log")
    assert res["total_findings"] >= 2
    assert res["summary"]["CRITICAL"] >= 1
    assert res["summary"]["HIGH"] >= 1

def test_analyze_demo_scenarios():
    engine = DiagnosticEngine()
    scenario_files = list(DEMO_DIR.glob("*.json"))
    assert len(scenario_files) == 5

    for sf in scenario_files:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
            res = engine.analyze_structured_scenario(data)
            assert res["total_findings"] > 0
            assert "security_score" in res
            assert "summary" in res

def test_parse_input_auto_yaml():
    engine = DiagnosticEngine()
    yaml_content = """
raw_log: |
  [ERROR] [1715420102.110] [amcl]: tf2.LookupException: "base_link" passed to lookupTransform argument target_frame does not exist
nodes:
  - name: /test_node
    state: active
"""
    res = engine.parse_input_auto(yaml_content, "config.yaml")
    assert res["total_findings"] >= 1
