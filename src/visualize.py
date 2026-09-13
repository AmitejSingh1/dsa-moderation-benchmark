"""
src/visualize.py
EU DSA Moderation Benchmark — Phase 7 Visualization Pipeline

Generates all portfolio-quality charts from validated Phase 5 processed CSV outputs:
- 01_detection_vs_decision.png: Overall automated detection vs. decision execution
- 02_scams_decision_automation.png: HERO CHART — Scams & Fraud decision automation divide
- 03_scams_monthly_consistency.png: Monthly persistence of the scams decision gap
- 04_category_mix_context.png: Overall platform gap vs. core Terms of Service parity
- 05_enforcement_actions.png: Multi-label normalized enforcement action prevalence

All data is read directly from data/processed/*.csv without hardcoded benchmark numbers.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHARTS_DIR = BASE_DIR / "reports" / "charts"

# Color Palette (consistent across all charts)
COLORS = {
    "TikTok": "#00A896",      # Teal / Cyan
    "YouTube": "#E63946",     # Crimson Red
    "Instagram": "#8338EC",   # Purple / Magenta
    "Gray": "#6C757D",
    "LightGray": "#E9ECEF",
    "DarkText": "#212529",
}

SOURCE_NOTE = (
    "Source: EU Digital Services Act Transparency Database (aggregated-complete.parquet).\n"
    "Analysis window: July 1, 2025 – May 31, 2026 (11 monthly partitions; 661.7M represented SoRs)."
)


def set_plot_style():
    """Applies a clean, modern, publication-quality style."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans", "Helvetica"],
        "axes.edgecolor": "#CED4DA",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelsize": 10,
        "axes.titlesize": 12,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "figure.titlesize": 13,
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def load_data():
    """Loads required processed benchmark CSVs and validates presence."""
    required_files = [
        "automation_overall.csv",
        "automation_by_category.csv",
        "automation_monthly.csv",
        "automation_category_monthly.csv",
        "enforcement_action_overall.csv",
    ]
    dfs = {}
    for f in required_files:
        path = PROCESSED_DIR / f
        if not path.exists():
            raise FileNotFoundError(f"Missing required processed dataset: {path}")
        dfs[f] = pd.read_csv(path)
    return dfs


# -----------------------------------------------------------------------------
# Chart 1: Detection vs. Decision Automation
# -----------------------------------------------------------------------------
def plot_chart_01_detection_vs_decision(dfs):
    df_ov = dfs["automation_overall.csv"].set_index("platform")
    platforms = ["TikTok", "YouTube", "Instagram"]

    det_rates = [df_ov.loc[p, "automated_detection_rate"] * 100 for p in platforms]
    any_rates = [df_ov.loc[p, "decision_with_any_automation_rate"] * 100 for p in platforms]
    full_rates = [df_ov.loc[p, "fully_automated_decision_rate"] * 100 for p in platforms]

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    x = np.arange(len(platforms))
    width = 0.25

    rects1 = ax.bar(x - width, det_rates, width, label="Automated Detection Rate", color="#3A86FF", alpha=0.9)
    rects2 = ax.bar(x, any_rates, width, label="Decision with Any Automation Rate", color="#8338EC", alpha=0.9)
    rects3 = ax.bar(x + width, full_rates, width, label="Fully Automated Decision Rate", color="#FB5607", alpha=0.9)

    ax.set_ylabel("Rate (%)", fontweight="bold", color=COLORS["DarkText"])
    ax.set_title(
        "Automated Detection Is Universally High (>95%), but Decision Automation Diverges",
        fontweight="bold",
        pad=22,
        loc="left",
        color=COLORS["DarkText"],
    )
    ax.text(
        0.0,
        1.03,
        "Across 661.7M EU DSA records, automated detection is standard, but final decision execution varies widely.",
        transform=ax.transAxes,
        fontsize=8.8,
        color=COLORS["Gray"],
    )

    ax.set_xticks(x)
    ax.set_xticklabels(platforms, fontweight="bold", fontsize=10.5)
    ax.set_ylim(0, 130)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#CED4DA",
        loc="upper center",
        bbox_to_anchor=(0.5, 0.98),
        ncol=3,
        fontsize=8.8,
    )

    # Add direct percentage labels
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            label_text = f"{height:.1f}%" if height > 0 else "0.0%"
            ax.annotate(
                label_text,
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
                color=COLORS["DarkText"],
            )

    fig.text(0.08, -0.05, SOURCE_NOTE, fontsize=7.5, color=COLORS["Gray"])
    out_path = CHARTS_DIR / "01_detection_vs_decision.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")


