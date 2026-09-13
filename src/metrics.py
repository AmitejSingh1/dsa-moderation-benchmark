"""
src/metrics.py
Core metrics calculation pipeline for Phase 5 content moderation benchmark.

Implements all 12 approved methodological rules from MAPPING.md:
- Uses SUM(count) weighting for all rates
- Computes volume, automation, and enforcement metrics across:
  - Overall platform level
  - Category breakdown (with project-defined <0.10% sparsity flag)
  - Monthly time-series
  - Category x Monthly matrix
- Multi-label granular enforcement prevalence across 15 actions
- Pairwise platform effect sizes (percentage-point differences and rate ratios)
- Complete population and additivity validations
"""

import sys
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from src.load_dsa import (
    CORE_PLATFORMS,
    DEFAULT_DSA_PATH,
    iter_harmonized_monthly_batches,
)

PROCESSED_DIR = Path("data/processed")

# Canonical 16 categories observed in Era 2
CANONICAL_CATEGORIES = [
    "STATEMENT_CATEGORY_OTHER_VIOLATION_TC",
    "STATEMENT_CATEGORY_SCAMS_AND_FRAUD",
    "STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH",
    "STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS",
    "STATEMENT_CATEGORY_VIOLENCE",
    "STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS",
    "STATEMENT_CATEGORY_PROTECTION_OF_MINORS",
    "STATEMENT_CATEGORY_CONSUMER_INFORMATION",
    "STATEMENT_CATEGORY_UNSAFE_AND_PROHIBITED_PRODUCTS",
    "STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS",
    "STATEMENT_CATEGORY_SELF_HARM",
    "STATEMENT_CATEGORY_ANIMAL_WELFARE",
    "STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY",
    "STATEMENT_CATEGORY_CYBER_VIOLENCE",
    "STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE",
    "STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT",
]

# Canonical 15 granular enforcement actions
ENFORCEMENT_ACTIONS = [
    "CONTENT_REMOVED",
    "VISIBILITY_OTHER",
    "CONTENT_DISABLED",
    "CONTENT_AGE_RESTRICTED",
    "CONTENT_DEMOTED",
    "CONTENT_INTERACTION_RESTRICTED",
    "CONTENT_LABELLED",
    "ACCOUNT_TERMINATED",
    "ACCOUNT_SUSPENDED",
    "PROVISION_PARTIAL_SUSPENSION",
    "PROVISION_PARTIAL_TERMINATION",
    "PROVISION_TOTAL_SUSPENSION",
    "PROVISION_TOTAL_TERMINATION",
    "MONETARY_TERMINATION",
    "MONETARY_SUSPENSION",
]

# Expected population totals for strict reconciliation
EXPECTED_POPULATION = {
    "TikTok": 480_532_153,
    "YouTube": 88_376_558,
    "Instagram": 92_756_287,
    "TOTAL": 661_664_998,
}


