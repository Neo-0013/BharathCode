"""
Unit tests for AI client, safety validator, and offline explanation engine.
"""

import pytest
from ai.client import BharatCodeClient
from ai.response_validator import ResponseValidator
from ai.explanation_engine import ExplanationEngine

def test_response_validator_blocks_dangerous_commands():
    validator = ResponseValidator()
    dangerous_text = "To fix this issue, run: rm -rf / and recompile."
    is_safe, sanitized, warnings = validator.validate_and_sanitize(dangerous_text, "TEST-01")
    assert is_safe is False
    assert "[BLOCKED DANGEROUS COMMAND]" in sanitized
    assert len(warnings) > 0

def test_response_validator_permits_safe_ros2_commands():
    validator = ResponseValidator()
    safe_text = (
        "Finding TEST-01 shows missing topic.\n"
        "Run the following verification:\n"
        "ros2 topic info /cmd_vel\n"
        "ros2 node list"
    )
    is_safe, sanitized, warnings = validator.validate_and_sanitize(safe_text, "TEST-01")
    assert is_safe is True
    assert "ros2 topic info" in sanitized

def test_offline_explanation_generation():
    engine = ExplanationEngine()
    mock_finding = {
        "id": "ROBO-TF-001",
        "title": "Disconnected TF2 Tree",
        "category": "TF2 Coordinate Transforms",
        "severity": "CRITICAL",
        "evidence": "Multiple root frames: map, odom",
        "root_cause": "Missing localization transform",
        "troubleshooting": ["Check AMCL node", "Inspect URDF"],
        "validation_commands": ["ros2 run tf2_tools view_frames"]
    }
    res = engine.explain_finding(mock_finding, force_offline=True)
    assert res["offline"] is True
    assert "ROBO-TF-001" in res["explanation"]
    assert "Deterministic Engineering Engine" in res["source"]
    assert "view_frames" in res["explanation"]

def test_client_unconfigured_offline():
    client = BharatCodeClient(api_key="")
    assert client.is_configured() is False
    res = client.generate_chat_completion([{"role": "user", "content": "hi"}])
    assert res["success"] is False
    assert "not configured" in res["error"]

def test_client_http_402_handling(monkeypatch):
    class MockResponse:
        status_code = 402
        text = '{"error":{"message":"Coding and API use need BharatCode Lite (₹399/month, Qwen 3.8 27B) or Pro (₹999/month, Qwen and DeepSeek)."}}'
        def json(self):
            return {"error": {"message": "Coding and API use need BharatCode Lite (₹399/month, Qwen 3.8 27B) or Pro (₹999/month, Qwen and DeepSeek)."}}

    import requests
    monkeypatch.setattr(requests, "post", lambda *args, **kwargs: MockResponse())

    client = BharatCodeClient(api_key="mock_key")
    res = client.test_connection()
    assert res["success"] is False
    assert res["status_code"] == 402
    assert res["is_payment_required"] is True
    assert "BharatCode Plan Required" in res["message"]

def test_ollama_provider_configuration():
    client = BharatCodeClient(provider="ollama", model="qwen2.5-coder:3b")
    assert client.is_configured() is True
    assert "11434" in client.base_url
    assert client.model == "qwen2.5-coder:3b"

def test_gemini_provider_configuration():
    client = BharatCodeClient(provider="gemini", api_key="test_gemini_key", model="gemini-1.5-flash")
    assert client.is_configured() is True
    assert "generativelanguage.googleapis.com" in client.base_url
    assert client.model == "gemini-1.5-flash"
