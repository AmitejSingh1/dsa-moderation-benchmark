"""
src/dashboard_utils.py
EU DSA Moderation Benchmark — Dashboard Utility Module (Phase 8B Premium Redesign)

Provides data loading with @st.cache_data, CSS styling systems, typography,
custom component renderers, and polished Plotly chart generators.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# Paths & Directory Configuration
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# -----------------------------------------------------------------------------
# Color Palette & Theme Constants
# -----------------------------------------------------------------------------
PLATFORM_COLORS = {
    "TikTok": "#00A896",      # Refined modern teal
    "YouTube": "#E63946",     # Warm crimson
    "Instagram": "#8338EC",   # Vibrant purple
}

STAGE_COLORS = {
    "Automated Detection Rate": "#38BDF8",      # Sky blue
    "Decision with Any Automation Rate": "#8338EC", # Purple
    "Fully Automated Decision Rate": "#FB5607",  # Vivid orange
}

THEME = {
    "bg_dark": "#070B14",
    "bg_secondary": "#0B1020",
    "card_bg": "#101725",
    "card_elevated": "#141D30",
    "card_border": "rgba(255, 255, 255, 0.08)",
    "card_border_light": "rgba(148, 163, 184, 0.15)",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "text_muted": "#64748B",
    "accent_blue": "#38BDF8",
    "accent_green": "#10B981",
    "accent_amber": "#F59E0B",
    "grid_color": "rgba(255, 255, 255, 0.04)",
}

# -----------------------------------------------------------------------------
# Humanized Label Mappings
# -----------------------------------------------------------------------------
CATEGORY_LABELS = {
    "STATEMENT_CATEGORY_SCAMS_AND_FRAUD": "Scams & Fraud",
    "STATEMENT_CATEGORY_OTHER_VIOLATION_TC": "Other Terms of Service Violations",
    "STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH": "Illegal or Harmful Speech",
    "STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT": "Pornography or Sexualized Content",
    "STATEMENT_CATEGORY_VIOLENCE": "Violence",
    "STATEMENT_CATEGORY_PROTECTION_OF_MINORS": "Protection of Minors",
    "STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS": "Data Protection & Privacy",
    "STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS": "Civic Discourse & Elections",
    "STATEMENT_CATEGORY_UNSAFE_AND_PROHIBITED_PRODUCTS": "Unsafe & Prohibited Products",
    "STATEMENT_CATEGORY_CONSUMER_INFORMATION": "Consumer Information",
    "STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS": "Intellectual Property Infringements",
    "STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY": "Risk for Public Security",
    "STATEMENT_CATEGORY_ANIMAL_WELFARE": "Animal Welfare",
    "STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE": "Scope of Platform Service",
    "STATEMENT_CATEGORY_SELF_HARM": "Self-Harm",
    "STATEMENT_CATEGORY_CYBER_VIOLENCE": "Cyber Violence",
}

ACTION_LABELS = {
    "CONTENT_REMOVED": "Content Removed",
    "VISIBILITY_OTHER": "Visibility Restrictions (Other)",
    "ACCOUNT_TERMINATED": "Account Terminated",
    "CONTENT_DISABLED": "Content Feature Disabled",
    "CONTENT_DEMOTED": "Content Demoted / Downranked",
    "CONTENT_AGE_RESTRICTED": "Age Restricted",
    "CONTENT_INTERACTION_RESTRICTED": "Interaction Restricted",
    "CONTENT_LABELLED": "Content Labelled",
    "ACCOUNT_SUSPENDED": "Account Suspended",
    "MONETARY_SUSPENSION": "Monetary Suspension",
    "MONETARY_TERMINATION": "Monetary Termination",
    "PROVISION_PARTIAL_SUSPENSION": "Partial Provision Suspension",
    "PROVISION_PARTIAL_TERMINATION": "Partial Provision Termination",
    "PROVISION_TOTAL_SUSPENSION": "Total Provision Suspension",
    "PROVISION_TOTAL_TERMINATION": "Total Provision Termination",
}

METRIC_LABELS = {
    "decision_with_any_automation_rate": "Decision with Any Automation Rate",
    "automated_detection_rate": "Automated Detection Rate",
    "fully_automated_decision_rate": "Fully Automated Decision Rate",
}

# -----------------------------------------------------------------------------
# Data Loading & Caching
# -----------------------------------------------------------------------------
@st.cache_data
def load_benchmark_data():
    """Loads all 8 processed analytical CSV files from data/processed/."""
    files = {
        "overall": "automation_overall.csv",
        "by_category": "automation_by_category.csv",
        "monthly": "automation_monthly.csv",
        "category_monthly": "automation_category_monthly.csv",
        "category_volume": "category_volume.csv",
        "enforcement_overall": "enforcement_action_overall.csv",
        "enforcement_prevalence": "enforcement_action_prevalence.csv",
        "effect_sizes": "platform_effect_sizes.csv",
    }
    data = {}
    for key, fname in files.items():
        path = PROCESSED_DIR / fname
        if not path.exists():
            raise FileNotFoundError(f"Missing processed file: {path}")
        data[key] = pd.read_csv(path)
    return data


# -----------------------------------------------------------------------------
# Formatting Helpers
# -----------------------------------------------------------------------------
def format_pct(val, decimals=2):
    """Formats a 0-1 float or NaN to a percentage string."""
    if pd.isna(val) or val is None:
        return "N/A"
    return f"{val * 100:.{decimals}f}%"


def format_sors(val):
    """Formats an SoR count to a concise string with units (M, K)."""
    if pd.isna(val) or val is None:
        return "N/A"
    if val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    if val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{int(val):,}"


def humanize_category(cat):
    """Converts a raw DSA category enum to a clean human-readable name."""
    return CATEGORY_LABELS.get(cat, cat.replace("STATEMENT_CATEGORY_", "").replace("_", " ").title())


def humanize_action(action):
    """Converts a raw DSA action enum to a clean human-readable name."""
    return ACTION_LABELS.get(action, action.replace("_", " ").title())


def render_html(html_str: str):
    """Safely render HTML without markdown converting indented lines into code blocks."""
    clean_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Premium CSS Styling System
# -----------------------------------------------------------------------------
def get_custom_css():
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Root & Background */
        .stApp {{
            background-color: {THEME["bg_dark"]};
            background-image: 
                radial-gradient(ellipse 60% 40% at 85% 5%, rgba(0, 168, 150, 0.05), transparent 60%),
                radial-gradient(ellipse 50% 35% at 15% 15%, rgba(230, 57, 70, 0.05), transparent 60%),
                radial-gradient(ellipse 55% 40% at 50% 85%, rgba(131, 56, 236, 0.04), transparent 65%);
            color: {THEME["text_primary"]};
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            letter-spacing: -0.01em;
        }}

        /* Clean Streamlit Layout & Chrome */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 5rem;
            max-width: 1200px;
        }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        #MainMenu {{ visibility: hidden; }}
        div[data-testid="stToolbar"] {{ visibility: hidden; height: 0%; }}
        div[data-testid="stDecoration"] {{ visibility: hidden; height: 0%; }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {THEME["bg_secondary"]};
            border-right: 1px solid {THEME["card_border"]};
        }}
        section[data-testid="stSidebar"] div.block-container {{
            padding-top: 2rem;
        }}

        /* Number Typography & Tabular Alignment */
        .tabular-nums {{
            font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
            font-feature-settings: 'tnum';
            font-variant-numeric: tabular-nums;
        }}

        /* Section Numbers (Editorial Style) */
        .section-anchor {{
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            margin-top: 3.5rem;
            margin-bottom: 0.25rem;
        }}
        .section-num {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            font-weight: 700;
            color: {THEME["accent_blue"]};
            letter-spacing: 0.1em;
        }}
        .section-title {{
            font-size: 1.5rem;
            font-weight: 800;
            color: {THEME["text_primary"]};
            letter-spacing: -0.025em;
            margin: 0;
        }}
        .section-subtitle {{
            font-size: 0.92rem;
            color: {THEME["text_secondary"]};
            margin-top: 0.35rem;
            margin-bottom: 1.25rem;
            line-height: 1.5;
            max-width: 850px;
        }}

        /* Elevated Card System */
        .premium-card {{
            background-color: {THEME["card_bg"]};
            border: 1px solid {THEME["card_border"]};
            border-radius: 16px;
            padding: 1.5rem 1.75rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .premium-card:hover {{
            border-color: {THEME["card_border_light"]};
            box-shadow: 0 14px 40px -10px rgba(0, 0, 0, 0.5);
        }}

        /* KPI Masthead Strip */
        .masthead-strip {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: {THEME["card_bg"]};
            border: 1px solid {THEME["card_border"]};
            border-radius: 14px;
            padding: 1.25rem 2rem;
            margin: 2rem 0;
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.3);
        }}
        .masthead-item {{
            text-align: center;
            flex: 1;
        }}
        .masthead-val {{
            font-size: 2rem;
            font-weight: 800;
            color: {THEME["text_primary"]};
            line-height: 1.1;
            font-family: 'JetBrains Mono', sans-serif;
        }}
        .masthead-lbl {{
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {THEME["text_muted"]};
            margin-top: 0.25rem;
        }}
        .masthead-sep {{
            width: 1px;
            height: 38px;
            background-color: {THEME["card_border"]};
        }}

        /* Hero Progress Track Elements */
        .track-container {{
            background-color: {THEME["card_bg"]};
            border: 1px solid {THEME["card_border"]};
            border-radius: 18px;
            padding: 1.75rem;
            box-shadow: 0 12px 36px -10px rgba(0, 0, 0, 0.45);
        }}
        .track-row {{
            margin-bottom: 1.35rem;
        }}
        .track-row:last-child {{
            margin-bottom: 0;
        }}
        .track-meta {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.45rem;
        }}
        .track-platform {{
            font-size: 1.05rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .track-rate {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.6rem;
            font-weight: 800;
            line-height: 1;
        }}
        .track-sub {{
            font-size: 0.8rem;
            color: {THEME["text_muted"]};
        }}
        .track-bar-bg {{
            width: 100%;
            height: 10px;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 999px;
            overflow: hidden;
            position: relative;
        }}
        .track-bar-fill {{
            height: 100%;
            border-radius: 999px;
            transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        /* The Dramatic GAP Card */
        .gap-container {{
            background: linear-gradient(135deg, rgba(20, 27, 44, 0.9) 0%, rgba(16, 23, 37, 0.95) 100%);
            border: 1px solid {THEME["card_border_light"]};
            border-radius: 18px;
            padding: 2rem 2.25rem;
            margin: 2.25rem 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            box-shadow: 0 16px 40px -12px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }}
        .gap-container::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 1px;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.4), transparent);
        }}
        .gap-num {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 3.8rem;
            font-weight: 800;
            line-height: 0.95;
            color: {THEME["accent_blue"]};
            letter-spacing: -0.03em;
        }}
        .gap-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {THEME["text_primary"]};
            margin-bottom: 0.25rem;
        }}
        .gap-desc {{
            font-size: 0.88rem;
            color: {THEME["text_secondary"]};
            line-height: 1.45;
            max-width: 580px;
        }}

        /* Deep Dive Cards */
        .deep-card {{
            background-color: {THEME["card_bg"]};
            border: 1px solid {THEME["card_border"]};
            border-radius: 16px;
            padding: 1.5rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.3);
            position: relative;
        }}
        .deep-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            border-bottom: 1px solid {THEME["card_border"]};
            padding-bottom: 0.75rem;
        }}
        .deep-name {{
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: 0.02em;
        }}
        .deep-sors {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: {THEME["text_muted"]};
        }}
        .deep-stat-row {{
            margin-bottom: 0.75rem;
        }}
        .deep-stat-label {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {THEME["text_muted"]};
        }}
        .deep-stat-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.25rem;
            font-weight: 700;
            color: {THEME["text_primary"]};
        }}
        .deep-primary-value {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
            margin: 0.2rem 0;
        }}
        .deep-badge-note {{
            font-size: 0.8rem;
            line-height: 1.45;
            padding: 0.65rem 0.85rem;
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid {THEME["card_border"]};
            margin-top: 1rem;
        }}

        /* Subtle Pill Badges */
        .pill-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background-color: rgba(255, 255, 255, 0.04);
            color: {THEME["text_secondary"]};
        }}

        /* Full Width Recommendation Banner */
        .rec-banner {{
            background: linear-gradient(135deg, rgba(16, 24, 39, 0.95) 0%, rgba(13, 33, 30, 0.9) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 18px;
            padding: 2rem 2.25rem;
            margin: 2.5rem 0;
            box-shadow: 0 16px 40px -12px rgba(0, 0, 0, 0.5);
            position: relative;
        }}
        .rec-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 0.75rem;
            margin: 1.5rem 0;
        }}
        .rec-pill {{
            background-color: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            text-align: center;
            font-size: 0.84rem;
            font-weight: 700;
            color: {THEME["text_primary"]};
            letter-spacing: 0.03em;
        }}

        /* Expander Component Styling */
        div[data-testid="stExpander"] {{
            background-color: {THEME["card_bg"]};
            border: 1px solid {THEME["card_border"]};
            border-radius: 12px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        div[data-testid="stExpander"] details {{
            background-color: transparent !important;
        }}
        div[data-testid="stExpander"] summary {{
            background-color: transparent !important;
            color: {THEME["text_primary"]} !important;
            font-weight: 600 !important;
            padding: 0.85rem 1.25rem !important;
        }}
        div[data-testid="stExpander"] summary:hover {{
            color: {THEME["accent_blue"]} !important;
        }}
        div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
            padding: 1rem 1.25rem !important;
            border-top: 1px solid {THEME["card_border"]};
        }}
    </style>
    """


