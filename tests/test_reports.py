"""
Unit tests for ReportGenerator in ROBOGUARD AI.
"""

import pytest
from pathlib import Path
from core.report_generator import ReportGenerator

def test_generate_markdown_report():
    gen = ReportGenerator()
    mock_res = {
        "findings": [
            {
                "id": "ROBO-TEST-001",
                "title": "Test Defect",
                "category": "QoS Profile Compatibility",
                "severity": "CRITICAL",
                "evidence": "Pub offered Best Effort, Sub requested Reliable",
                "root_cause": "DDS QoS Mismatch",
                "troubleshooting": ["Fix subscriber QoS"],
                "validation_commands": ["ros2 topic info -v /test"]
            }
        ],
        "severity_counts": {"CRITICAL": 1, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0},
        "security_score": {"score": 75.0, "risk_tier": "ACCEPTABLE WITH DEFECTS"}
    }
    md = gen.generate_markdown(mock_res)
    assert "# ROBOGUARD AI" in md
    assert "ROBO-TEST-001" in md
    assert "CRITICAL" in md
    assert "ros2 topic info -v /test" in md

def test_generate_pdf_report(tmp_path):
    gen = ReportGenerator(output_dir=tmp_path)
    mock_res = {
        "findings": [
            {
                "id": "ROBO-TEST-001",
                "title": "Test Defect",
                "category": "General",
                "severity": "CRITICAL",
                "evidence": "Snippet",
                "root_cause": "Root cause",
                "troubleshooting": ["Step 1"],
                "validation_commands": ["ros2 topic list"]
            }
        ],
        "severity_counts": {"CRITICAL": 1},
        "security_score": {"score": 80.0, "risk_tier": "HARDENED"}
    }
    pdf_file = tmp_path / "test_report.pdf"
    res_path = gen.generate_pdf(mock_res, pdf_file)
    assert res_path.exists()
    assert res_path.stat().st_size > 1000  # PDF generated with content
