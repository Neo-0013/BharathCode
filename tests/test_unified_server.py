"""
Tests for the ROBOGUARD AI Unified Platform Server (server.py).
Validates page delivery, API response integrity, scenario switching,
threat simulation, eBPF isolation, and 1-click git patch application.
"""

import asyncio
import json
from server import (
    serve_hero,
    serve_soc,
    redirect_dashboard,
    get_status,
    list_scenarios,
    switch_scenario,
    get_graph,
    trigger_attack,
    isolate_node,
    apply_patch,
    engage_estop,
    export_offline_html,
)


def test_hero_page_route():
    res = asyncio.run(serve_hero())
    assert res.status_code == 200
    text = res.body.decode("utf-8")
    assert "ROBOGUARD AI" in text
    assert "/soc" in text
    assert "THREE" in text


def test_soc_page_route():
    res = asyncio.run(serve_soc())
    assert res.status_code == 200
    text = res.body.decode("utf-8")
    assert "ROS 2 JAZZY" in text
    assert "Critical Vulnerabilities" in text
    assert "Computational Graph" in text
    assert "DDS Telemetry" in text
    assert "FastDDS" in text


def test_dashboard_redirect():
    res = asyncio.run(redirect_dashboard())
    assert res.status_code == 307
    assert res.headers["location"] == "/soc"


def test_api_status():
    res = asyncio.run(get_status())
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert "active_scenario" in data
    assert "posture_score" in data
    assert "wire_throughput" in data


def test_api_scenarios_list():
    res = asyncio.run(list_scenarios())
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert "scenario_1" in data["scenarios"]
    assert "scenario_5" in data["scenarios"]


def test_api_scenario_switch():
    # Switch to Scenario 1 (Baseline Zero-Trust)
    res = asyncio.run(switch_scenario("scenario_1"))
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert data["status"] == "success"
    assert data["scenario"] == "scenario_1"
    assert data["score"] == 96
    assert data["vulns"] == 0

    # Switch back to Scenario 5 (Insecure Fleet)
    res5 = asyncio.run(switch_scenario("scenario_5"))
    assert res5.status_code == 200
    data5 = json.loads(res5.body.decode("utf-8"))
    assert data5["scenario"] == "scenario_5"
    assert data5["score"] == 45
    assert data5["vulns"] == 2


def test_api_graph_payload():
    res = asyncio.run(get_graph())
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 0


def test_api_attack_simulation():
    res = asyncio.run(trigger_attack({"vector": "cmd_vel"}))
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert data["status"] == "active"
    assert data["attack"]["vector"] == "cmd_vel"
    assert "Rogue /cmd_vel" in data["attack"]["alert"]


def test_api_ebpf_isolation():
    res = asyncio.run(isolate_node({"node": "/teleop_keyboard"}))
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert data["status"] == "isolated"
    assert data["node"] == "/teleop_keyboard"
    assert data["ebpf_rule_id"] == 4092


def test_api_git_patch_application():
    res = asyncio.run(apply_patch("SEC-SROS2-001"))
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert data["status"] == "applied"
    assert data["patch_id"] == "SEC-SROS2-001"
    assert data["posture_score"] > 45


def test_api_estop():
    res = asyncio.run(engage_estop())
    assert res.status_code == 200
    data = json.loads(res.body.decode("utf-8"))
    assert data["status"] == "engaged"
    assert data["action"] == "FLEET_ACTUATION_HALT"


def test_api_export_html():
    res = asyncio.run(export_offline_html())
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "attachment" in res.headers["content-disposition"]
    text = res.body.decode("utf-8")
    assert "ROBOGUARD" in text
