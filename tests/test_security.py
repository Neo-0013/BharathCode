"""
Unit tests for SecurityEngine in ROBOGUARD AI.
"""

import pytest
from core.security_engine import SecurityEngine

def test_audit_insecure_environment():
    engine = SecurityEngine()
    env = {
        "ROS_SECURITY_ENABLE": "false",
        "ROS_SECURITY_STRATEGY": "Permissive",
        "ROS_DOMAIN_ID": "0",
        "ROS_AUTOMATIC_DISCOVERY_RANGE": "SUBNET"
    }
    findings = engine.audit_environment(env)
    assert len(findings) == 4
    ids = [f["id"] for f in findings]
    assert "ROBO-SEC-001" in ids  # Disabled SROS2
    assert "ROBO-SEC-002" in ids  # Permissive strategy
    assert "ROBO-SEC-003" in ids  # Domain 0
    assert "ROBO-SEC-004" in ids  # Subnet discovery

def test_audit_secure_environment():
    engine = SecurityEngine()
    env = {
        "ROS_SECURITY_ENABLE": "true",
        "ROS_SECURITY_STRATEGY": "Enforce",
        "ROS_DOMAIN_ID": "42",
        "ROS_AUTOMATIC_DISCOVERY_RANGE": "LOCALHOST"
    }
    findings = engine.audit_environment(env)
    assert len(findings) == 0

def test_audit_dds_xml_wildcard_and_unauth():
    engine = SecurityEngine()
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <dds>
      <governance>
        <domain_rule>
          <allow_unauthenticated_participants>true</allow_unauthenticated_participants>
          <discovery_protection>NONE</discovery_protection>
        </domain_rule>
      </governance>
      <permissions>
        <grant name="test">
          <allow_rule>
            <publish><topic>*</topic></publish>
          </allow_rule>
        </grant>
      </permissions>
    </dds>"""
    findings = engine.audit_dds_xml_configuration(xml)
    assert len(findings) == 3
    ids = [f["id"] for f in findings]
    assert "ROBO-SEC-005" in ids
    assert "ROBO-SEC-006" in ids
    assert "ROBO-SEC-007" in ids

def test_calculate_posture_score():
    engine = SecurityEngine()
    mock_findings = [
        {"id": "F1", "severity": "CRITICAL"},  # -25
        {"id": "F2", "severity": "HIGH"}       # -15
    ]
    posture = engine.calculate_posture_score(mock_findings)
    assert posture["score"] == 60.0
    assert posture["risk_tier"] == "ELEVATED RISK"
    assert posture["deductions_applied"] == 40.0
