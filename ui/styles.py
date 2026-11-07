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

    /* Top Header Bar & Streamlit Chrome Purge */
    #MainMenu { visibility: hidden !important; display: none !important; }
    header[data-testid="stHeader"] { 
        background-color: transparent !important;
        height: 0px !important;
        min-height: 0px !important;
        padding: 0px !important;
        visibility: hidden !important;
    }
    div[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    .stDeployButton { display: none !important; visibility: hidden !important; }
    footer { visibility: hidden !important; display: none !important; }

    /* Main Container Padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1350px !important;
    }

    /* Transform Streamlit Radio into Linear-Style Navigation Items */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background-color: #11141E !important;
        border: 1px solid #1E2330 !important;
        border-radius: 6px !important;
        padding: 0.6rem 0.85rem !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background-color: #1A1F2D !important;
        border-color: #38BDF8 !important;
    }
    /* Hide the ugly circular radio input dot completely */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        margin: 0 !important;
    }
    /* Active selected radio item */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.25) 0%, rgba(0, 229, 255, 0.15) 100%) !important;
        border-color: #00E5FF !important;
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.2) !important;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

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

    /* High-Contrast Interactive Buttons (All variants & download buttons) */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    button[data-testid^="baseButton-"] {
        background-color: #161A26 !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.55rem 1.15rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.4) !important;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover,
    button[data-testid^="baseButton-"]:hover {
        background-color: #22293B !important;
        border-color: #38BDF8 !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }

    /* Primary Accent Button with Cyan Pulse */
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #00E5FF 100%) !important;
        border: 1px solid #38BDF8 !important;
        color: #0B0D13 !important;
        font-weight: 700 !important;
        box-shadow: 0 0 14px rgba(0, 229, 255, 0.4) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #0369A1 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.6) !important;
    }

    /* Input and Selectbox Customization */
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #0F121C !important;
        color: #F8FAFC !important;
        border: 1px solid #1E2330 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.2) !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #0F121C !important;
        border: 1px solid #1E2330 !important;
    }
    li[role="option"] {
        background-color: #0F121C !important;
        color: #CBD5E1 !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1E2433 !important;
        color: #00E5FF !important;
    }

    /* Expanders & Chat Components */
    div[data-testid="stExpander"] {
        background-color: #0E111A !important;
        border: 1px solid #1E2330 !important;
        border-radius: 8px !important;
        margin-bottom: 0.75rem !important;
    }
    div[data-testid="stExpander"] summary {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #00E5FF !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #0E111A !important;
        border: 1px solid #1E2330 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #F8FAFC !important;
    }
    div[data-testid="stChatMessage"] {
        background-color: #11141E !important;
        border: 1px solid #1E2330 !important;
        border-radius: 8px !important;
        margin-bottom: 0.5rem !important;
    }

    /* Streamlit Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #0F121C !important;
        border: 1px solid #1E2330 !important;
        border-radius: 8px !important;
        padding: 4px 6px !important;
        margin-bottom: 1rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 8px 16px !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
        background-color: #161A26 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E2433 !important;
        color: #00E5FF !important;
        border: 1px solid rgba(0, 229, 255, 0.4) !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.15) !important;
    }

    /* Unified Code Diff Box */
    .rg-diff-box {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        background-color: #06070A;
        border: 1px solid #1E2330;
        border-radius: 6px;
        padding: 0.85rem 1rem;
        color: #CBD5E1;
        overflow-x: auto;
        line-height: 1.5;
    }
    .diff-line-add {
        color: #10B981;
        background-color: rgba(16, 185, 129, 0.12);
        display: block;
        padding: 0.1rem 0.3rem;
        border-radius: 2px;
    }
    .diff-line-del {
        color: #EF4444;
        background-color: rgba(239, 68, 68, 0.12);
        display: block;
        padding: 0.1rem 0.3rem;
        border-radius: 2px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
