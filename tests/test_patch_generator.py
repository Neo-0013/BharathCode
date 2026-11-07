"""
Unit tests for PatchGenerator in ROBOGUARD AI.
"""

import pytest
from core.patch_generator import PatchGenerator

def test_generate_qos_patch():
    finding = {
        "id": "ROBO-QOS-001",
        "title": "QoS Incompatibility on '/cmd_vel': Reliability Mismatch",
        "category": "QoS Profile Compatibility",
        "entities": ["/cmd_vel", "/teleop", "/motor_controller"]
    }
    patch = PatchGenerator.generate_patch(finding)
    assert "patch_filename" in patch
    assert "--- a/" in patch["diff"]
    assert "+++ b/" in patch["diff"]
    assert "ReliabilityPolicy.BEST_EFFORT" in patch["diff"]
    assert "corrected_code" in patch

def test_generate_tf_patch():
    finding = {
        "id": "ROBO-TF-001",
        "title": "Disconnected TF2 Tree: Multiple Root Frames Detected",
        "category": "TF2 Coordinate Transforms",
        "entities": ["map", "odom"]
    }
    patch = PatchGenerator.generate_patch(finding)
    assert "fix_tf2_map_odom_connection.patch" == patch["patch_filename"]
    assert "static_transform_publisher" in patch["diff"]

def test_generate_security_patch():
    finding = {
        "id": "ROBO-SEC-005",
        "title": "DDS Governance Insecurity: Unauthenticated Participants Allowed",
        "category": "Robotics Cybersecurity & SROS2",
        "entities": ["governance.xml"]
    }
    patch = PatchGenerator.generate_patch(finding)
    assert "harden_sros2_governance.patch" == patch["patch_filename"]
    assert "<allow_unauthenticated_participants>false</allow_unauthenticated_participants>" in patch["diff"]