def aggregate_batches(dsa_path: Path = DEFAULT_DSA_PATH) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Stream through the 11 monthly partitions and accumulate compact summary tables:
    1. auto_summary: grouped by (month, platform_name, category, automated_detection, automated_decision)
    2. enforce_summary: grouped by (platform_name, category, action)
    """
    auto_records = []
    enforce_records = []

    for month_label, df in iter_harmonized_monthly_batches(dsa_path=dsa_path):
        # 1. Automation grouping
        grouped_auto = (
            df.groupby(
                ["month", "platform_name", "category", "automated_detection", "automated_decision"],
                observed=False,
            )["count"]
            .sum()
            .reset_index()
        )
        auto_records.append(grouped_auto)

        # 2. Granular enforcement action mappings
        action_conditions = {
            "CONTENT_REMOVED": df["DECISION_VISIBILITY_CONTENT_REMOVED"] == True,
            "VISIBILITY_OTHER": df["DECISION_VISIBILITY_OTHER"] == True,
            "CONTENT_DISABLED": df["DECISION_VISIBILITY_CONTENT_DISABLED"] == True,
            "CONTENT_AGE_RESTRICTED": df["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"] == True,
            "CONTENT_DEMOTED": df["DECISION_VISIBILITY_CONTENT_DEMOTED"] == True,
            "CONTENT_INTERACTION_RESTRICTED": df["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"] == True,
            "CONTENT_LABELLED": df["DECISION_VISIBILITY_CONTENT_LABELLED"] == True,
            "ACCOUNT_TERMINATED": df["decision_account"] == "DECISION_ACCOUNT_TERMINATED",
            "ACCOUNT_SUSPENDED": df["decision_account"] == "DECISION_ACCOUNT_SUSPENDED",
            "PROVISION_PARTIAL_SUSPENSION": df["decision_provision"] == "DECISION_PROVISION_PARTIAL_SUSPENSION",
            "PROVISION_PARTIAL_TERMINATION": df["decision_provision"] == "DECISION_PROVISION_PARTIAL_TERMINATION",
            "PROVISION_TOTAL_TERMINATION": df["decision_provision"] == "DECISION_PROVISION_TOTAL_TERMINATION",
            "PROVISION_TOTAL_SUSPENSION": df["decision_provision"] == "DECISION_PROVISION_TOTAL_SUSPENSION",
            "MONETARY_TERMINATION": df["decision_monetary"] == "DECISION_MONETARY_TERMINATION",
            "MONETARY_SUSPENSION": df["decision_monetary"] == "DECISION_MONETARY_SUSPENSION",
        }

        for act_name, cond in action_conditions.items():
            sub = df[cond]
            if len(sub) > 0:
                act_grouped = (
                    sub.groupby(["platform_name", "category"], observed=False)["count"]
                    .sum()
                    .reset_index()
                )
                act_grouped["action"] = act_name
                act_grouped.rename(columns={"count": "action_numerator"}, inplace=True)
                enforce_records.append(act_grouped)

    auto_df = pd.concat(auto_records, ignore_index=True)
    enforce_df = pd.concat(enforce_records, ignore_index=True)

    # Consolidate enforcement records across months
    if len(enforce_df) > 0:
        enforce_df = (
            enforce_df.groupby(["platform_name", "category", "action"], observed=False)[
                "action_numerator"
            ]
            .sum()
            .reset_index()
        )

    return auto_df, enforce_df


def build_category_volume(auto_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build platform / category volume table (category_volume.csv).
    Includes a complete 48-row grid (3 platforms x 16 categories) with explicit zero-volume rows.
    """
    obs = (
        auto_df.groupby(["platform_name", "category"], observed=False)["count"]
        .sum()
        .reset_index()
        .rename(columns={"platform_name": "platform", "count": "represented_sors"})
    )

    platform_totals = obs.groupby("platform")["represented_sors"].sum().to_dict()

    # Generate full Cartesian product grid for complete reproducibility
    grid_rows = []
    obs_map = {(r["platform"], r["category"]): r["represented_sors"] for _, r in obs.iterrows()}

    for p in CORE_PLATFORMS:
        p_total = platform_totals.get(p, 0)
        for c in CANONICAL_CATEGORIES:
            sors = obs_map.get((p, c), 0)
            share = sors / p_total if p_total > 0 else 0.0
            sparse_flag = share < 0.001
            grid_rows.append(
                {
                    "platform": p,
                    "category": c,
                    "represented_sors": int(sors),
                    "platform_total_sors": int(p_total),
                    "category_share": round(share, 8),
                    "sparse_flag": bool(sparse_flag),
                }
            )

    vol_df = pd.DataFrame(grid_rows)
    vol_df.sort_values(by=["platform", "represented_sors"], ascending=[True, False], inplace=True)
    return vol_df


