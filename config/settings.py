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

# AI Provider Configurations
AI_PROVIDERS = {
    "ollama": {
        "name": "Local Ollama (100% Free / Localhost)",
        "base_url": os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1"),
        "default_model": "qwen2.5-coder:3b",
        "requires_key": False,
        "models": [
            {"id": "qwen2.5-coder:3b", "name": "Qwen 2.5 Coder 3B (Pre-installed & Active)", "context_window": "32k"},
            {"id": "nemotron-mini:latest", "name": "NVIDIA Nemotron Mini 4.2B (Pre-installed)", "context_window": "4k"},
            {"id": "llama3:latest", "name": "Meta Llama 3 (Local)", "context_window": "8k"}
        ]
    },
    "gemini": {
        "name": "Google Gemini API (Generous Free Tier)",
        "base_url": os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai"),
        "default_model": "gemini-1.5-flash",
        "requires_key": True,
        "models": [
            {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash (Fast, Free Tier 15 RPM)", "context_window": "1M"},
            {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash (Next-Gen Fast Reasoning)", "context_window": "1M"},
            {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro (Deep Engineering Analysis)", "context_window": "2M"}
        ]
    },
    "bharatcode": {
        "name": "BharatCode Model API (Competition Official)",
        "base_url": os.getenv("BHARATCODE_API_BASE", "https://bharatcode.ai/api/model/v1"),
        "default_model": "deepseek-v4.1-flash",
        "requires_key": True,
        "models": [
            {"id": "qwen-3.8-27b", "name": "BharatCode Qwen 3.8 27B (Free for verified students)", "context_window": "32k"},
            {"id": "deepseek-v4.1-flash", "name": "BharatCode DeepSeek V4.1 Flash (Pro tier)", "context_window": "128k"}
        ]
    }
}

# Legacy BharatCode aliases for backwards compatibility
BHARATCODE_API_BASE = AI_PROVIDERS["bharatcode"]["base_url"]
BHARATCODE_DEFAULT_MODEL = AI_PROVIDERS["bharatcode"]["default_model"]
BHARATCODE_AVAILABLE_MODELS = AI_PROVIDERS["bharatcode"]["models"]

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

# UI Color Tokens (Classic Tremor Light System: White/Slate Surfaces, Cobalt Accents)
UI_THEME = {
    "bg_base": "#F8FAFC",
    "bg_surface": "#FFFFFF",
    "bg_surface_elevated": "#FFFFFF",
    "border_subtle": "#E2E8F0",
    "border_strong": "#CBD5E1",
    "accent_primary": "#2563EB",      # Cobalt Blue
    "accent_secondary": "#0284C7",    # Sky Cyan
    "accent_highlight": "#4F46E5",    # Indigo
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#64748B",
    "severity_colors": {
        Severity.CRITICAL: {"color": "#DC2626", "bg": "#FEF2F2", "border": "#FECACA"},
        Severity.HIGH: {"color": "#D97706", "bg": "#FFFBEB", "border": "#FDE68A"},
        Severity.MEDIUM: {"color": "#D97706", "bg": "#FFFBEB", "border": "#FDE68A"},
        Severity.LOW: {"color": "#059669", "bg": "#ECFDF5", "border": "#A7F3D0"},
        Severity.INFO: {"color": "#2563EB", "bg": "#EFF6FF", "border": "#BFDBFE"}
    }
}