# -----------------------------------------------------------------------------
# Plotly Layout Helper (Dark Analytical Minimal)
# -----------------------------------------------------------------------------
def get_premium_plotly_layout(
    title="",
    subtitle="",
    xaxis_title=None,
    yaxis_title=None,
    height=400,
    showlegend=True,
    barmode="group",
):
    """Returns a unified, high-contrast dark layout for Plotly charts."""
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=45, r=35, t=55 if title else 25, b=45),
        font=dict(color=THEME["text_primary"], family="'Plus Jakarta Sans', sans-serif", size=11),
        xaxis=dict(
            gridcolor=THEME["grid_color"],
            gridwidth=1,
            zeroline=False,
            tickfont=dict(color=THEME["text_secondary"], size=10),
        ),
        yaxis=dict(
            gridcolor=THEME["grid_color"],
            gridwidth=1,
            zeroline=False,
            tickfont=dict(color=THEME["text_secondary"], size=10),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=10.5, color=THEME["text_secondary"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        barmode=barmode,
        showlegend=showlegend,
        hoverlabel=dict(
            bgcolor=THEME["card_bg"],
            bordercolor=THEME["card_border_light"],
            font=dict(color=THEME["text_primary"], family="'Plus Jakarta Sans', sans-serif", size=11),
        ),
    )
    if title:
        title_text = f"<b>{title}</b>"
        if subtitle:
            title_text += f"<br><span style='font-size:12px; color:{THEME['text_secondary']}; font-weight:normal'>{subtitle}</span>"
        layout["title"] = dict(
            text=title_text,
            font=dict(size=14, color=THEME["text_primary"], family="'Plus Jakarta Sans', sans-serif"),
            x=0.01,
            y=0.96,
            xanchor="left",
            yanchor="top",
        )
    if xaxis_title:
        layout["xaxis"]["title"] = dict(text=xaxis_title, font=dict(color=THEME["text_secondary"], size=11))
    if yaxis_title:
        layout["yaxis"]["title"] = dict(text=yaxis_title, font=dict(color=THEME["text_secondary"], size=11))
    return layout
