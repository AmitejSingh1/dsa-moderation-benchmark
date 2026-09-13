"""
app.py
EU DSA Content Moderation Benchmark — Interactive Portfolio Dashboard (Phase 8B Premium Redesign)

A cinematic, publication-grade Trust & Safety analytics product communicating
cross-platform moderation findings across 661.7M EU DSA Statements of Reasons.

Reads strictly from data/processed/*.csv without requiring raw Parquet downloads.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

from src.dashboard_utils import (
    load_benchmark_data,
    PLATFORM_COLORS,
    STAGE_COLORS,
    THEME,
    CATEGORY_LABELS,
    ACTION_LABELS,
    METRIC_LABELS,
    format_pct,
    format_sors,
    humanize_category,
    humanize_action,
    get_custom_css,
    get_premium_plotly_layout,
    render_html,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EU DSA · Moderation Benchmark",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_html(get_custom_css())

# -----------------------------------------------------------------------------
# 2. Data Loading (Cached)
# -----------------------------------------------------------------------------
data = load_benchmark_data()
df_overall = data["overall"].set_index("platform")
df_cat = data["by_category"]
df_cat_m = data["category_monthly"]
df_enf_ov = data["enforcement_overall"]
df_enf_prev = data["enforcement_prevalence"]
df_effect = data["effect_sizes"]

# Precompute benchmark constants
TOTAL_SORS = int(df_overall["represented_sors"].sum())
NUM_PLATFORMS = len(df_overall)
NUM_MONTHS = 11

scams_data = df_cat[df_cat["category"] == "STATEMENT_CATEGORY_SCAMS_AND_FRAUD"].set_index("platform")
SCAMS_TOTAL_SORS = int(scams_data["represented_sors"].sum())

yt_scams_sors = int(scams_data.loc["YouTube", "represented_sors"])
tt_scams_sors = int(scams_data.loc["TikTok", "represented_sors"])
ig_scams_sors = int(scams_data.loc["Instagram", "represented_sors"])

yt_scams_any_rate = scams_data.loc["YouTube", "decision_with_any_automation_rate"]
tt_scams_any_rate = scams_data.loc["TikTok", "decision_with_any_automation_rate"]
ig_scams_any_rate = scams_data.loc["Instagram", "decision_with_any_automation_rate"]

yt_scams_det_rate = scams_data.loc["YouTube", "automated_detection_rate"]
tt_scams_det_rate = scams_data.loc["TikTok", "automated_detection_rate"]
ig_scams_det_rate = scams_data.loc["Instagram", "automated_detection_rate"]

yt_scams_full_rate = scams_data.loc["YouTube", "fully_automated_decision_rate"]
tt_scams_full_rate = scams_data.loc["TikTok", "fully_automated_decision_rate"]
ig_scams_full_rate = scams_data.loc["Instagram", "fully_automated_decision_rate"]

# Calculate exact Gap values
scams_gap_pp = (ig_scams_any_rate - yt_scams_any_rate) * 100  # 99.20 pp
max_scams_det_diff = (max(yt_scams_det_rate, tt_scams_det_rate, ig_scams_det_rate) -
                      min(yt_scams_det_rate, tt_scams_det_rate, ig_scams_det_rate)) * 100  # 8.49 pp
yt_ig_det_diff = abs(yt_scams_det_rate - ig_scams_det_rate) * 100  # 0.48 pp


# -----------------------------------------------------------------------------
# 3. Sidebar Control Rail
# -----------------------------------------------------------------------------
with st.sidebar:
    render_html(f"""
        <div style='padding-bottom: 0.75rem; border-bottom: 1px solid {THEME["card_border"]}; margin-bottom: 1.25rem;'>
            <div style='font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: {THEME["accent_blue"]};'>
                EU DSA Article 17
            </div>
            <div style='font-size: 1.15rem; font-weight: 800; color: {THEME["text_primary"]}; margin-top: 0.15rem;'>
                MODERATION BENCHMARK
            </div>
        </div>
        """)

    render_html(f"<div style='font-size: 0.74rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {THEME['text_muted']}; margin-bottom: 0.5rem;'>EXPLORE CONTROLS</div>")

    metric_choice = st.selectbox(
        "Metric",
        options=[
            "decision_with_any_automation_rate",
            "automated_detection_rate",
            "fully_automated_decision_rate",
        ],
        format_func=lambda x: METRIC_LABELS.get(x, x),
        index=0,
        label_visibility="collapsed",
    )

    selected_platforms = st.multiselect(
        "Platforms",
        options=["TikTok", "YouTube", "Instagram"],
        default=["TikTok", "YouTube", "Instagram"],
    )

    hide_sparse = st.toggle(
        "Hide low-volume (<0.10%)",
        value=True,
        help="Hides categories representing <0.10% of a platform's total SoRs (MAPPING.md Rule 6). Display filter only.",
    )

    render_html(f"""
        <div style='margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid {THEME["card_border"]};'>
            <div style='font-size: 0.74rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {THEME["text_muted"]}; margin-bottom: 0.6rem;'>BENCHMARK SCOPE</div>
            <div style='font-size: 0.82rem; color: {THEME["text_secondary"]}; line-height: 1.6;'>
                • <b>Window:</b> Jul 2025 – May 2026<br>
                • <b>Volume:</b> 661.7M Represented SoRs<br>
                • <b>Corpus:</b> Complete DSA Aggregates<br>
                • <b>Scope:</b> Fixed 11-Month Harmonized Era
            </div>
        </div>
        """)

    render_html(f"""
        <div style='margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid {THEME["card_border"]};'>
            <div style='font-size: 0.74rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {THEME["text_muted"]}; margin-bottom: 0.5rem;'>SECTION JUMP</div>
            <div style='font-size: 0.8rem; line-height: 1.8;'>
                <a href='#01-detection-vs-decision' style='color:{THEME["text_secondary"]}; text-decoration:none;'>01 Detection vs Decision</a><br>
                <a href='#02-the-scams-fraud-divide' style='color:{THEME["text_secondary"]}; text-decoration:none;'>02 Scams & Fraud Divide</a><br>
                <a href='#03-does-it-persist' style='color:{THEME["text_secondary"]}; text-decoration:none;'>03 11-Month Persistence</a><br>
                <a href='#04-why-overall-averages-mislead' style='color:{THEME["text_secondary"]}; text-decoration:none;'>04 Composition Effect</a><br>
                <a href='#05-how-enforcement-differs' style='color:{THEME["text_secondary"]}; text-decoration:none;'>05 Enforcement Actions</a><br>
                <a href='#06-explore-the-data' style='color:{THEME["text_secondary"]}; text-decoration:none;'>06 Category Explorer</a><br>
                <a href='#07-what-should-a-safety-team-do' style='color:{THEME["text_secondary"]}; text-decoration:none;'>07 Safety Action</a><br>
                <a href='#08-limitations-methodology' style='color:{THEME["text_secondary"]}; text-decoration:none;'>08 Methodology & Limitations</a>
            </div>
        </div>
        """)

    render_html(f"""
        <div style='margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid {THEME["card_border"]}; font-size: 0.76rem; color: {THEME["text_muted"]};'>
            Source: EU DSA Transparency Database<br>
            Analysis adheres to MAPPING.md rules.
        </div>
        """)


# -----------------------------------------------------------------------------
# 4. EDITORIAL HERO
# -----------------------------------------------------------------------------
col_hero_left, col_hero_right = st.columns([1.1, 1.25], gap="large")

with col_hero_left:
    render_html(f"""
        <div style='padding-top: 0.5rem;'>
            <div style='display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;'>
                <span class='pill-badge' style='border-color: rgba(56, 189, 248, 0.3); color: {THEME["accent_blue"]};'>
                    EU DSA · TRUST & SAFETY INTELLIGENCE
                </span>
                <span class='pill-badge'>JUL 2025 — MAY 2026</span>
            </div>
            <h1 style='font-size: 2.85rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; color: {THEME["text_primary"]}; margin: 0 0 1rem 0;'>
                Detection converges.<br>
                <span style='color: {THEME["text_muted"]};'>Decision automation doesn't.</span>
            </h1>
            <p style='font-size: 1.05rem; line-height: 1.55; color: {THEME["text_secondary"]}; margin-bottom: 1.5rem; max-width: 520px;'>
                <b>661.7M standardized moderation records</b> across TikTok, YouTube, and Instagram reveal similar automated detection — but sharply different decision-stage automation in Scams & Fraud.
            </p>
        </div>
        """)

with col_hero_right:
    render_html(f"""
        <div class='track-container'>
            <div style='display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.25rem;'>
                <div>
                    <div style='font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {THEME["text_muted"]};'>
                        PRIMARY FINDING · SCAMS & FRAUD
                    </div>
                    <div style='font-size: 1.05rem; font-weight: 700; color: {THEME["text_primary"]};'>
                        Decision with Any Automation Rate
                    </div>
                </div>
                <div style='font-size: 0.8rem; color: {THEME["text_muted"]};'>
                    90.8M Represented SoRs
                </div>
            </div>

            <!-- YouTube Track -->
            <div class='track-row'>
                <div class='track-meta'>
                    <span class='track-platform' style='color: {PLATFORM_COLORS["YouTube"]};'>
                        <span style='width:8px; height:8px; border-radius:50%; background-color:{PLATFORM_COLORS["YouTube"]}; display:inline-block;'></span>
                        YouTube
                    </span>
                    <span class='track-rate' style='color: {PLATFORM_COLORS["YouTube"]};'>{format_pct(yt_scams_any_rate)}</span>
                </div>
                <div class='track-bar-bg'>
                    <div class='track-bar-fill' style='width: {max(yt_scams_any_rate * 100, 2):.1f}%; background-color: {PLATFORM_COLORS["YouTube"]};'></div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 0.3rem;'>
                    <span class='track-sub'>{format_sors(yt_scams_sors)} SoRs</span>
                    <span class='track-sub'>Detection: {format_pct(yt_scams_det_rate, 1)}</span>
                </div>
            </div>

            <!-- TikTok Track -->
            <div class='track-row'>
                <div class='track-meta'>
                    <span class='track-platform' style='color: {PLATFORM_COLORS["TikTok"]};'>
                        <span style='width:8px; height:8px; border-radius:50%; background-color:{PLATFORM_COLORS["TikTok"]}; display:inline-block;'></span>
                        TikTok
                    </span>
                    <span class='track-rate' style='color: {PLATFORM_COLORS["TikTok"]};'>{format_pct(tt_scams_any_rate)}</span>
                </div>
                <div class='track-bar-bg'>
                    <div class='track-bar-fill' style='width: {tt_scams_any_rate * 100:.1f}%; background-color: {PLATFORM_COLORS["TikTok"]};'></div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 0.3rem;'>
                    <span class='track-sub'>{format_sors(tt_scams_sors)} SoRs</span>
                    <span class='track-sub'>Detection: {format_pct(tt_scams_det_rate, 1)}</span>
                </div>
            </div>

            <!-- Instagram Track -->
            <div class='track-row'>
                <div class='track-meta'>
                    <span class='track-platform' style='color: {PLATFORM_COLORS["Instagram"]};'>
                        <span style='width:8px; height:8px; border-radius:50%; background-color:{PLATFORM_COLORS["Instagram"]}; display:inline-block;'></span>
                        Instagram
                    </span>
                    <span class='track-rate' style='color: {PLATFORM_COLORS["Instagram"]};'>{format_pct(ig_scams_any_rate)}</span>
                </div>
                <div class='track-bar-bg'>
                    <div class='track-bar-fill' style='width: {ig_scams_any_rate * 100:.1f}%; background-color: {PLATFORM_COLORS["Instagram"]};'></div>
                </div>
                <div style='display: flex; justify-content: space-between; margin-top: 0.3rem;'>
                    <span class='track-sub'>{format_sors(ig_scams_sors)} SoRs</span>
                    <span class='track-sub'>Detection: {format_pct(ig_scams_det_rate, 1)}</span>
                </div>
            </div>
        </div>
        """)


# -----------------------------------------------------------------------------
# 5. KPI MASTHEAD STRIP
# -----------------------------------------------------------------------------
render_html(f"""
    <div class='masthead-strip'>
        <div class='masthead-item'>
            <div class='masthead-val'>{format_sors(TOTAL_SORS)}</div>
            <div class='masthead-lbl'>Represented SoRs</div>
        </div>
        <div class='masthead-sep'></div>
        <div class='masthead-item'>
            <div class='masthead-val'>{format_sors(SCAMS_TOTAL_SORS)}</div>
            <div class='masthead-lbl'>Scams & Fraud SoRs</div>
        </div>
        <div class='masthead-sep'></div>
        <div class='masthead-item'>
            <div class='masthead-val'>{NUM_PLATFORMS}</div>
            <div class='masthead-lbl'>Benchmark Platforms</div>
        </div>
        <div class='masthead-sep'></div>
        <div class='masthead-item'>
            <div class='masthead-val'>{NUM_MONTHS}</div>
            <div class='masthead-lbl'>Observation Months</div>
        </div>
    </div>
    """)


# -----------------------------------------------------------------------------
# 6. "THE GAP" DRAMATIC CALLOUT
# -----------------------------------------------------------------------------
render_html(f"""
    <div class='gap-container'>
        <div>
            <div class='gap-title'>THE SCAMS & FRAUD DIVIDE</div>
            <div class='gap-desc'>
                YouTube → Instagram gap in Scams & Fraud decision-stage automation.
                While decision execution diverges by nearly the entire metric range, detection differs by less than 8.5 pp across all three platforms (and by just 0.48 pp between YouTube and Instagram).
            </div>
        </div>
        <div style='text-align: right;'>
            <div class='gap-num'>{scams_gap_pp:.1f} pp</div>
            <div style='font-size: 0.76rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {THEME["text_muted"]}; margin-top: 0.2rem;'>
                DECISION AUTOMATION GAP
            </div>
        </div>
    </div>
    """)


# -----------------------------------------------------------------------------
# SECTION 01: DETECTION VS DECISION (Dumbbell / Connected Dot Chart)
# -----------------------------------------------------------------------------
render_html("""
    <div id='01-detection-vs-decision' class='section-anchor'>
        <span class='section-num'>01</span>
        <h2 class='section-title'>DETECTION VS DECISION</h2>
    </div>
    <div class='section-subtitle'>
        Finding content is automated everywhere. Deciding what happens next is not.
        Tracking movement between automated detection and decision execution reveals where operational models diverge.
    </div>
    """)

platforms_all = ["YouTube", "TikTok", "Instagram"]
det_rates_all = [df_overall.loc[p, "automated_detection_rate"] * 100 for p in platforms_all]
any_rates_all = [df_overall.loc[p, "decision_with_any_automation_rate"] * 100 for p in platforms_all]
drops = [d - a for d, a in zip(det_rates_all, any_rates_all)]

fig_dumbbell = go.Figure()

# Add connector lines between detection and decision
for i, p in enumerate(platforms_all):
    fig_dumbbell.add_trace(
        go.Scatter(
            x=[any_rates_all[i], det_rates_all[i]],
            y=[p, p],
            mode="lines",
            line=dict(color=THEME["card_border_light"], width=4),
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Add Decision Stage dots
fig_dumbbell.add_trace(
    go.Scatter(
        x=any_rates_all,
        y=platforms_all,
        mode="markers+text",
        name="Decision with Any Automation",
        marker=dict(
            color=[PLATFORM_COLORS[p] for p in platforms_all],
            size=16,
            line=dict(color="white", width=2),
        ),
        text=[f"<b>{r:.1f}%</b>" if p != "Instagram" else "" for p, r in zip(platforms_all, any_rates_all)],
        textposition=["bottom center" if p == "YouTube" else "top center" for p in platforms_all],
        textfont=dict(color=THEME["text_primary"], size=11, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>Decision Automation: %{x:.2f}%<extra></extra>",
    )
)

# Add Detection Stage dots
fig_dumbbell.add_trace(
    go.Scatter(
        x=det_rates_all,
        y=platforms_all,
        mode="markers+text",
        name="Automated Detection Rate",
        marker=dict(
            color=STAGE_COLORS["Automated Detection Rate"],
            size=14,
            symbol="diamond",
            line=dict(color="white", width=1.5),
        ),
        text=[f"<b>{r:.1f}%</b>" if p != "Instagram" else "<b>95.5% (both)</b>" for p, r in zip(platforms_all, det_rates_all)],
        textposition="top center",
        textfont=dict(color=STAGE_COLORS["Automated Detection Rate"], size=11, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>Detection Rate: %{x:.2f}%<extra></extra>",
    )
)

layout_dumbbell = get_premium_plotly_layout(
    xaxis_title="Rate (%)",
    yaxis_title="",
    height=280,
    showlegend=True,
)
layout_dumbbell["xaxis"]["range"] = [45, 105]
layout_dumbbell["xaxis"]["ticksuffix"] = "%"
fig_dumbbell.update_layout(layout_dumbbell)

st.plotly_chart(fig_dumbbell, use_container_width=True, config=dict(displayModeBar=False))

render_html(f"""
    <div style='background-color:{THEME["card_bg"]}; border:1px solid {THEME["card_border"]}; border-radius:12px; padding:1rem 1.25rem; margin-top:0.5rem;'>
        <div style='display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem; font-size:0.85rem;'>
            <div><b>YouTube:</b> 98.89% detection → 54.67% decision (<span style='color:{PLATFORM_COLORS["YouTube"]}; font-weight:700;'>-44.2 pp drop</span>)</div>
            <div><b>TikTok:</b> 97.25% detection → 92.44% decision (<span style='color:{PLATFORM_COLORS["TikTok"]}; font-weight:700;'>-4.8 pp drop</span>)</div>
            <div><b>Instagram:</b> 95.50% detection → 95.50% decision (<span style='color:{PLATFORM_COLORS["Instagram"]}; font-weight:700;'>0.0 pp drop</span>)</div>
        </div>
    </div>
    """)


# -----------------------------------------------------------------------------
# SECTION 02: THE SCAMS & FRAUD DIVIDE (Deep-Dive Cards)
# -----------------------------------------------------------------------------
render_html("""
    <div id='02-the-scams-fraud-divide' class='section-anchor'>
        <span class='section-num'>02</span>
        <h2 class='section-title'>THE SCAMS & FRAUD DIVIDE</h2>
    </div>
    <div class='section-subtitle'>
        Three platforms, three distinct decision-stage operating profiles across 90,782,865 regulatory disclosures.
    </div>
    """)

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    render_html(f"""
        <div class='deep-card' style='border-top: 3px solid {PLATFORM_COLORS["YouTube"]};'>
            <div>
                <div class='deep-header'>
                    <span class='deep-name' style='color: {PLATFORM_COLORS["YouTube"]};'>YOUTUBE</span>
                    <span class='deep-sors'>{yt_scams_sors:,} SoRs</span>
                </div>
                <div class='deep-stat-row'>
                    <div class='deep-stat-label'>DECISION WITH ANY AUTOMATION</div>
                    <div class='deep-primary-value' style='color: {PLATFORM_COLORS["YouTube"]};'>{format_pct(yt_scams_any_rate)}</div>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;'>
                    <div>
                        <div class='deep-stat-label'>DETECTION</div>
                        <div class='deep-stat-value'>{format_pct(yt_scams_det_rate, 1)}</div>
                    </div>
                    <div>
                        <div class='deep-stat-label'>FULLY AUTOMATED</div>
                        <div class='deep-stat-value'>{format_pct(yt_scams_full_rate, 2)}</div>
                    </div>
                </div>
            </div>
            <div class='deep-badge-note'>
                99.75% of represented Scams & Fraud SoRs were reported as decisions taken without automated means (32.6M of 32.7M SoRs).
            </div>
        </div>
        """)

with col_d2:
    render_html(f"""
        <div class='deep-card' style='border-top: 3px solid {PLATFORM_COLORS["TikTok"]};'>
            <div>
                <div class='deep-header'>
                    <span class='deep-name' style='color: {PLATFORM_COLORS["TikTok"]};'>TIKTOK</span>
                    <span class='deep-sors'>{tt_scams_sors:,} SoRs</span>
                </div>
                <div class='deep-stat-row'>
                    <div class='deep-stat-label'>DECISION WITH ANY AUTOMATION</div>
                    <div class='deep-primary-value' style='color: {PLATFORM_COLORS["TikTok"]};'>{format_pct(tt_scams_any_rate)}</div>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;'>
                    <div>
                        <div class='deep-stat-label'>DETECTION</div>
                        <div class='deep-stat-value'>{format_pct(tt_scams_det_rate, 1)}</div>
                    </div>
                    <div>
                        <div class='deep-stat-label'>FULLY AUTOMATED</div>
                        <div class='deep-stat-value'>{format_pct(tt_scams_full_rate, 2)}</div>
                    </div>
                </div>
            </div>
            <div class='deep-badge-note'>
                <b>84.94% reported as FULLY automated</b> (8.6M SoRs).
            </div>
        </div>
        """)

with col_d3:
    render_html(f"""
        <div class='deep-card' style='border-top: 3px solid {PLATFORM_COLORS["Instagram"]};'>
            <div>
                <div class='deep-header'>
                    <span class='deep-name' style='color: {PLATFORM_COLORS["Instagram"]};'>INSTAGRAM</span>
                    <span class='deep-sors'>{ig_scams_sors:,} SoRs</span>
                </div>
                <div class='deep-stat-row'>
                    <div class='deep-stat-label'>DECISION WITH ANY AUTOMATION</div>
                    <div class='deep-primary-value' style='color: {PLATFORM_COLORS["Instagram"]};'>{format_pct(ig_scams_any_rate)}</div>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;'>
                    <div>
                        <div class='deep-stat-label'>DETECTION</div>
                        <div class='deep-stat-value'>{format_pct(ig_scams_det_rate, 1)}</div>
                    </div>
                    <div>
                        <div class='deep-stat-label'>FULLY AUTOMATED</div>
                        <div class='deep-stat-value'>{format_pct(ig_scams_full_rate, 2)}</div>
                    </div>
                </div>
            </div>
            <div class='deep-badge-note'>
                <b>99.45% reported as PARTIALLY automated</b> (47.7M SoRs; 0.00% fully automated). 98.77% of scam decisions result in account termination.
            </div>
        </div>
        """)

render_html(f"""
    <div style='background-color:rgba(19, 27, 46, 0.7); border:1px solid {THEME["card_border"]}; border-radius:12px; padding:1rem 1.25rem; margin-top:1.25rem; font-size:0.83rem; color:{THEME["text_secondary"]}; line-height:1.5;'>
        <b>Crucial Interpretation Rule:</b> Instagram's 99.45% rate reflects <i>partially automated decisions</i>, whereas TikTok's 84.94% reflects <i>fully automated decisions</i>. The two figures describe different regulatory classifications and should not be conflated as representing the same type of reported decision automation.
    </div>
    """)


# -----------------------------------------------------------------------------
# SECTION 03: DOES IT PERSIST? (Monthly Trend)
# -----------------------------------------------------------------------------
render_html("""
    <div id='03-does-it-persist' class='section-anchor'>
        <span class='section-num'>03</span>
        <h2 class='section-title'>DOES IT PERSIST?</h2>
    </div>
    <div class='section-subtitle'>
        Monthly consistency across all 11 continuous partitions from July 2025 through May 2026.
    </div>
    """)

scams_m = df_cat_m[df_cat_m["category"] == "STATEMENT_CATEGORY_SCAMS_AND_FRAUD"].copy()

# Direct editorial statistics
render_html(f"""
    <div style='display:flex; gap:2rem; margin-bottom:1rem; flex-wrap:wrap;'>
        <div>
            <div style='font-family:JetBrains Mono, monospace; font-size:1.8rem; font-weight:800; color:{THEME["text_primary"]};'>11 MONTHS</div>
            <div style='font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:{THEME["text_muted"]};'>CONTINUOUS WINDOW</div>
        </div>
        <div>
            <div style='font-family:JetBrains Mono, monospace; font-size:1.8rem; font-weight:800; color:{THEME["accent_green"]};'>0</div>
            <div style='font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:{THEME["text_muted"]};'>RANK REVERSALS</div>
        </div>
        <div>
            <div style='font-family:JetBrains Mono, monospace; font-size:1.8rem; font-weight:800; color:{PLATFORM_COLORS["YouTube"]};'>&lt;0.6%</div>
            <div style='font-size:0.72rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:{THEME["text_muted"]};'>YOUTUBE CEILING</div>
        </div>
    </div>
    """)

fig_monthly = go.Figure()

for platform in ["Instagram", "TikTok", "YouTube"]:
    sub = scams_m[scams_m["platform"] == platform].sort_values("month")
    y_vals = sub["decision_with_any_automation_rate"] * 100

    fig_monthly.add_trace(
        go.Scatter(
            x=sub["month"],
            y=y_vals,
            mode="lines+markers",
            name=platform,
            line=dict(color=PLATFORM_COLORS[platform], width=3),
            marker=dict(size=6),
            customdata=sub["represented_sors"],
            hovertemplate=(
                f"<b>{platform}</b> (%{{x}})<br>"
                "Decision Automation: <b>%{y:.2f}%</b><br>"
                "Represented SoRs: <b>%{customdata:,.0f}</b>"
                "<extra></extra>"
            ),
        )
    )

layout_monthly = get_premium_plotly_layout(
    xaxis_title="",
    yaxis_title="Decision Automation (%)",
    height=360,
    showlegend=True,
)
layout_monthly["yaxis"]["range"] = [-3, 105]
layout_monthly["yaxis"]["ticksuffix"] = "%"
fig_monthly.update_layout(layout_monthly)

st.plotly_chart(fig_monthly, use_container_width=True, config=dict(displayModeBar=False))


# -----------------------------------------------------------------------------
# SECTION 04: WHY OVERALL AVERAGES MISLEAD (Category Composition)
# -----------------------------------------------------------------------------
render_html("""
    <div id='04-why-overall-averages-mislead' class='section-anchor'>
        <span class='section-num'>04</span>
        <h2 class='section-title'>WHY OVERALL AVERAGES MISLEAD</h2>
    </div>
    <div class='section-subtitle'>
        Category mix materially changes the platform-wide comparison.
        Evaluating moderation automation requires controlling for category distribution.
    </div>
    """)

tt_ov = df_overall.loc["TikTok", "decision_with_any_automation_rate"] * 100
yt_ov = df_overall.loc["YouTube", "decision_with_any_automation_rate"] * 100

tc_data = df_cat[df_cat["category"] == "STATEMENT_CATEGORY_OTHER_VIOLATION_TC"].set_index("platform")
tt_tc = tc_data.loc["TikTok", "decision_with_any_automation_rate"] * 100
yt_tc = tc_data.loc["YouTube", "decision_with_any_automation_rate"] * 100

col_m1, col_m2 = st.columns(2, gap="large")

with col_m1:
    render_html(f"""
        <div class='premium-card' style='height:100%;'>
            <div style='font-size:0.75rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:{THEME["text_muted"]};'>
                PLATFORM-WIDE OVERALL (ALL CATEGORIES)
            </div>
            <div style='display:flex; justify-content:space-between; align-items:baseline; margin-top:0.75rem;'>
                <div style='font-family:JetBrains Mono, monospace; font-size:2.6rem; font-weight:800; color:{THEME["text_primary"]};'>+37.76 pp</div>
                <div class='pill-badge' style='color:{THEME["text_muted"]};'>661.7M SORS</div>
            </div>
            <div style='margin:1rem 0; font-size:0.9rem; color:{THEME["text_secondary"]};'>
                TikTok: <b>{tt_ov:.2f}%</b> · YouTube: <b>{yt_ov:.2f}%</b>
            </div>
            <p style='font-size:0.84rem; color:{THEME["text_muted"]}; margin:0; line-height:1.5;'>
                Platform-wide averages show a 37.76 percentage-point difference.
            </p>
        </div>
        """)

with col_m2:
    render_html(f"""
        <div class='premium-card' style='height:100%; border-color:rgba(16, 185, 129, 0.3);'>
            <div style='font-size:0.75rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:{THEME["accent_green"]};'>
                SAME CATEGORY · TERMS OF SERVICE VIOLATIONS
            </div>
            <div style='display:flex; justify-content:space-between; align-items:baseline; margin-top:0.75rem;'>
                <div style='font-family:JetBrains Mono, monospace; font-size:2.6rem; font-weight:800; color:{THEME["accent_green"]};'>+0.06 pp</div>
                <div class='pill-badge' style='border-color:rgba(16, 185, 129, 0.3); color:{THEME["accent_green"]};'>400.8M SORS</div>
            </div>
            <div style='margin:1rem 0; font-size:0.9rem; color:{THEME["text_secondary"]};'>
                TikTok: <b>{tt_tc:.2f}%</b> · YouTube: <b>{yt_tc:.2f}%</b>
            </div>
            <p style='font-size:0.84rem; color:{THEME["text_muted"]}; margin:0; line-height:1.5;'>
                Within Other Terms of Service Violations, the difference narrows to 0.06 percentage points (TikTok 93.84% vs YouTube 93.78%).
            </p>
        </div>
        """)

with st.expander("🔬 Sensitivity Decomposition Methodology Note"):
    st.markdown(
        """
        - **Sensitivity Range**: Depending on the counterfactual decomposition convention used, the estimated contribution of category composition to the overall platform automation gap ranged from **29.2% to 87.0%**; **55.0% in the shared-category / overlapping-subset decomposition**.
        - **Conservative Scientific Conclusion**: Rather than relying on a single point estimate, this benchmark establishes the robust finding that:  
          *"A substantial portion of the overall difference is associated with category composition."*
        - **Analytical Standard**: Cross-platform moderation benchmarks must always be conducted at the specific policy category level rather than relying on aggregate corporate averages.
        """
    )


# -----------------------------------------------------------------------------
# SECTION 05: HOW ENFORCEMENT DIFFERS (Enforcement Profiles)
# -----------------------------------------------------------------------------
render_html(
    """
    <div id='05-how-enforcement-differs' class='section-anchor'>
        <span class='section-num'>05</span>
        <h2 class='section-title'>HOW ENFORCEMENT DIFFERS</h2>
    </div>
    <div class='section-subtitle'>
        Platforms enforce actions at fundamentally different entity layers (content assets vs user accounts).
    </div>
    """
)

top_actions = ["CONTENT_REMOVED", "VISIBILITY_OTHER", "ACCOUNT_TERMINATED"]
piv_enf = df_enf_ov.pivot(index="platform", columns="action", values="action_prevalence").fillna(0) * 100

fig_enf = go.Figure()
for platform in ["Instagram", "TikTok", "YouTube"]:
    action_vals = [piv_enf.loc[platform, a] if a in piv_enf.columns else 0 for a in top_actions]
    fig_enf.add_trace(
        go.Bar(
            y=[humanize_action(a) for a in top_actions],
            x=action_vals,
            name=platform,
            orientation="h",
            marker_color=PLATFORM_COLORS[platform],
            text=[f"<b>{v:.1f}%</b>" if v > 0.5 else ("<0.1%" if v > 0 else "0.0%") for v in action_vals],
            textposition="outside",
            hovertemplate=f"<b>{platform}</b><br>%{{y}}: %{{x:.2f}}%<extra></extra>",
        )
    )

layout_enf = get_premium_plotly_layout(
    xaxis_title="Prevalence (% of Represented SoRs)",
    height=300,
    showlegend=True,
)
layout_enf["xaxis"]["range"] = [0, 110]
layout_enf["xaxis"]["ticksuffix"] = "%"
fig_enf.update_layout(layout_enf)

st.plotly_chart(fig_enf, use_container_width=True, config=dict(displayModeBar=False))

render_html(f"""
    <div style='display:flex; justify-content:space-between; align-items:center; background-color:{THEME["card_bg"]}; border:1px solid {THEME["card_border"]}; border-radius:12px; padding:1rem 1.25rem; margin-top:0.5rem; flex-wrap:wrap; gap:1rem;'>
        <div style='font-size:0.84rem; color:{THEME["text_secondary"]};'>
            <span class='pill-badge' style='margin-right:0.5rem;'>MULTI-LABEL METRIC</span>
            An SoR may contain more than one enforcement action; percentages represent independent prevalence and need not sum to 100%.
        </div>
        <div style='font-size:0.84rem; color:{PLATFORM_COLORS["Instagram"]}; font-weight:700;'>
            Instagram Scams: 98.77% ACCOUNT_TERMINATED (47.4M of 48.0M SoRs)
        </div>
    </div>
    """)


# -----------------------------------------------------------------------------
# SECTION 06: EXPLORE THE DATA (Contained Workspace)
# -----------------------------------------------------------------------------
render_html("""
    <div id='06-explore-the-data' class='section-anchor'>
        <span class='section-num'>06</span>
        <h2 class='section-title'>EXPLORE THE DATA</h2>
    </div>
    <div class='section-subtitle'>
        Examine policy category distributions, sparse slice flags, and decision automation across platforms.
    </div>
    """)

df_cat_filtered = df_cat[df_cat["platform"].isin(selected_platforms)].copy()
if hide_sparse:
    df_cat_filtered = df_cat_filtered[~df_cat_filtered["sparse_flag"]]

df_cat_filtered["human_category"] = df_cat_filtered["category"].apply(humanize_category)

cat_order = (
    df_cat_filtered.groupby("human_category")["represented_sors"]
    .sum()
    .sort_values(ascending=True)
    .index.tolist()
)

fig_cat = go.Figure()
for platform in selected_platforms:
    sub = df_cat_filtered[df_cat_filtered["platform"] == platform].set_index("human_category")
    sub = sub.reindex(cat_order).dropna(subset=["category"])

    y_cats = sub.index.tolist()
    x_rates = (sub[metric_choice] * 100).tolist()
    sors_vals = sub["represented_sors"].tolist()
    sparse_vals = sub["sparse_flag"].tolist()

    text_labels = [
        f"{r:.1f}%" if pd.notna(r) else "N/A"
        for r in x_rates
    ]

    fig_cat.add_trace(
        go.Bar(
            y=y_cats,
            x=x_rates,
            name=platform,
            orientation="h",
            marker_color=PLATFORM_COLORS[platform],
            text=text_labels,
            textposition="outside",
            customdata=list(zip(sors_vals, sparse_vals)),
            hovertemplate=(
                f"<b>{platform}</b> · %{{y}}<br>"
                f"{METRIC_LABELS.get(metric_choice, metric_choice)}: <b>%{{x:.2f}}%</b><br>"
                "Represented SoRs: <b>%{customdata[0]:,.0f}</b><br>"
                "Low-Volume Flag (<0.10%): <b>%{customdata[1]}</b>"
                "<extra></extra>"
            ),
        )
    )

layout_cat = get_premium_plotly_layout(
    xaxis_title=f"{METRIC_LABELS.get(metric_choice, metric_choice)} (%)",
    height=max(420, len(cat_order) * 32),
    barmode="group",
)
layout_cat["xaxis"]["range"] = [0, 115]
layout_cat["xaxis"]["ticksuffix"] = "%"
fig_cat.update_layout(layout_cat)

st.plotly_chart(fig_cat, use_container_width=True, config=dict(displayModeBar=False))

render_html(f"""
    <div style='font-size:0.78rem; color:{THEME["text_muted"]}; margin-top:0.5rem;'>
        <b>Display Standards:</b> Slices marked as low-volume represent &lt;0.10% of a platform's total benchmark volume. Zero-volume combinations display <b>N/A</b>, never 0%.
    </div>
    """)

with st.expander("📋 View Category Benchmark Data Table", expanded=False):
    table_df = df_cat_filtered.copy().sort_values(by=["human_category", "platform"])
    table_display = pd.DataFrame({
        "Category": table_df["human_category"],
        "Platform": table_df["platform"],
        "Represented SoRs": table_df["represented_sors"].apply(lambda v: f"{int(v):,}"),
        "Decision Automation": table_df["decision_with_any_automation_rate"].apply(lambda v: format_pct(v)),
        "Automated Detection": table_df["automated_detection_rate"].apply(lambda v: format_pct(v)),
        "Fully Automated": table_df["fully_automated_decision_rate"].apply(lambda v: format_pct(v)),
        "Low Volume (<0.10%)": table_df["sparse_flag"].apply(lambda s: "Yes (<0.10%)" if s else "No"),
    })
    st.dataframe(table_display, hide_index=True, use_container_width=True)


# -----------------------------------------------------------------------------
# SECTION 07: WHAT SHOULD A SAFETY TEAM DO? (Recommendation Panel)
# -----------------------------------------------------------------------------
render_html("""
    <div id='07-what-should-a-safety-team-do' class='section-anchor'>
        <span class='section-num'>07</span>
        <h2 class='section-title'>WHAT SHOULD A SAFETY TEAM DO?</h2>
    </div>
    """)

render_html(f"""
    <div class='rec-banner'>
        <div style='font-size: 0.74rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: {THEME["accent_green"]};'>
            TRUST & SAFETY ACTION
        </div>
        <h3 style='font-size: 1.6rem; font-weight: 800; color: {THEME["text_primary"]}; margin: 0.35rem 0 0.5rem 0; letter-spacing: -0.02em;'>
            Audit the automation boundary — don't blindly move it.
        </h3>
        <p style='font-size: 0.95rem; color: {THEME["text_secondary"]}; max-width: 780px; line-height: 1.5; margin-bottom: 1.25rem;'>
            The benchmark identifies where automation differs, not which platform is right. Where a platform reports unusually low or unusually high decision automation relative to peers, safety operations should systematically evaluate:
        </p>
        <div class='rec-grid'>
            <div class='rec-pill'>FALSE POSITIVES</div>
            <div class='rec-pill'>APPEALS</div>
            <div class='rec-pill'>REVERSALS</div>
            <div class='rec-pill'>HANDLING TIME</div>
            <div class='rec-pill'>HARM SEVERITY</div>
            <div class='rec-pill'>ESCALATION PATTERNS</div>
        </div>
        <div style='font-size: 0.85rem; color: {THEME["text_muted"]}; border-top: 1px solid rgba(16, 185, 129, 0.2); padding-top: 0.85rem; line-height: 1.5;'>
            <b>Core Operational Principle:</b> This benchmark identifies <i>where investigation is warranted</i>. It does not establish which platform has the optimal automation level. More automation is not automatically better, and less automation is not automatically safer.
        </div>
    </div>
    """)


# -----------------------------------------------------------------------------
# SECTION 08: METHODOLOGY & LIMITATIONS
# -----------------------------------------------------------------------------
render_html("""
    <div id='08-limitations-methodology' class='section-anchor'>
        <span class='section-num'>08</span>
        <h2 class='section-title'>METHODOLOGY & LIMITATIONS</h2>
    </div>
    """)

with st.expander("⚠️ Scientific Caveats & Reporting Boundaries", expanded=False):
    st.markdown(
        """
        To maintain scientific and analytical integrity, benchmark metrics must be interpreted within documented boundaries:
        
        1. **Administrative Statements of Reasons**: DSA data captures moderation actions taken and reported under Article 17; it does not measure total violative content prevalence or user exposure.
        2. **Automation Involvement ≠ Accuracy**: Regulatory records document whether automated means participated in decisions; they do not measure precision, recall, false-positive rates, or false-negative rates.
        3. **No User Appeal Outcomes in Aggregates**: Parquet aggregates do not link initial Statements of Reasons to subsequent appeal outcomes or content restorations.
        4. **Handling Latency Is Unobserved**: Public aggregates do not track queue transit times or handling durations.
        5. **Within-Category Composition**: Unobserved differences in language, content format (short-form video vs long-form video vs photo/story), or geographic origin may exist within categories.
        6. **Platform Reporting Architecture Disparities**: Differences in action prevalence (e.g. account termination vs content removal) reflect divergent entity architectures and compliance logging models.
        7. **TikTok January 2026 Batch Reporting**: TikTok's January 2026 submissions reflect delayed batch processing from late 2025; sensitivity testing confirms that excluding January shifts its automation metrics by **<0.25 percentage points**.
        """
    )

render_html(
    f"""
    <div style='background-color:{THEME["card_bg"]}; border:1px solid {THEME["card_border"]}; border-radius:12px; padding:1.25rem 1.5rem; margin-top:1rem; font-size:0.84rem; color:{THEME["text_secondary"]}; line-height:1.6;'>
        <b>Methodological Artifacts & Verification:</b><br>
        • Full Benchmark Report: <code>reports/final_report.md</code><br>
        • Arithmetic Validation Audit: <code>reports/phase5_validation.md</code><br>
        • Candidate Finding Scorecard: <code>reports/phase6_candidate_findings.md</code><br>
        • 12-Rule Technical Specification: <code>MAPPING.md</code><br>
        • Regulatory Endpoint: <a href='https://transparency.dsa.ec.europa.eu/' target='_blank' style='color:{THEME["accent_blue"]}; text-decoration:none;'>EU DSA Transparency Database</a>
    </div>
    """)
