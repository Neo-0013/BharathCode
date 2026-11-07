"""
ROBOGUARD AI — UI Styles & Design Tokens Module
Injects bespoke CSS into Streamlit to deliver an enterprise-grade,
anti-AI-slop developer tooling aesthetic inspired by modern AI observability
dashboards and Linear ergonomics.
"""

import streamlit as st
from config.settings import UI_THEME

def inject_custom_styles():
    """Injects high-fidelity custom CSS styles into the Streamlit DOM."""
    css = f"""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Reset & Base Theme */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {UI_THEME['bg_base']} !important;
        color: {UI_THEME['text_primary']} !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        overflow-x: clip !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {UI_THEME['bg_surface']} !important;
        border-right: 1px solid {UI_THEME['border_subtle']} !important;
    }}
    [data-testid="stSidebar"] * {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* Top Header Bar */
    header[data-testid="stHeader"] {{
        background-color: {UI_THEME['bg_base']} !important;
        border-bottom: 1px solid {UI_THEME['border_subtle']} !important;
    }}

    /* Main Container Padding */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1300px !important;
    }}

    /* Reusable Card */
    .rg-card {{
        background-color: {UI_THEME['bg_surface']};
        border: 1px solid {UI_THEME['border_subtle']};
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .rg-card:hover {{
        border-color: {UI_THEME['border_strong']};
    }}

    .rg-card-elevated {{
        background-color: {UI_THEME['bg_surface_elevated']};
        border: 1px solid {UI_THEME['border_strong']};
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }}

    /* Observability Stat Cards */
    .rg-stat-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }}
    .rg-stat-card {{
        background-color: {UI_THEME['bg_surface']};
        border: 1px solid {UI_THEME['border_subtle']};
        border-radius: 8px;
        padding: 1rem;
    }}
    .rg-stat-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {UI_THEME['text_secondary']};
        margin-bottom: 0.35rem;
    }}
    .rg-stat-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {UI_THEME['text_primary']};
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }}
    .rg-stat-badge {{
        font-size: 0.75rem;
        padding: 0.15rem 0.45rem;
        border-radius: 9999px;
        font-weight: 600;
    }}
    .badge-green {{
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .badge-orange {{
        background-color: rgba(249, 115, 22, 0.15);
        color: #F97316;
        border: 1px solid rgba(249, 115, 22, 0.3);
    }}
    .badge-red {{
        background-color: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .badge-cyan {{
        background-color: rgba(0, 229, 255, 0.15);
        color: #00E5FF;
        border: 1px solid rgba(0, 229, 255, 0.3);
    }}

    /* AI Copilot Highlight Banner */
    .rg-ai-banner {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(19, 22, 32, 0.95) 100%);
        border: 1px solid rgba(0, 229, 255, 0.35);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.05);
    }}
    .rg-ai-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        color: {UI_THEME['accent_primary']};
        margin-bottom: 0.75rem;
    }}

    /* Monospace Code Box */
    .rg-code-box {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.825rem;
        background-color: #06070A;
        border: 1px solid #1E2330;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        color: #E2E8F0;
        overflow-x: auto;
        white-space: pre-wrap;
    }}

    /* Linear-style Finding Item */
    .rg-finding-item {{
        background-color: {UI_THEME['bg_surface']};
        border: 1px solid {UI_THEME['border_subtle']};
        border-radius: 6px;
        padding: 0.875rem 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: background-color 0.15s ease, border-color 0.15s ease;
    }}
    .rg-finding-item:hover {{
        background-color: {UI_THEME['bg_surface_elevated']};
        border-color: {UI_THEME['border_strong']};
    }}

    /* Buttons */
    .stButton > button {{
        background-color: #1E2330 !important;
        color: #F1F5F9 !important;
        border: 1px solid {UI_THEME['border_strong']} !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background-color: #272F42 !important;
        border-color: {UI_THEME['accent_primary']} !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.15) !important;
    }}

    /* Primary Accent Button */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        border: 1px solid #38BDF8 !important;
        color: #FFFFFF !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }}

    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid {UI_THEME['border_subtle']};
        padding-bottom: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 6px 6px 0px 0px;
        color: {UI_THEME['text_secondary']};
        font-weight: 500;
        padding: 8px 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {UI_THEME['bg_surface']} !important;
        color: {UI_THEME['accent_primary']} !important;
        border-bottom: 2px solid {UI_THEME['accent_primary']} !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
