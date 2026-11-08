"""
ROBOGUARD AI — UI Styles & Design Tokens Module (Classic Tremor Light Theme)
Injects bespoke CSS into Streamlit to deliver an enterprise-grade,
clean aerospace & robotics SOC aesthetic inspired by Tremor Labs,
Linear ergonomics, and modern design systems.
"""

import streamlit as st

def inject_custom_styles():
    """Injects high-fidelity Classic Light & Tremor-inspired CSS into Streamlit."""
    css = """
    <style>
    /* Google Fonts: Plus Jakarta Sans (Headings & UI) & JetBrains Mono (Code) */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Reset & Classic Clean Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        overflow-x: clip !important;
    }

    /* Strict Modern Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0F172A !important;
        letter-spacing: -0.025em !important;
        font-weight: 800 !important;
    }
    p, span, label, div {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    code, pre, .stCode, [data-testid="stCode"] * {
        font-family: 'JetBrains Mono', monospace !important;
    }

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

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        max-width: 1440px !important;
    }

    /* Classic High-Craft Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 1px 0 3px 0 rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Transform Streamlit Radio into Crisp Modern Navigation Items */
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.62rem 0.95rem !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background-color: #F8FAFC !important;
        border-color: #CBD5E1 !important;
        transform: translateX(3px) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05) !important;
    }
    /* Hide the radio input circle completely across all browser engines */
    [data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] label > div:first-child,
    [data-testid="stSidebar"] div[data-testid="stRadio"] span[data-baseweb="radio-control"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
    }
    /* Active selected radio item (Linear / Tremor Cobalt Glow & Left Accent) */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked),
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[aria-checked="true"] {
        background: #EFF6FF !important;
        border-color: #2563EB !important;
        border-left: 4px solid #2563EB !important;
        box-shadow: 0 2px 6px 0 rgba(37, 99, 235, 0.12) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
        color: #1D4ED8 !important;
        font-weight: 700 !important;
    }

    /* Tremor-Style Card System */
    .rg-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
        transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
    }
    .rg-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    }

    .rg-card-elevated {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Tremor Observability Stat Strips */
    .rg-stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 0.85rem;
        margin-bottom: 1.25rem;
    }
    .rg-stat-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.15rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease;
    }
    .rg-stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.06);
    }
    .rg-stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #2563EB;
    }
    .rg-stat-card.crit::before { background: #DC2626; }
    .rg-stat-card.success::before { background: #059669; }
    .rg-stat-card.amber::before { background: #D97706; }

    .rg-stat-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .rg-stat-value {
        font-size: 1.55rem;
        font-weight: 800;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0F172A;
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }
    .rg-stat-badge {
        font-size: 0.72rem;
        padding: 0.18rem 0.5rem;
        border-radius: 9999px;
        font-weight: 700;
    }
    .badge-green {
        background-color: #ECFDF5;
        color: #059669;
        border: 1px solid #A7F3D0;
    }
    .badge-orange {
        background-color: #FFFBEB;
        color: #D97706;
        border: 1px solid #FDE68A;
    }
    .badge-red {
        background-color: #FEF2F2;
        color: #DC2626;
        border: 1px solid #FECACA;
    }
    .badge-cyan {
        background-color: #EFF6FF;
        color: #2563EB;
        border: 1px solid #BFDBFE;
    }

    /* Tremor Progress Bar System */
    .tremor-progress-track {
        width: 100%;
        height: 8px;
        background-color: #F1F5F9;
        border-radius: 9999px;
        overflow: hidden;
        margin-top: 6px;
        border: 1px solid #E2E8F0;
    }
    .tremor-progress-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Monospace Code & Traceback Box */
    .rg-code-box {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.85rem 1.15rem;
        color: #0F172A;
        overflow-x: auto;
        white-space: pre-wrap;
        line-height: 1.5;
    }

    /* Tremor Metric Finding Card */
    .rg-finding-item {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.95rem 1.15rem;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s ease;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.02);
    }
    .rg-finding-item:hover {
        background-color: #F8FAFC;
        border-color: #CBD5E1;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.05);
    }

    /* High-Contrast Classic Buttons */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button,
    button[data-testid^="baseButton-"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.15rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05) !important;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover,
    button[data-testid^="baseButton-"]:hover {
        background-color: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0284C7 !important;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.08) !important;
    }

    /* Tremor AI Banner & Callout Cards */
    .rg-ai-banner {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 1.15rem 1.35rem;
        margin-bottom: 1.25rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.08);
    }
    .rg-ai-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #2563EB;
    }
    .rg-ai-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        font-size: 0.92rem;
        color: #1D4ED8;
        margin-bottom: 0.45rem;
    }

    /* React Bits / Magic UI Shimmer & Pulsing Keyframes */
    @keyframes shimmerFlow {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes borderBeamSweep {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }
    @keyframes sentinelFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    @keyframes sentinelPulseRing {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.5); }
        70% { box-shadow: 0 0 0 16px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }

    /* Primary Cobalt Action Button (React-Bits / Magic UI Shimmer & Glow) */
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #1D4ED8 0%, #2563EB 35%, #3B82F6 50%, #2563EB 65%, #1D4ED8 100%) !important;
        background-size: 200% 100% !important;
        animation: shimmerFlow 5s infinite linear !important;
        border: 1px solid #1E40AF !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 6px 0 rgba(37, 99, 235, 0.28) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(90deg, #1E40AF 0%, #1D4ED8 50%, #1E40AF 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* Input Fields, Selectboxes, and Textareas */
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03) !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important;
        border-radius: 8px !important;
    }
    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #334155 !important;
    }
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
    }

    /* Expanders & Chat Containers */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 1px 2px 0 rgba(0,0,0,0.03) !important;
    }
    div[data-testid="stExpander"] summary {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #2563EB !important;
    }

    /* Tremor Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background-color: #F1F5F9 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 4px !important;
        margin-bottom: 1.25rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 6px 16px !important;
        background-color: transparent !important;
        border: 1px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #0F172A !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        font-weight: 700 !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.08) !important;
    }

    /* Unified Git Diff Box */
    .rg-diff-box {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.85rem 1rem;
        color: #334155;
        overflow-x: auto;
        line-height: 1.5;
    }
    .diff-line-add {
        color: #059669;
        background-color: #ECFDF5;
        display: block;
        padding: 0.1rem 0.35rem;
        border-radius: 3px;
        font-weight: 600;
    }
    .diff-line-del {
        color: #DC2626;
        background-color: #FEF2F2;
        display: block;
        padding: 0.1rem 0.35rem;
        border-radius: 3px;
        font-weight: 600;
    }

    /* ==========================================================================
       PERSISTENT FLOATING LIVE AI SENTINEL COPILOT (DOCK WIDGET)
       ========================================================================== */
    .rg-floating-sentinel-dock {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.75rem;
        pointer-events: none;
    }
    .rg-floating-sentinel-dock > * {
        pointer-events: auto;
    }

    /* Floating Attack Reactive Toast */
    .rg-floating-attack-toast {
        background: #FFFFFF;
        border: 1px solid #FECACA;
        border-left: 4px solid #DC2626;
        border-radius: 12px;
        padding: 0.95rem 1.15rem;
        box-shadow: 0 10px 25px -5px rgba(220, 38, 38, 0.18), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
        max-width: 360px;
        animation: slideUpToast 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes slideUpToast {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .toast-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.35rem;
    }
    .toast-title {
        font-size: 0.8rem;
        font-weight: 800;
        color: #DC2626;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    .toast-body {
        font-size: 0.76rem;
        color: #334155;
        line-height: 1.45;
        margin-bottom: 0.65rem;
    }

    /* Floating Popover Trigger Styling */
    div[data-testid="stPopover"] {
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 99999 !important;
    }
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #1D4ED8 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 9999px !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        padding: 0.75rem 1.35rem !important;
        box-shadow: 0 8px 24px rgba(29, 78, 216, 0.38) !important;
        animation: sentinelFloat 3.5s ease-in-out infinite, sentinelPulseRing 4s infinite !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }
    div[data-testid="stPopover"] > button:hover {
        transform: scale(1.06) translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(29, 78, 216, 0.5) !important;
    }
    div[data-testid="stPopoverBody"] {
        width: 380px !important;
        max-width: 90vw !important;
        border-radius: 14px !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.15) !important;
        padding: 1.15rem !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