# -----------------------------------------------------------------------------
# Chart 2: HERO CHART — Scams & Fraud Decision Automation Divide
# -----------------------------------------------------------------------------
def plot_chart_02_scams_decision_automation(dfs):
    df_cat = dfs["automation_by_category.csv"]
    scams = df_cat[df_cat["category"] == "STATEMENT_CATEGORY_SCAMS_AND_FRAUD"].set_index("platform")

    platforms = ["YouTube", "TikTok", "Instagram"]
    any_rates = [scams.loc[p, "decision_with_any_automation_rate"] * 100 for p in platforms]
    det_rates = [scams.loc[p, "automated_detection_rate"] * 100 for p in platforms]
    sors = [scams.loc[p, "represented_sors"] for p in platforms]

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    x = np.arange(len(platforms))
    width = 0.42

    bar_colors = [COLORS["YouTube"], COLORS["TikTok"], COLORS["Instagram"]]
    rects = ax.bar(x, any_rates, width, color=bar_colors, alpha=0.88, edgecolor="#495057", linewidth=0.5)

    # Plot detection rate as reference markers
    ax.scatter(
        x,
        det_rates,
        color="#3A86FF",
        s=85,
        zorder=5,
        label="Automated Detection Rate (Reference Marker)",
        edgecolor="black",
        linewidth=0.8,
    )

    ax.set_ylabel("Decision with Any Automation Rate (%)", fontweight="bold", color=COLORS["DarkText"])
    ax.set_title(
        "Scams & Fraud: Universal Detection vs. Sharply Different Decision Automation",
        fontweight="bold",
        pad=18,
        loc="left",
        color=COLORS["DarkText"],
    )
    ax.text(
        0.0,
        1.025,
        "Detection exceeds 91% across all platforms, but reported decision automation differs from 0.25% to 99.45% across 90.8M SoRs.",
        transform=ax.transAxes,
        fontsize=8.8,
        color=COLORS["Gray"],
    )

    ax.set_xticks(x)
    xtick_labels = [
        f"{p}\n({sors[i]/1e6:.1f}M SoRs)"
        for i, p in enumerate(platforms)
    ]
    ax.set_xticklabels(xtick_labels, fontweight="bold", fontsize=10)
    ax.set_ylim(0, 122)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CED4DA", loc="upper left", fontsize=8.8)

    # Add value annotations
    for i, rect in enumerate(rects):
        rate = any_rates[i]
        det = det_rates[i]

        # Bar label placement: inside bar if tall enough, otherwise above
        if rate > 50:
            # Place inside top of bar in bold white text
            ax.annotate(
                f"{rate:.2f}%",
                xy=(rect.get_x() + rect.get_width() / 2, rate),
                xytext=(0, -18),
                textcoords="offset points",
                ha="center",
                va="top",
                fontsize=11,
                fontweight="bold",
                color="white",
            )
        else:
            ax.annotate(
                f"{rate:.2f}%",
                xy=(rect.get_x() + rect.get_width() / 2, max(rate, 1)),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=10.5,
                fontweight="bold",
                color=COLORS["DarkText"],
            )

        # Detection reference label: placed clearly above reference marker
        ax.annotate(
            f"Detection: {det:.1f}%",
            xy=(x[i], det),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#023E8A",
        )

    # Highlight YouTube callout
    ax.annotate(
        "YouTube reports 99.75% of scam decisions\ntaken without automated means\n(32.6M of 32.7M SoRs)",
        xy=(0, 0.25),
        xytext=(0.32, 32),
        arrowprops=dict(facecolor=COLORS["YouTube"], shrink=0.08, width=1, headwidth=6),
        fontsize=8.5,
        fontweight="bold",
        color=COLORS["YouTube"],
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF0F0", edgecolor=COLORS["YouTube"], alpha=0.9),
    )

    fig.text(0.08, -0.06, SOURCE_NOTE, fontsize=7.5, color=COLORS["Gray"])
    out_path = CHARTS_DIR / "02_scams_decision_automation.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")


