"""
ROBOGUARD AI — Configuration & Settings Module
Centralizes application constants, BharatCode model API parameters,
ROS 2 Jazzy specifications, and UI design tokens.
"""

import os
from enum import Enum
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
DEMO_DIR = DATA_DIR / "demo_scenarios"
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Product Metadata
APP_NAME = "ROBOGUARD AI"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Understand your robot. Diagnose its failures. Strengthen its security."
TARGET_ROS_DISTRO = "ROS 2 Jazzy"

# BharatCode Model API Configuration
BHARATCODE_API_BASE = os.getenv("BHARATCODE_API_BASE", "https://bharatcode.ai/api/model/v1")
BHARATCODE_DEFAULT_MODEL = os.getenv("BHARATCODE_MODEL", "deepseek-v4.1-flash")
BHARATCODE_AVAILABLE_MODELS = [
    {"id": "deepseek-v4.1-flash", "name": "BharatCode DeepSeek V4.1 Flash (Recommended for Diagnostics)", "context_window": "128k"},
    {"id": "qwen-3.8-27b", "name": "BharatCode Qwen 3.8 27B (High-Precision Reasoning)", "context_window": "32k"}
]

# Diagnostic Severity
class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

# Diagnostic Categories
class DiagnosticCategory(str, Enum):
    NODE_TOPIC = "Node & Topic Architecture"
    QOS_COMPATIBILITY = "QoS Profile Compatibility"
    TF2_TRANSFORM = "TF2 Coordinate Transforms"
    BUILD_LAUNCH = "Build & Launch Environment"
    SENSOR_NAV = "Sensor & Navigation Stack"
    CYBERSECURITY = "Robotics Cybersecurity & SROS2"

# Confidence Levels
class Confidence(str, Enum):
    CONFIRMED = "Confirmed"
    SUSPECTED = "Suspected"
    INFORMATIONAL = "Informational"

# UI Color Tokens (Anti-AI-slop Dark Slate/Graphite Theme)
UI_THEME = {
    "bg_base": "#0B0D13",
    "bg_surface": "#131620",
    "bg_surface_elevated": "#1B1F2D",
    "border_subtle": "#232A3B",
    "border_strong": "#2E374D",
    "accent_primary": "#00E5FF",      # Telemetry Cyan
    "accent_secondary": "#3B82F6",    # Engineering Blue
    "accent_highlight": "#818CF8",    # Indigo
    "text_primary": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "severity_colors": {
        Severity.CRITICAL: {"color": "#EF4444", "bg": "#3B1417", "border": "#7F1D1D"},
        Severity.HIGH: {"color": "#F97316", "bg": "#38190B", "border": "#7C2D12"},
        Severity.MEDIUM: {"color": "#F59E0B", "bg": "#38290B", "border": "#78350F"},
        Severity.LOW: {"color": "#10B981", "bg": "#0B3020", "border": "#064E3B"},
        Severity.INFO: {"color": "#38BDF8", "bg": "#0C2D42", "border": "#0369A1"}
    }
}