def build_automation_overall(auto_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build overall platform automation table (automation_overall.csv).
    """
    rows = []
    for p in CORE_PLATFORMS:
        pdf = auto_df[auto_df["platform_name"] == p]
        tot_sors = int(pdf["count"].sum())

        det_num = int(pdf[pdf["automated_detection"] == "Yes"]["count"].sum())
        fully_num = int(
            pdf[pdf["automated_decision"] == "AUTOMATED_DECISION_FULLY"]["count"].sum()
        )
        any_num = int(
            pdf[
                pdf["automated_decision"].isin(
                    ["AUTOMATED_DECISION_FULLY", "AUTOMATED_DECISION_PARTIALLY"]
                )
            ]["count"].sum()
        )

        rows.append(
            {
                "platform": p,
                "represented_sors": tot_sors,
                "automated_detection_numerator": det_num,
                "automated_detection_rate": round(det_num / tot_sors, 8),
                "fully_automated_decision_numerator": fully_num,
                "fully_automated_decision_rate": round(fully_num / tot_sors, 8),
                "any_automated_decision_numerator": any_num,
                "decision_with_any_automation_rate": round(any_num / tot_sors, 8),
            }
        )

    return pd.DataFrame(rows)


def build_automation_by_category(auto_df: pd.DataFrame, vol_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build automation metrics by category (automation_by_category.csv).
    If denominator = 0, rates are reported as NaN / null, never 0.0.
    """
    cat_summary = (
        auto_df.groupby(
            ["platform_name", "category", "automated_detection", "automated_decision"],
            observed=False,
        )["count"]
        .sum()
        .reset_index()
    )

    rows = []
    for _, vrow in vol_df.iterrows():
        p = vrow["platform"]
        c = vrow["category"]
        sors = int(vrow["represented_sors"])
        share = vrow["category_share"]
        sparse = vrow["sparse_flag"]

        sub = cat_summary[
            (cat_summary["platform_name"] == p) & (cat_summary["category"] == c)
        ]

        det_num = int(sub[sub["automated_detection"] == "Yes"]["count"].sum())
        fully_num = int(
            sub[sub["automated_decision"] == "AUTOMATED_DECISION_FULLY"]["count"].sum()
        )
        any_num = int(
            sub[
                sub["automated_decision"].isin(
                    ["AUTOMATED_DECISION_FULLY", "AUTOMATED_DECISION_PARTIALLY"]
                )
            ]["count"].sum()
        )

        if sors > 0:
            det_rate = round(det_num / sors, 8)
            fully_rate = round(fully_num / sors, 8)
            any_rate = round(any_num / sors, 8)
        else:
            det_rate = np.nan
            fully_rate = np.nan
            any_rate = np.nan

        rows.append(
            {
                "platform": p,
                "category": c,
                "represented_sors": sors,
                "category_share": share,
                "sparse_flag": sparse,
                "automated_detection_numerator": det_num,
                "automated_detection_rate": det_rate,
                "fully_automated_decision_numerator": fully_num,
                "fully_automated_decision_rate": fully_rate,
                "any_automated_decision_numerator": any_num,
                "decision_with_any_automation_rate": any_rate,
            }
        )

    cat_df = pd.DataFrame(rows)
    cat_df.sort_values(by=["platform", "represented_sors"], ascending=[True, False], inplace=True)
    return cat_df


def build_automation_monthly(auto_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build monthly automation series (automation_monthly.csv) for 2025-07 through 2026-05.
    """
    rows = []
    months = sorted(auto_df["month"].unique())

    for m in months:
        mdf = auto_df[auto_df["month"] == m]
        for p in CORE_PLATFORMS:
            pmdf = mdf[mdf["platform_name"] == p]
            sors = int(pmdf["count"].sum())

            det_num = int(pmdf[pmdf["automated_detection"] == "Yes"]["count"].sum())
            fully_num = int(
                pmdf[pmdf["automated_decision"] == "AUTOMATED_DECISION_FULLY"]["count"].sum()
            )
            any_num = int(
                pmdf[
                    pmdf["automated_decision"].isin(
                        ["AUTOMATED_DECISION_FULLY", "AUTOMATED_DECISION_PARTIALLY"]
                    )
                ]["count"].sum()
            )

            det_rate = round(det_num / sors, 8) if sors > 0 else np.nan
            fully_rate = round(fully_num / sors, 8) if sors > 0 else np.nan
            any_rate = round(any_num / sors, 8) if sors > 0 else np.nan

            rows.append(
                {
                    "month": m,
                    "platform": p,
                    "represented_sors": sors,
                    "automated_detection_numerator": det_num,
                    "automated_detection_rate": det_rate,
                    "fully_automated_decision_numerator": fully_num,
                    "fully_automated_decision_rate": fully_rate,
                    "any_automated_decision_numerator": any_num,
                    "decision_with_any_automation_rate": any_rate,
                }
            )

    return pd.DataFrame(rows)


def build_automation_category_monthly(auto_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build monthly category-level automation matrix (automation_category_monthly.csv).
    """
    grouped = (
        auto_df.groupby(
            ["month", "platform_name", "category", "automated_detection", "automated_decision"],
            observed=False,
        )["count"]
        .sum()
        .reset_index()
    )

    months = sorted(auto_df["month"].unique())
    rows = []

    for m in months:
        mdf = grouped[grouped["month"] == m]
        for p in CORE_PLATFORMS:
            pmdf = mdf[mdf["platform_name"] == p]
            for c in CANONICAL_CATEGORIES:
                sub = pmdf[pmdf["category"] == c]
                sors = int(sub["count"].sum())

                if sors == 0:
                    continue  # Keep compact by emitting observed combinations

                det_num = int(sub[sub["automated_detection"] == "Yes"]["count"].sum())
                fully_num = int(
                    sub[sub["automated_decision"] == "AUTOMATED_DECISION_FULLY"]["count"].sum()
                )
                any_num = int(
                    sub[
                        sub["automated_decision"].isin(
                            ["AUTOMATED_DECISION_FULLY", "AUTOMATED_DECISION_PARTIALLY"]
                        )
                    ]["count"].sum()
                )

                rows.append(
                    {
                        "month": m,
                        "platform": p,
                        "category": c,
                        "represented_sors": sors,
                        "automated_detection_numerator": det_num,
                        "automated_detection_rate": round(det_num / sors, 8),
                        "fully_automated_decision_numerator": fully_num,
                        "fully_automated_decision_rate": round(fully_num / sors, 8),
                        "any_automated_decision_numerator": any_num,
                        "decision_with_any_automation_rate": round(any_num / sors, 8),
                    }
                )

    return pd.DataFrame(rows)


def build_enforcement_action_prevalence(
    enforce_df: pd.DataFrame, vol_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Build granular multi-label enforcement action prevalence table
    (enforcement_action_prevalence.csv).
    """
    enf_map = {
        (r["platform_name"], r["category"], r["action"]): r["action_numerator"]
        for _, r in enforce_df.iterrows()
    }

    rows = []
    for _, vrow in vol_df.iterrows():
        p = vrow["platform"]
        c = vrow["category"]
        sors = int(vrow["represented_sors"])
        share = vrow["category_share"]
        sparse = vrow["sparse_flag"]

        for act in ENFORCEMENT_ACTIONS:
            num = int(enf_map.get((p, c, act), 0))
            prev = round(num / sors, 8) if sors > 0 else np.nan

            rows.append(
                {
                    "platform": p,
                    "category": c,
                    "action": act,
                    "represented_sors": sors,
                    "action_numerator": num,
                    "action_prevalence": prev,
                    "category_share": share,
                    "sparse_flag": sparse,
                }
            )

    enf_table = pd.DataFrame(rows)
    enf_table.sort_values(
        by=["platform", "category", "action_numerator"],
        ascending=[True, True, False],
        inplace=True,
    )
    return enf_table


def build_enforcement_action_overall(
    enforce_df: pd.DataFrame, overall_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Build platform-wide overall enforcement prevalence table (enforcement_action_overall.csv).
    """
    tot_map = {r["platform"]: r["represented_sors"] for _, r in overall_df.iterrows()}

    act_overall = (
        enforce_df.groupby(["platform_name", "action"], observed=False)["action_numerator"]
        .sum()
        .reset_index()
    )
    act_map = {
        (r["platform_name"], r["action"]): r["action_numerator"]
        for _, r in act_overall.iterrows()
    }

    rows = []
    for p in CORE_PLATFORMS:
        tot_sors = int(tot_map[p])
        for act in ENFORCEMENT_ACTIONS:
            num = int(act_map.get((p, act), 0))
            prev = round(num / tot_sors, 8) if tot_sors > 0 else 0.0
            rows.append(
                {
                    "platform": p,
                    "action": act,
                    "represented_sors": tot_sors,
                    "action_numerator": num,
                    "action_prevalence": prev,
                }
            )

    enf_ov = pd.DataFrame(rows)
    enf_ov.sort_values(by=["platform", "action_numerator"], ascending=[True, False], inplace=True)
    return enf_ov


def build_platform_effect_sizes(overall_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build pairwise platform effect sizes table (platform_effect_sizes.csv)
    for Phase 6 candidate-finding selection.
    Reports percentage-point difference (rate_a - rate_b) * 100 and rate_ratio.
    """
    rates = {}
    for _, r in overall_df.iterrows():
        p = r["platform"]
        rates[p] = {
            "automated_detection_rate": r["automated_detection_rate"],
            "fully_automated_decision_rate": r["fully_automated_decision_rate"],
            "decision_with_any_automation_rate": r["decision_with_any_automation_rate"],
        }

    pairs = [
        ("TikTok", "YouTube"),
        ("TikTok", "Instagram"),
        ("YouTube", "Instagram"),
    ]

    metrics = [
        "automated_detection_rate",
        "fully_automated_decision_rate",
        "decision_with_any_automation_rate",
    ]

    rows = []
    for pa, pb in pairs:
        for m in metrics:
            ra = rates[pa][m]
            rb = rates[pb][m]
            pp_diff = round((ra - rb) * 100.0, 4)
            ratio = round(ra / rb, 4) if rb > 0 else np.nan

            rows.append(
                {
                    "platform_a": pa,
                    "platform_b": pb,
                    "metric": m,
                    "rate_a": ra,
                    "rate_b": rb,
                    "percentage_point_difference": pp_diff,
                    "rate_ratio": ratio,
                }
            )

    return pd.DataFrame(rows)


def validate_metrics(
    vol_df: pd.DataFrame,
    overall_df: pd.DataFrame,
    cat_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    enf_cat_df: pd.DataFrame,
    enf_ov_df: pd.DataFrame,
) -> Dict[str, bool]:
    """
    Run comprehensive data validation checks against Phase 4 invariants.
    """
    results = {}

    # A. Population Reconciliation
    tot_reconciled = True
    for p in CORE_PLATFORMS:
        obs_p = int(overall_df[overall_df["platform"] == p]["represented_sors"].iloc[0])
        exp_p = EXPECTED_POPULATION[p]
        if obs_p != exp_p:
            tot_reconciled = False
            print(f"Validation FAILED: Platform {p} SoRs {obs_p:,} != expected {exp_p:,}")

    tot_sors = int(overall_df["represented_sors"].sum())
    if tot_sors != EXPECTED_POPULATION["TOTAL"]:
        tot_reconciled = False
        print(f"Validation FAILED: Total SoRs {tot_sors:,} != expected {EXPECTED_POPULATION['TOTAL']:,}")
    results["population_reconciliation"] = tot_reconciled

    # B. Category Additivity
    cat_additivity = True
    for p in CORE_PLATFORMS:
        p_vol = vol_df[vol_df["platform"] == p]
        sum_cat_sors = int(p_vol["represented_sors"].sum())
        exp_sors = EXPECTED_POPULATION[p]
        if sum_cat_sors != exp_sors:
            cat_additivity = False
            print(f"Validation FAILED: Category sum for {p} {sum_cat_sors:,} != {exp_sors:,}")
        sum_shares = float(p_vol["category_share"].sum())
        if abs(sum_shares - 1.0) > 1e-4:
            cat_additivity = False
            print(f"Validation FAILED: Category shares for {p} sum to {sum_shares} != 1.0")
    results["category_additivity"] = cat_additivity

    # C. Automation Numerators & Rate Bounds
    auto_bounds = True
    for df_to_check in [overall_df, cat_df, monthly_df]:
        for prefix in ["automated_detection", "fully_automated_decision", "any_automated_decision"]:
            num_col = f"{prefix}_numerator"
            if prefix == "any_automated_decision":
                rate_col = "decision_with_any_automation_rate"
            else:
                rate_col = f"{prefix}_rate"

            valid_rows = df_to_check[df_to_check["represented_sors"] > 0]
            if (valid_rows[num_col] < 0).any() or (
                valid_rows[num_col] > valid_rows["represented_sors"]
            ).any():
                auto_bounds = False
                print(f"Validation FAILED: Numerator out of bounds for {num_col}")

            non_null_rates = valid_rows[rate_col].dropna()
            if (non_null_rates < 0.0).any() or (non_null_rates > 1.0).any():
                auto_bounds = False
                print(f"Validation FAILED: Rate out of bounds [0, 1] for {rate_col}")
    results["automation_bounds"] = auto_bounds

    # D. Monthly Reconciliation
    monthly_reconciled = True
    for p in CORE_PLATFORMS:
        m_sum = int(monthly_df[monthly_df["platform"] == p]["represented_sors"].sum())
        exp_p = EXPECTED_POPULATION[p]
        if m_sum != exp_p:
            monthly_reconciled = False
            print(f"Validation FAILED: Monthly sum for {p} {m_sum:,} != expected {exp_p:,}")
    results["monthly_reconciliation"] = monthly_reconciled

    # E. Enforcement Bounds
    enf_bounds = True
    for enf_check in [enf_ov_df, enf_cat_df]:
        valid_rows = enf_check[enf_check["represented_sors"] > 0]
        if (valid_rows["action_numerator"] < 0).any() or (
            valid_rows["action_numerator"] > valid_rows["represented_sors"]
        ).any():
            enf_bounds = False
            print("Validation FAILED: Enforcement numerator out of bounds")

        non_null_prev = valid_rows["action_prevalence"].dropna()
        if (non_null_prev < 0.0).any() or (non_null_prev > 1.0).any():
            enf_bounds = False
            print("Validation FAILED: Action prevalence out of bounds [0, 1]")
    results["enforcement_bounds"] = enf_bounds

    return results


def run_pipeline(dsa_path: Path = DEFAULT_DSA_PATH, output_dir: Path = PROCESSED_DIR) -> None:
    """
    Run the complete Phase 5 metrics pipeline and output processed CSV files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    print("Step 1: Aggregating monthly batches from raw DSA dataset...")
    auto_df, enforce_df = aggregate_batches(dsa_path=dsa_path)

    print("Step 2: Building analytical tables...")
    vol_df = build_category_volume(auto_df)
    overall_df = build_automation_overall(auto_df)
    cat_df = build_automation_by_category(auto_df, vol_df)
    monthly_df = build_automation_monthly(auto_df)
    cat_monthly_df = build_automation_category_monthly(auto_df)
    enf_cat_df = build_enforcement_action_prevalence(enforce_df, vol_df)
    enf_ov_df = build_enforcement_action_overall(enforce_df, overall_df)
    effects_df = build_platform_effect_sizes(overall_df)

    print("Step 3: Validating metrics against Phase 4 invariants...")
    val_results = validate_metrics(
        vol_df=vol_df,
        overall_df=overall_df,
        cat_df=cat_df,
        monthly_df=monthly_df,
        enf_cat_df=enf_cat_df,
        enf_ov_df=enf_ov_df,
    )

    all_passed = all(val_results.values())
    if not all_passed:
        raise RuntimeError(f"Pipeline validation failed: {val_results}")
    print("  ALL VALIDATION CHECKS PASSED.")

    print("Step 4: Writing processed outputs...")
    vol_path = output_dir / "category_volume.csv"
    vol_df.to_csv(vol_path, index=False)
    print(f"  - {vol_path.name} ({len(vol_df)} rows)")

    overall_path = output_dir / "automation_overall.csv"
    overall_df.to_csv(overall_path, index=False)
    print(f"  - {overall_path.name} ({len(overall_df)} rows)")

    cat_path = output_dir / "automation_by_category.csv"
    cat_df.to_csv(cat_path, index=False)
    print(f"  - {cat_path.name} ({len(cat_df)} rows)")

    monthly_path = output_dir / "automation_monthly.csv"
    monthly_df.to_csv(monthly_path, index=False)
    print(f"  - {monthly_path.name} ({len(monthly_df)} rows)")

    cat_monthly_path = output_dir / "automation_category_monthly.csv"
    cat_monthly_df.to_csv(cat_monthly_path, index=False)
    print(f"  - {cat_monthly_path.name} ({len(cat_monthly_df)} rows)")

    enf_cat_path = output_dir / "enforcement_action_prevalence.csv"
    enf_cat_df.to_csv(enf_cat_path, index=False)
    print(f"  - {enf_cat_path.name} ({len(enf_cat_df)} rows)")

    enf_ov_path = output_dir / "enforcement_action_overall.csv"
    enf_ov_df.to_csv(enf_ov_path, index=False)
    print(f"  - {enf_ov_path.name} ({len(enf_ov_df)} rows)")

    effects_path = output_dir / "platform_effect_sizes.csv"
    effects_df.to_csv(effects_path, index=False)
    print(f"  - {effects_path.name} ({len(effects_df)} rows)")

    print("\nPhase 5 pipeline execution complete.")


if __name__ == "__main__":
    run_pipeline()