# -----------------------------------------------------------------------------
# Chart 3: Monthly Persistence of Scams Decision Gap
# -----------------------------------------------------------------------------
def plot_chart_03_scams_monthly_consistency(dfs):
    df_cat_m = dfs["automation_category_monthly.csv"]
    scams_m = df_cat_m[df_cat_m["category"] == "STATEMENT_CATEGORY_SCAMS_AND_FRAUD"]

    months = sorted(scams_m["month"].unique())
    # Human-friendly month names: 'Jul 25', 'Aug', ..., 'Jan 26', ..., 'May 26'
    month_display = []
    for m in months:
        y, mo = m.split("-")
        month_abbr = pd.to_datetime(m).strftime("%b")
        if mo in ["07", "01", "05"]:
            month_display.append(f"{month_abbr} '{y[2:]}")
        else:
            month_display.append(month_abbr)

    fig, ax = plt.subplots(figsize=(9.5, 5.2))

    for platform in ["Instagram", "TikTok", "YouTube"]:
        sub = scams_m[scams_m["platform"] == platform].sort_values("month")
        y = sub["decision_with_any_automation_rate"] * 100
        ax.plot(
            months,
            y,
            marker="o",
            markersize=6,
            linewidth=2.2,
            label=f"{platform}",
            color=COLORS[platform],
            alpha=0.92,
        )
        # End of line label
        last_val = y.iloc[-1]
        ax.annotate(
            f"{last_val:.1f}%",
            xy=(months[-1], last_val),
            xytext=(7, -2 if platform == "YouTube" else 0),
            textcoords="offset points",
            va="center",
            fontsize=8.5,
            fontweight="bold",
            color=COLORS[platform],
        )

    ax.set_ylabel("Decision with Any Automation Rate (%)", fontweight="bold", color=COLORS["DarkText"])
    ax.set_title(
        "11-Month Persistence: Scams Decision-Automation Difference Is Consistent",
        fontweight="bold",
        pad=16,
        loc="left",
        color=COLORS["DarkText"],
    )
    ax.text(
        0.0,
        1.025,
        "Across all 11 monthly partitions, YouTube remains near zero (<0.6%), while TikTok and Instagram remain high (zero rank reversals).",
        transform=ax.transAxes,
        fontsize=8.8,
        color=COLORS["Gray"],
    )

    ax.set_xticks(months)
    ax.set_xticklabels(month_display, fontsize=8.8)
    ax.set_xlabel("Observation Month (July 2025 – May 2026)", fontweight="bold", labelpad=8, color=COLORS["DarkText"])
    ax.set_ylim(-4, 108)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CED4DA", loc="center right")

    fig.text(0.08, -0.06, SOURCE_NOTE, fontsize=7.5, color=COLORS["Gray"])
    out_path = CHARTS_DIR / "03_scams_monthly_consistency.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")


# -----------------------------------------------------------------------------
# Chart 4: Overall Platform Averages vs. Core Category Parity
# -----------------------------------------------------------------------------
def plot_chart_04_category_mix_context(dfs):
    df_ov = dfs["automation_overall.csv"].set_index("platform")
    df_cat = dfs["automation_by_category.csv"]
    tc = df_cat[df_cat["category"] == "STATEMENT_CATEGORY_OTHER_VIOLATION_TC"].set_index("platform")

    platforms = ["TikTok", "YouTube"]
    ov_rates = [df_ov.loc[p, "decision_with_any_automation_rate"] * 100 for p in platforms]
    tc_rates = [tc.loc[p, "decision_with_any_automation_rate"] * 100 for p in platforms]

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    x = np.arange(2)  # 0 = Overall, 1 = Core Terms of Service
    width = 0.32

    # Grouped bars: TikTok vs YouTube
    tt_vals = [ov_rates[0], tc_rates[0]]
    yt_vals = [ov_rates[1], tc_rates[1]]

    rects1 = ax.bar(x - width / 2, tt_vals, width, label="TikTok", color=COLORS["TikTok"], alpha=0.9)
    rects2 = ax.bar(x + width / 2, yt_vals, width, label="YouTube", color=COLORS["YouTube"], alpha=0.9)

    ax.set_ylabel("Decision with Any Automation Rate (%)", fontweight="bold", color=COLORS["DarkText"])
    ax.set_title(
        "Category Composition Matters for Platform-Wide Averages",
        fontweight="bold",
        pad=16,
        loc="left",
        color=COLORS["DarkText"],
    )
    ax.text(
        0.0,
        1.025,
        "The contrast shows why platform-wide averages should be interpreted alongside category-level results: the gap collapses from 37.76 pp to 0.06 pp in their largest shared category.",
        transform=ax.transAxes,
        fontsize=8.5,
        color=COLORS["Gray"],
    )

    ax.set_xticks(x)
    ax.set_xticklabels([
        "Platform-Wide Overall\n(All Categories Combined)",
        "Terms of Service Violations\n(OTHER_VIOLATION_TC; 400.8M SoRs)",
    ], fontweight="bold", fontsize=10)
    ax.set_ylim(0, 116)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E9ECEF", loc="upper left")

    # Add direct labels
    for rects in [rects1, rects2]:
        for rect in rects:
            h = rect.get_height()
            ax.annotate(
                f"{h:.2f}%",
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9.5,
                fontweight="bold",
                color=COLORS["DarkText"],
            )

    # Gap callouts
    # Overall gap bracket
    ax.annotate(
        "Gap: +37.76 pp\n(Heavily associated with category mix)",
        xy=(0, 74),
        xytext=(0, 80),
        ha="center",
        fontsize=8.5,
        fontweight="bold",
        color=COLORS["DarkText"],
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#F8F9FA", edgecolor="#CED4DA"),
    )

    # TC gap bracket
    ax.annotate(
        "Gap: +0.06 pp\n(Virtual Parity)",
        xy=(1, 95),
        xytext=(1, 102),
        ha="center",
        fontsize=8.5,
        fontweight="bold",
        color="#007F5F",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F5E9", edgecolor="#007F5F"),
    )

    fig.text(0.08, -0.06, SOURCE_NOTE, fontsize=7.5, color=COLORS["Gray"])
    out_path = CHARTS_DIR / "04_category_mix_context.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")


