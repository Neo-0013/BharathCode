"""Smoke test: every workspace page renders without raising an exception."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parent.parent / "app.py"

PAGES = [
    "📖 Mission Story & 3D Twin",
    "🛡️ 3D Robotics SOC",
    "📊 Command Center",
    "🔬 Diagnostics Workspace",
    "🔐 Cybersecurity Center",
    "🕸️ ROS Graph Explorer",
    "📋 Reports & History",
    "⚙️ Settings & Connectivity",
]


@pytest.mark.parametrize("page", PAGES)
def test_page_renders_without_exception(page):
    at = AppTest.from_file(str(APP), default_timeout=30)
    at.session_state["nav_selection"] = page
    at.run()
    assert not at.exception, [e.value for e in at.exception]
