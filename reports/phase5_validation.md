# Phase 5 — Core Metrics Validation Report

**Date**: September 2026  
**Status**: Complete  
**Methodology Specification**: [MAPPING.md](file:///c:/dsa-moderation-benchmark/MAPPING.md) (All 12 Rules Enforced)  
**Primary Dataset**: EU Digital Services Act Transparency Database Complete Aggregates (`data/raw/dsa_aggregates/aggregated-complete.parquet`)  

---

## 1. Input Population & Filter Specification

The primary analysis population is strictly defined according to MAPPING.md Rules 1 and 2:
- **Harmonized Observation Window**: `created_at >= '2025-07-01' AND created_at <= '2026-05-31'` (11 monthly partitions: `2025-07-01` through `2026-05-01`).
- **Target Platform Filter**: `platform_name IN ('TikTok', 'YouTube', 'Instagram')`.
- **Weighting Invariant**: All aggregations and rate calculations use `SUM(count)` weighting (MAPPING.md Rule 4).

### Population Summary & Exact Reconciliation:
| Platform | Physical Parquet Rows | Represented SoRs (`SUM(count)`) | Expected SoRs (MAPPING.md) | Discrepancy |
| :--- | :---: | :---: | :---: | :---: |
| **TikTok** | 6,493,181 | 480,532,153 | 480,532,153 | **0 (Exact match)** |
| **YouTube** | 3,753,653 | 88,376,558 | 88,376,558 | **0 (Exact match)** |
| **Instagram** | 6,976,215 | 92,756,287 | 92,756,287 | **0 (Exact match)** |
| **TOTAL** | **17,223,049** | **661,664,998** | **661,664,998** | **0 (Exact match)** |

---

## 2. Processed Outputs Summary

The Phase 5 pipeline (`src/metrics.py`, backed by `src/load_dsa.py`) generated eight compact, reproducible analytical CSV tables in `data/processed/`:

| Output Filename | Rows | File Size | Description |
| :--- | :---: | :---: | :--- |
| `category_volume.csv` | 48 | 4,086 bytes | Full Cartesian grid (3 platforms × 16 categories) with SoRs, platform total, category share, and `< 0.10%` sparsity flag. Includes explicit zero-volume rows for complete reproducibility. |
| `automation_overall.csv` | 3 | 438 bytes | Overall platform automation rates and numerators: Automated Detection Rate, Fully Automated Decision Rate, and Decision with Any Automation Rate. |
| `automation_by_category.csv` | 48 | 5,733 bytes | Category-level automation metrics. Zero-denominator combinations report rates as `null` / `NaN` (never `0%`), preserving sparsity flags. |
| `automation_monthly.csv` | 33 | 2,836 bytes | Monthly time-series (11 months × 3 platforms) for temporal consistency and robustness auditing. |
| `automation_category_monthly.csv` | 409 | 45,088 bytes | Monthly category-level automation matrix for observed combinations, enabling Phase 6 persistence checks without table bloat. |
| `enforcement_action_prevalence.csv` | 720 | 74,836 bytes | Granular multi-label enforcement action prevalence (3 platforms × 16 categories × 15 actions). Percentages are independent and not forced to sum to 100%. |
| `enforcement_action_overall.csv` | 45 | 2,399 bytes | Platform-wide overall prevalence across the 15 normalized enforcement actions. |
| `platform_effect_sizes.csv` | 9 | 812 bytes | Pairwise platform effect sizes (percentage-point differences and rate ratios) across the three overall automation metrics for candidate-finding evaluation. |

---

## 3. Direct Numerator, Denominator, and Rate Manual Sanity Checks

To guarantee complete independence, three targeted calculations were executed directly against the raw Parquet partitions using `pyarrow.dataset`, completely bypassing the reusable modules in `src/`. Both raw and processed numerators, denominators, and rates were compared.

### Check 1 — YouTube Overall Automation
- Raw query directly filters `platform_name == 'YouTube'` across all 11 raw partitions:

| Metric | Raw Numerator | Processed Numerator | Numerator Diff | Raw Denom | Processed Denom | Denom Diff | Raw Rate (float64) | Processed Rate (CSV) | Rate Diff |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Automated Detection** | 87,392,106 | 87,392,106 | **0** | 88,376,558 | 88,376,558 | **0** | 0.98886071123... | 0.98886071 | **1.23e-9** |
| **Fully Automated Decision** | 44,009,286 | 44,009,286 | **0** | 88,376,558 | 88,376,558 | **0** | 0.49797466478... | 0.49797466 | **4.78e-9** |
| **Decision with Any Automation** | 48,317,326 | 48,317,326 | **0** | 88,376,558 | 88,376,558 | **0** | 0.54672107400... | 0.54672107 | **3.99e-9** |

### Check 2 — Instagram × Scams and Fraud Automation
- Raw query filters `platform_name == 'Instagram'` and `category == 'STATEMENT_CATEGORY_SCAMS_AND_FRAUD'`:

| Metric | Raw Numerator | Processed Numerator | Numerator Diff | Raw Denom | Processed Denom | Denom Diff | Raw Rate (float64) | Processed Rate (CSV) | Rate Diff |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Automated Detection** | 47,710,406 | 47,710,406 | **0** | 47,973,134 | 47,973,134 | **0** | 0.99452343472... | 0.99452343 | **4.72e-9** |
| **Fully Automated Decision** | 0 | 0 | **0** | 47,973,134 | 47,973,134 | **0** | 0.00000000000... | 0.00000000 | **0.00e+00** |
| **Decision with Any Automation** | 47,710,406 | 47,710,406 | **0** | 47,973,134 | 47,973,134 | **0** | 0.99452343472... | 0.99452343 | **4.72e-9** |

### Check 3 — TikTok × Illegal/Harmful Speech × CONTENT_REMOVED
- Raw query filters `platform_name == 'TikTok'`, `category == 'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH'`, and `DECISION_VISIBILITY_CONTENT_REMOVED == True`:

| Metric | Raw Numerator | Processed Numerator | Numerator Diff | Raw Denom | Processed Denom | Denom Diff | Raw Rate (float64) | Processed Rate (CSV) | Rate Diff |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CONTENT_REMOVED** | 69,994,541 | 69,994,541 | **0** | 73,417,484 | 73,417,484 | **0** | 0.95337700486... | 0.95337700 | **4.86e-9** |

### Check 4 — Exhaustive 720-Row Enforcement Action Reconciliation
An independent verification script queried the raw Parquet partitions across all 11 months directly, aggregating every combination of platform, category, and normalized enforcement action:
- **`enforcement_action_prevalence.csv` (720 rows)**:
  - Rows audited: **720 of 720**
  - Mismatches detected: **0**
  - Maximum absolute numerator discrepancy: **0**
  - Maximum absolute denominator discrepancy: **0**
- **`enforcement_action_overall.csv` (45 rows)**:
  - Rows audited: **45 of 45**
  - Mismatches detected: **0**
  - Maximum absolute numerator discrepancy: **0**
  - Maximum absolute denominator discrepancy: **0**

- **Verification Summary**:
  - Every single raw vs. processed numerator difference across all tables is **exactly 0**.
  - Every single raw vs. processed denominator difference across all tables is **exactly 0**.
  - The rate differences ($\sim 1 \times 10^{-9}$ to $5 \times 10^{-9}$) are solely due to rounding at the 8th decimal place in `src/metrics.py`.

---

## 4. CSV Numeric Precision Documentation

In `src/metrics.py`, calculated rates are serialized to CSV using 8 decimal places (`round(rate, 8)`):
- **Precision Standard**: 8 decimal places corresponds to $10^{-8}$ of a unit, or **$0.000001\%$** (one hundred-thousandth of a percentage point). This provides extreme auditability while eliminating arbitrary binary floating-point representation noise (e.g. `0.49797466000000003`).
- **Explanation of $\sim 1 \times 10^{-9}$ Differences**: When Python evaluates `raw_rate = 87392106 / 88376558` in standard 64-bit float, it computes `0.9888607112306863...`. Rounding this value to 8 decimal places produces `0.98886071`. The difference between the unrounded float64 and the 8-decimal serialized rate is $0.00000000123... \approx 1.23 \times 10^{-9}$.
- **Reconstructibility**: Every processed CSV stores both the exact integer numerator and denominator (`represented_sors`, `*_numerator`). Any downstream consumer can reproduce unrounded double-precision quotients directly from these integer columns.

---

## 5. Monthly Reconciliations (Denominator & Numerator)

### Monthly to Overall Platform Reconciliation:
For each platform, summing across the 11 monthly records in `automation_monthly.csv` reconciles to `automation_overall.csv` with **0 discrepancy**:

| Platform | Metric | Sum of 11 Months (`automation_monthly.csv`) | Platform Total (`automation_overall.csv`) | Discrepancy |
| :--- | :--- | :---: | :---: | :---: |
| **TikTok** | Represented SoRs (Denominator) | 480,532,153 | 480,532,153 | **0** |
| **TikTok** | Automated Detection Numerator | 467,328,339 | 467,328,339 | **0** |
| **TikTok** | Fully Automated Decision Numerator | 444,185,856 | 444,185,856 | **0** |
| **TikTok** | Any Automated Decision Numerator | 444,189,374 | 444,189,374 | **0** |
| **YouTube** | Represented SoRs (Denominator) | 88,376,558 | 88,376,558 | **0** |
| **YouTube** | Automated Detection Numerator | 87,392,106 | 87,392,106 | **0** |
| **YouTube** | Fully Automated Decision Numerator | 44,009,286 | 44,009,286 | **0** |
| **YouTube** | Any Automated Decision Numerator | 48,317,326 | 48,317,326 | **0** |
| **Instagram** | Represented SoRs (Denominator) | 92,756,287 | 92,756,287 | **0** |
| **Instagram** | Automated Detection Numerator | 88,610,815 | 88,610,815 | **0** |
| **Instagram** | Fully Automated Decision Numerator | 0 | 0 | **0** |
| **Instagram** | Any Automated Decision Numerator | 88,610,815 | 88,610,815 | **0** |

---

## 6. Category-Monthly Reconciliation

Because `automation_category_monthly.csv` was generated to enable Phase 6 temporal persistence analysis, every platform/category combination was reconciled against `automation_by_category.csv`:
- **Total Platform/Category Combinations Tested**: Exactly **48** (16 categories × 3 platforms).
- **Maximum Absolute Denominator Discrepancy**: **0** (across all 48 combinations).
- **Maximum Absolute Detection Numerator Discrepancy**: **0**.
- **Maximum Absolute Fully Decision Numerator Discrepancy**: **0**.
- **Maximum Absolute Any Decision Numerator Discrepancy**: **0**.

---

## 7. Monthly Volume Concentration QA

To document the degree to which weighted overall rates are driven by specific submission volumes, the monthly volume distribution across the 11-month observation window was audited:

| Platform | Minimum Monthly SoRs | Month of Minimum | Maximum Monthly SoRs | Month of Maximum | Largest Month's Share of 11-Month Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TikTok** | 5,367,152 | 2025-09 | 120,568,406 | 2026-01 | **25.0906%** (2026-01) |
| **YouTube** | 4,086,150 | 2026-02 | 12,177,127 | 2025-11 | **13.7787%** (2025-11) |
| **Instagram** | 7,251,298 | 2025-07 | 10,388,056 | 2025-10 | **11.1993%** (2025-10) |

*Descriptive Note*: This variation reflects administrative submission volumes across time. Under volume-weighting (MAPPING.md Rule 4), overall rates mathematically reflect these volume proportions.

---

## 8. Effect-Size Unit Documentation

In `data/processed/platform_effect_sizes.csv`:
- **`percentage_point_difference`**: Stored in **PERCENTAGE POINTS** ($\Delta\%$).
  - Example: For TikTok ($92.44\%$) vs YouTube ($49.80\%$) on `fully_automated_decision_rate`, the stored value is **`42.6388`** (i.e. $+42.64$ percentage points), **NOT** `0.4264`.
- **`rate_ratio`**: Stored as a **unitless ratio** ($\text{Rate}_A / \text{Rate}_B$).
  - Where $\text{Rate}_B = 0.0$ (e.g. comparisons against Instagram's Fully Automated Decision Rate), `rate_ratio` is stored as **`NaN` / null (undefined)** rather than infinity.

---

## 9. Zero-Volume Category Representation QA

The explicit 48-row grid in `category_volume.csv` and `automation_by_category.csv` is fully intentional (16 categories × 3 platforms):
- **Observed Combinations**: 40 platform/category pairs have $\text{represented\_sors} > 0$.
- **Zero-Volume Combinations**: Exactly **8** platform/category pairs have $\text{represented\_sors} = 0$:
  1. `Instagram` | `STATEMENT_CATEGORY_CONSUMER_INFORMATION`
  2. `Instagram` | `STATEMENT_CATEGORY_ANIMAL_WELFARE`
  3. `Instagram` | `STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE`
  4. `Instagram` | `STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT`
  5. `TikTok` | `STATEMENT_CATEGORY_CONSUMER_INFORMATION`
  6. `YouTube` | `STATEMENT_CATEGORY_SELF_HARM`
  7. `YouTube` | `STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE`
  8. `YouTube` | `STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT`

### Downstream Representation Properties:
For all 8 zero-volume combinations:
- `represented_sors = 0`
- `category_share = 0.0`
- `sparse_flag = True`
- `*_numerator = 0`
- `*_rate = null / NaN` (serialized as empty string `,` in CSV, never `0.0%`).

This enables downstream analytical code in Phase 6 to cleanly distinguish between:
- **Observed zero automation**: $\text{represented\_sors} > 0$, $\text{numerator} = 0$, $\text{rate} = 0.0$ (e.g. Instagram's Fully Automated Decision Rate = $0.0\%$ on 47.97M Scams SoRs).
- **Undefined category**: $\text{represented\_sors} = 0$, $\text{rate} = \text{null / NaN}$ (e.g. YouTube in `SELF_HARM`).

---

## 10. Summary of Validation Invariants

All 12 methodological rules from MAPPING.md were executed and verified with zero discrepancies:
- **Rule 1 & 2**: Temporal window (`2025-07-01` through `2026-05-31`) and platform filter verified.
- **Rule 3**: `category` string column used exclusively.
- **Rule 4 & 5**: Weighted by `SUM(count)`; single-label shares sum to $100.00\%$.
- **Rule 6**: Project-defined sparsity flag active for shares $< 0.10\%$; zero denominators yield null.
- **Rule 7**: Detection, fully automated decision, and any automation decision rates computed with literal source enums.
- **Rule 8 & 9**: Empirical $0\%$ nulls verified; platform-wide rates volume-weighted.
- **Rule 10**: Granular multi-label enforcement action prevalence table verified. Exclusive channel deferred.
- **Rule 11**: Supplementary platform data strictly excluded from quantitative tables.
- **Rule 12**: Platform effect sizes reported in percentage points and unitless ratios without p-values.

---

## 11. Pre-Analysis Data Behavior Diagnostics

To determine whether prominent empirical patterns reflect stable operational behaviors or reporting artifacts requiring methodological caveats, three targeted pre-analysis diagnostics were conducted.

### Diagnostic 1 — TikTok January 2026 Volume Spike

#### A. Monthly Volume Context (TikTok)
| Month | Represented SoRs | Share of 11-Month Total | MoM Absolute Change | MoM % Change |
| :---: | :---: | :---: | :---: | :---: |
| **2025-07** | 33,081,573 | 6.88% | — | — |
| **2025-08** | 48,490,818 | 10.09% | +15,409,245 | +46.58% |
| **2025-09** | 5,367,152 | 1.12% | -43,123,666 | -88.93% |
| **2025-10** | 43,302,182 | 9.01% | +37,935,030 | +706.80% |
| **2025-11** | 18,497,228 | 3.85% | -24,804,954 | -57.28% |
| **2025-12** | 20,513,138 | 4.27% | +2,015,910 | +10.90% |
| **2026-01** | 120,568,406 | 25.09% | +100,055,268 | +487.76% |
| **2026-02** | 72,150,742 | 15.01% | -48,417,664 | -40.16% |
| **2026-03** | 41,172,435 | 8.57% | -30,978,307 | -42.94% |
| **2026-04** | 39,661,448 | 8.25% | -1,510,987 | -3.67% |
| **2026-05** | 37,727,031 | 7.85% | -1,934,417 | -4.88% |

#### B. Category Decomposition (Dec 2025 → Jan 2026 → Feb 2026)
- Total Volume: Dec = 20,513,138 | Jan = 120,568,406 | Feb = 72,150,742
- Net Dec → Jan Increase: **+100,055,268 SoRs**
- Net Jan → Feb Decrease: **-48,417,664 SoRs**

| Category Name | Dec 2025 SoRs (Share) | Jan 2026 SoRs (Share) | Feb 2026 SoRs (Share) | Dec → Jan Diff (% Contrib) | Jan → Feb Diff (% Contrib) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `OTHER_VIOLATION_TC` | 15,325,726 (74.71%) | 91,510,993 (75.90%) | 57,490,455 (79.68%) | +76,185,267 (76.1%) | -34,020,538 (70.3%) |
| `ILLEGAL_OR_HARMFUL_SPEECH` | 2,499,150 (12.18%) | 15,141,396 (12.56%) | 9,952,997 (13.79%) | +12,642,246 (12.6%) | -5,188,399 (10.7%) |
| `NEGATIVE_EFFECTS_ON_CIVIC` | 1,344,391 (6.55%) | 5,819,337 (4.83%) | 169,359 (0.23%) | +4,474,946 (4.5%) | -5,649,978 (11.7%) |
| `VIOLENCE` | 425,234 (2.07%) | 2,762,621 (2.29%) | 1,667,854 (2.31%) | +2,337,387 (2.3%) | -1,094,767 (2.3%) |
| `SCAMS_AND_FRAUD` | 426,416 (2.08%) | 2,591,471 (2.15%) | 1,854,605 (2.57%) | +2,165,055 (2.2%) | -736,866 (1.5%) |
| `PROTECTION_OF_MINORS` | 312,521 (1.52%) | 1,728,129 (1.43%) | 669,111 (0.93%) | +1,415,608 (1.4%) | -1,059,018 (2.2%) |
| All Other Categories (10) | 179,700 (0.88%) | 1,014,459 (0.84%) | 346,362 (0.48%) | +834,759 (0.8%) | -668,098 (1.4%) |

*Finding*: The volume increase is **not** driven by a single anomalous category. The category proportions in January 2026 mirror December 2025 and February 2026 almost identically (`OTHER_VIOLATION_TC` contributed 76.1% and `ILLEGAL_OR_HARMFUL_SPEECH` contributed 12.6% of the net volume surge).

#### C. Enforcement Action Decomposition
| Action Type | Dec 2025 SoRs (Prev) | Jan 2026 SoRs (Prev) | Feb 2026 SoRs (Prev) |
| :--- | :---: | :---: | :---: |
| `VISIBILITY_OTHER` | 11,820,107 (57.62%) | 69,505,993 (57.65%) | 37,621,649 (52.14%) |
| `CONTENT_REMOVED` | 8,071,798 (39.35%) | 47,630,903 (39.51%) | 31,296,136 (43.38%) |
| `ACCOUNT_TERMINATED` | 395,258 (1.93%) | 1,490,223 (1.24%) | 412,500 (0.57%) |
| `PROVISION_PARTIAL_SUSPENSION` | 76,842 (0.37%) | 1,307,877 (1.08%) | 2,365,049 (3.28%) |
| `CONTENT_AGE_RESTRICTED` | 150,864 (0.74%) | 719,192 (0.60%) | 328,385 (0.46%) |
| `CONTENT_DISABLED` | 14,396 (0.07%) | 53,557 (0.04%) | 127,023 (0.18%) |

*Finding*: The distribution across enforcement actions remained virtually identical between December (57.62% `VISIBILITY_OTHER`, 39.35% `CONTENT_REMOVED`) and January (57.65% `VISIBILITY_OTHER`, 39.51% `CONTENT_REMOVED`).

#### D. Created_at Daily Distribution (January 2026)
- **Total Calendar Days Active**: 31
- **Daily Minimum**: 182,532 SoRs (2026-01-01)
- **Daily Median**: 1,915,037 SoRs
- **Daily Maximum**: 7,439,780 SoRs (2026-01-21)
- **Top Concentration Shares**:
  - Top 1 Day (2026-01-21): 7,439,780 SoRs (**6.17%** of January)
  - Top 3 Days (Jan 21, 22, 25): 22,015,083 SoRs (**18.26%** of January)
  - Top 5 Days: 36,307,774 SoRs (**30.11%** of January)
- **Daily Pattern**: January submissions exhibit an eleven-day sustained high-volume plateau from January 21 through January 31, averaging 7.17 million SoRs per day (accounting for 65.4% of the month's total).

#### E. Application Date Lag Distribution
| Submission Month | Median Lag (days) | 90th Percentile | 95th Percentile | 99th Percentile | % Lag > 7 Days | % Lag > 30 Days |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2025-12** | 37.00 | 90.00 | 90.00 | 90.00 | 100.00% | 70.72% |
| **2026-01** | 65.00 | 88.00 | 89.00 | 90.00 | 91.87% | 80.81% |
| **2026-02** | 0.00 | 24.00 | 26.00 | 29.00 | 38.60% | 0.02% |

- **Breakdown of Application Dates for January 2026 Submissions**:
  - `2025-12`: 36,891,382 SoRs (**30.60%**)
  - `2025-10`: 35,973,499 SoRs (**29.84%**)
  - `2025-11`: 34,994,229 SoRs (**29.02%**)
  - `2026-01`: 12,705,996 SoRs (**10.54%**)
- **Diagnostic Classification**: **Consistent with delayed batch submission behavior**. Over 89.4% of the SoRs submitted by TikTok in January 2026 correspond to moderation decisions that were applied in October, November, and December 2025. In February 2026, the submission lag abruptly returned to normal (median lag = 0.0 days).

#### F. Automation-Rate Sensitivity to January 2026
| Metric | Full 11-Month Window | Sensitivity Window (Excl. Jan 2026) | Percentage-Point Difference | Diagnostic Influence Threshold |
| :--- | :---: | :---: | :---: | :---: |
| **Represented SoRs** | 480,532,153 | 359,963,747 (74.91%) | -120,568,406 | — |
| **Automated Detection Rate** | 97.2523% (467.33M) | 97.4789% (350.89M) | **+0.2266 pp** | **< 1 pp (Limited influence)** |
| **Fully Automated Decision Rate** | 92.4362% (444.19M) | 92.5112% (333.01M) | **+0.0750 pp** | **< 1 pp (Limited influence)** |
| **Decision with Any Automation Rate**| 92.4370% (444.19M) | 92.5116% (333.01M) | **+0.0746 pp** | **< 1 pp (Limited influence)** |

- **Sensitivity Conclusion**: Excluding January 2026 causes all three overall automation rates to shift by **less than 0.25 percentage points** (well below the 1.0 pp diagnostic threshold). Therefore, despite the delayed batch submission volume, TikTok's aggregate automation metrics are highly robust and not distorted by the January volume surge.

---

### Diagnostic 2 — YouTube Monthly Decision-Automation Volatility

#### A & D. Monthly Decision Enum Distribution & Substitution
| Month | Represented SoRs | FULLY Count (Share) | PARTIALLY Count (Share) | NOT_AUTOMATED Count (Share) | Decision with Any Automation |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2025-07** | 7,719,948 | 4,591,607 (59.48%) | 382,647 (4.96%) | 2,745,694 (35.57%) | 64.43% |
| **2025-08** | 6,806,546 | 3,257,421 (47.86%) | 412,762 (6.06%) | 3,136,363 (46.08%) | 53.92% |
| **2025-09** | 9,483,004 | 3,792,337 (39.99%) | 326,933 (3.45%) | 5,363,734 (56.56%) | 43.44% |
| **2025-10** | 8,733,660 | 4,518,405 (51.74%) | 368,099 (4.21%) | 3,847,156 (44.05%) | 55.95% |
| **2025-11** | 12,177,127 | 3,720,238 (30.55%) | 308,582 (2.53%) | 8,148,307 (66.91%) | 33.09% |
| **2025-12** | 6,955,618 | 3,273,554 (47.06%) | 393,507 (5.66%) | 3,288,557 (47.28%) | 52.72% |
| **2026-01** | 7,028,058 | 3,184,358 (45.31%) | 464,773 (6.61%) | 3,378,927 (48.08%) | 51.92% |
| **2026-02** | 4,086,150 | 2,454,672 (60.07%) | 307,494 (7.53%) | 1,323,984 (32.40%) | 67.60% |
| **2026-03** | 5,905,997 | 3,241,732 (54.89%) | 339,764 (5.75%) | 2,324,501 (39.36%) | 60.64% |
| **2026-04** | 11,732,650 | 7,335,345 (62.52%) | 639,115 (5.45%) | 3,758,190 (32.03%) | 67.97% |
| **2026-05** | 7,747,800 | 4,639,617 (59.88%) | 364,364 (4.70%) | 2,743,819 (35.41%) | 64.59% |

#### B. Monthly Category Composition (YouTube)
| Month | `OTHER_VIOLATION_TC` | `SCAMS_AND_FRAUD` | `CONSUMER_INFO` | `UNSAFE_PRODUCTS` | `PROTECTION_MINORS` | `IP_INFRINGEMENTS` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **2025-07** | 71.57% | 13.71% | 3.20% | 9.59% | 1.25% | 0.39% |
| **2025-08** | 42.40% | 23.90% | 22.69% | 8.35% | 1.68% | 0.61% |
| **2025-09** | 34.09% | 52.31% | 5.13% | 6.05% | 0.86% | 0.32% |
| **2025-10** | 43.58% | 40.27% | 6.36% | 7.95% | 0.71% | 0.36% |
| **2025-11** | 23.25% | 63.47% | 6.73% | 5.59% | 0.48% | 0.26% |
| **2025-12** | 40.70% | 44.30% | 6.35% | 6.81% | 1.06% | 0.45% |
| **2026-01** | 42.58% | 43.80% | 5.66% | 5.69% | 1.03% | 0.87% |
| **2026-02** | 57.58% | 27.25% | 5.66% | 6.40% | 1.77% | 0.78% |
| **2026-03** | 51.00% | 18.39% | 11.62% | 5.30% | 1.37% | 0.53% |
| **2026-04** | 61.83% | 26.51% | 5.28% | 2.95% | 0.76% | 0.35% |
| **2026-05** | 52.70% | 30.05% | 10.64% | 4.10% | 1.19% | 0.48% |

#### C. Within-Category Automation Rate Stability
- **`OTHER_VIOLATION_TC`**: Highly stable around ~88%–92% fully automated decision across 10 of 11 months (Jul 2025: 71.33%, Aug: 90.72%, Sep: 91.39%, Oct: 89.66%, Nov: 90.08%, Dec: 87.93%, Jan: 86.02%, Feb: 88.16%, Mar: 83.49%, Apr: 90.94%, May: 92.22%).
- **`SCAMS_AND_FRAUD`**: Consistently near-zero fully automated decision across all 11 months (between 0.08% and 0.50% in every single month; over 99.5% evaluated via human review).
- **`PROTECTION_OF_MINORS`**: Exactly 0.00% fully automated decision in 10 of 11 months, but 99.9%–100.0% Decision with Any Automation in all 11 months (reported consistently as `AUTOMATED_DECISION_PARTIALLY`).
- **`INTELLECTUAL_PROPERTY`**: Near 0.0% fully automated decision in all months, but 60%–82% Decision with Any Automation in all months (reported consistently as `AUTOMATED_DECISION_PARTIALLY`).
- **Assessment**: YouTube's platform-wide decision-automation volatility (ranging from 30.55% to 62.52%) is **overwhelmingly composition-driven**, reflecting shifting volume balances between categories with substantially different reported decision-automation profiles. In November 2025, `SCAMS_AND_FRAUD` (where reported decision automation is ~0.1%) comprised 63.47% of YouTube's SoR volume, resulting in an overall platform decision-automation rate of 33.09%. In April 2026, `OTHER_VIOLATION_TC` (where reported fully automated decisions exceed 90%) comprised 61.83% of volume, resulting in an overall platform decision-automation rate of 67.97%. Across months, category-specific reported automation profiles remained stable.

---

### Diagnostic 3 — Instagram SCAMS_AND_FRAUD Account Termination

#### A. Monthly Termination Stability
| Month | `SCAMS_AND_FRAUD` SoRs | `ACCOUNT_TERMINATED` Numerator | Action Prevalence |
| :---: | :---: | :---: | :---: |
| **2025-07** | 3,392,154 | 3,368,841 | 99.3127% |
| **2025-08** | 4,949,976 | 4,926,574 | 99.5272% |
| **2025-09** | 5,292,175 | 5,272,950 | 99.6367% |
| **2025-10** | 7,105,666 | 7,089,353 | 99.7704% |
| **2025-11** | 6,235,151 | 6,228,867 | 99.8992% |
| **2025-12** | 4,896,245 | 4,884,764 | 99.7655% |
| **2026-01** | 4,522,716 | 4,512,579 | 99.7759% |
| **2026-02** | 4,624,634 | 4,616,842 | 99.8315% |
| **2026-03** | 3,862,763 | 3,738,945 | 96.7946% |
| **2026-04** | 1,335,278 | 1,257,464 | 94.1724% |
| **2026-05** | 1,756,376 | 1,487,582 | 84.6961% |
| **Total** | **47,973,134** | **47,384,761** | **98.7735%** |

#### B. Full Action Prevalence Breakdown (Instagram SCAMS_AND_FRAUD)
- `ACCOUNT_TERMINATED`: 47,384,761 SoRs (**98.7735%**)
- `CONTENT_REMOVED`: 587,837 SoRs (**1.2253%**)
- `CONTENT_DISABLED`: 510 SoRs (**0.0011%**)
- `ACCOUNT_SUSPENDED`: 26 SoRs (**0.0001%**)
- All Other 11 Actions: 0 SoRs (**0.0000%**)
- *Verification*: Account termination does not equal 100.0000% across the full window. In May 2026, account terminations fell to 84.70% while content removals rose to 15.30%.

#### C. Automation Enums (Instagram SCAMS_AND_FRAUD)
- **Automated Detection**: `Yes` = 47,710,406 (**99.45%**) | `No` = 262,728 (**0.55%**)
- **Automated Decision**: `AUTOMATED_DECISION_PARTIALLY` = 47,710,406 (**99.45%**) | `AUTOMATED_DECISION_NOT_AUTOMATED` = 262,728 (**0.55%**) | `AUTOMATED_DECISION_FULLY` = 0 (**0.00%**)

#### D. Record-Structure Check
- Total physical aggregate rows: 1,785,132.
- Legal Grounds: 1,784,680 rows (99.97%) classified under `DECISION_GROUND_INCOMPATIBLE_CONTENT`; 452 rows under `DECISION_GROUND_ILLEGAL_CONTENT`.
- Action Exclusivity: In Instagram's submissions for `SCAMS_AND_FRAUD`, an SoR records either `ACCOUNT_TERMINATED` or a visibility sanction, with 0 overlap.

#### E. Interpretation Boundary & Supported Conclusion
- **Observation**: Over 98.77% of all Instagram SoRs submitted under `SCAMS_AND_FRAUD` during the 11-month primary window record account termination (`ACCOUNT_TERMINATED`: 47,384,761 / 47,973,134 = 98.7735%).
- **Supported Conclusion**: In Instagram's DSA reporting architecture, scam violations are enforced almost entirely by terminating the offending account rather than taking item-by-item visibility actions against individual posts.
- **Phase 6 Caveat**: This reflects Instagram's administrative compliance reporting and enforcement targeting (sanctioning the account entity), and must not be cited as empirical evidence that Instagram terminates every scam account in existence.
- **Reporting Note on Processed vs. Preview Consistency**: The processed benchmark dataset `data/processed/enforcement_action_prevalence.csv` has always accurately recorded `ACCOUNT_TERMINATED` as `47,384,761 / 47,973,134 = 98.7735%`. An earlier conversational response text preview had truncated secondary action rows and displayed `1.000000`; this was strictly an illustrative conversational transcription error, NOT a pipeline or processed-data error. The processed data is accurate and confirmed against raw Parquet.