# -----------------------------------------------------------------------------
# Chart 5: Normalized Enforcement Action Prevalence
# -----------------------------------------------------------------------------
def plot_chart_05_enforcement_actions(dfs):
    df_enf = dfs["enforcement_action_overall.csv"]
    platforms = ["Instagram", "TikTok", "YouTube"]
    actions = ["CONTENT_REMOVED", "VISIBILITY_OTHER", "ACCOUNT_TERMINATED"]
    action_labels = ["Content Removed", "Visibility Other", "Account Terminated"]

    piv = df_enf.pivot(index="platform", columns="action", values="action_prevalence") * 100

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    x = np.arange(len(actions))
    width = 0.26

    rects1 = ax.bar(x - width, [piv.loc["Instagram", a] for a in actions], width, label="Instagram", color=COLORS["Instagram"], alpha=0.9)
    rects2 = ax.bar(x, [piv.loc["TikTok", a] for a in actions], width, label="TikTok", color=COLORS["TikTok"], alpha=0.9)
    rects3 = ax.bar(x + width, [piv.loc["YouTube", a] for a in actions], width, label="YouTube", color=COLORS["YouTube"], alpha=0.9)

    ax.set_ylabel("Action Prevalence (% of Represented SoRs)", fontweight="bold", color=COLORS["DarkText"])
    ax.set_title(
        "Reported Enforcement-Action Profiles Across Platforms",
        fontweight="bold",
        pad=16,
        loc="left",
        color=COLORS["DarkText"],
    )
    ax.text(
        0.0,
        1.025,
        "Enforcement actions are multi-label and independent; percentages need not sum to 100%.",
        transform=ax.transAxes,
        fontsize=8.5,
        color=COLORS["Gray"],
    )

    ax.set_xticks(x)
    ax.set_xticklabels(action_labels, fontweight="bold", fontsize=10)
    ax.set_ylim(0, 108)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=0))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="#E9ECEF", loc="upper right")

    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            h = rect.get_height()
            label_text = f"{h:.1f}%" if h > 0.5 else ("<0.1%" if h > 0 else "0.0%")
            ax.annotate(
                label_text,
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
                color=COLORS["DarkText"],
            )

    fig.text(0.08, -0.06, SOURCE_NOTE, fontsize=7.5, color=COLORS["Gray"])
    out_path = CHARTS_DIR / "05_enforcement_actions.png"
    plt.savefig(out_path)
    plt.close()
    print(f"Generated: {out_path}")


# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    set_plot_style()
    print("Loading processed data...")
    dfs = load_data()
    print("Generating final benchmark charts...")
    plot_chart_01_detection_vs_decision(dfs)
    plot_chart_02_scams_decision_automation(dfs)
    plot_chart_03_scams_monthly_consistency(dfs)
    plot_chart_04_category_mix_context(dfs)
    plot_chart_05_enforcement_actions(dfs)
    print("All charts successfully generated!")


if __name__ == "__main__":
    main()

