# Phase 6A — Candidate Findings & Root-Cause Investigation

**Date**: September 2026  
**Status**: Complete (Phase 6A Analysis, Evidence Boundary, & Sensitivity Review)  
**Methodological Specification**: [MAPPING.md](file:///c:/dsa-moderation-benchmark/MAPPING.md) (Rule 12: Practical Effect Sizes Over P-Values)  
**Authoritative Source Data**: Committed Phase 5 Processed Aggregates (`data/processed/*.csv`)  
**Observation Window**: July 1, 2025 – May 31, 2026 (11 continuous monthly partitions)  
**Primary Benchmark Population**: 661,664,998 represented Statements of Reasons (TikTok: 480,532,153; YouTube: 88,376,558; Instagram: 92,756,287)  

---

## 1. Executive Summary & Analytical Approach

Phase 6A evaluates the cross-platform moderation benchmark established in Phase 5 to identify the strongest, most defensible cross-platform findings. In strict accordance with **MAPPING.md Rule 12**, candidate findings are evaluated on **practical effect magnitude, consistency across relevant categories, consistency across time, substantial volume support, robustness to administrative reporting artifacts, defensible operational interpretations, and actionable Trust & Safety implications**, avoiding conventional significance-testing theater.

All numerical claims are read directly from the verified Phase 5 processed datasets in `data/processed/`.

In accordance with official regulatory specifications (EU DSA Article 17 Implementing Regulation) and MAPPING.md, all automation metrics strictly preserve literal source semantics:
- **`AUTOMATED_DECISION_FULLY`**: Decisions taken exclusively through automated means without human involvement.
- **`AUTOMATED_DECISION_PARTIALLY`**: Decisions taken with automated assistance or where automated means participated in the decision.
- **`AUTOMATED_DECISION_NOT_AUTOMATED`**: Decisions taken without automated means.
- Inferences regarding internal human review queues or operational burdens are strictly demarcated as interpretations or questions for follow-up rather than established facts.

---

## 2. Detection vs. Decision Automation

A critical first step in benchmarking moderation automation is separating the **detection stage** (`automated_detection = Yes`) from the **decision stage** (`automated_decision = FULLY | PARTIALLY | NOT_AUTOMATED`).

### Empirical Comparison:
| Metric Stage | TikTok (480.53M SoRs) | YouTube (88.38M SoRs) | Instagram (92.76M SoRs) | Cross-Platform Spread | Analytical Utility |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Automated Detection Rate** | **97.25%** (467,328,339) | **98.89%** (87,392,106) | **95.53%** (88,610,815) | **3.36 percentage points** | **Low differentiator** (universal industry saturation) |
| **Fully Automated Decision Rate** | **92.44%** (444,185,856) | **49.80%** (44,009,286) | **0.00%** (0) | **92.44 percentage points** | **High differentiator** (divergent autonomous execution) |
| **Decision with Any Automation Rate** | **92.44%** (444,189,374) | **54.67%** (48,317,326) | **95.53%** (88,610,815) | **40.86 percentage points** | **High differentiator** (identifies reliance on automated decision means) |

### Key Takeaways:
1. **Universal Detection Saturation**: All three platforms report automated detection rates exceeding 95.5%. Front-end automated detection is ubiquitous across the industry, providing virtually zero competitive differentiation (spread of only 3.36 pp).
2. **Divergence at Decision Execution**: While automated systems flag the overwhelming majority of content across all platforms, platforms diverge sharply in how decisions are reported:
   - TikTok reports **92.44%** of decisions as `AUTOMATED_DECISION_FULLY` and only 3,518 SoRs (<0.001%) as `PARTIALLY`.
   - Instagram reports **95.53%** of decisions as `AUTOMATED_DECISION_PARTIALLY` and **0.00%** as `FULLY`.
   - YouTube reports **49.80%** as `FULLY`, **4.87%** as `PARTIALLY`, and **45.33%** as `NOT_AUTOMATED` (decisions taken without automated means).
3. **Analytical Implication**: Trust & Safety benchmark comparisons must focus on the **decision stage**. Evaluating detection alone creates an impression of operational parity that masks substantial differences in how final moderation decisions are made.

---

## 3. Candidate Finding Inventory

Six candidate findings spanning diverse operational dimensions were systematically evaluated:

### Candidate 1: Detection-Stage Uniformity (Industry-Wide Saturation)
- **Statement**: Automated detection is nearly universal across TikTok, YouTube, and Instagram (95.53%–98.89%), rendering detection-stage metrics non-differentiating as a competitive benchmark.
- **Platforms**: TikTok, YouTube, Instagram
- **Metric**: Automated Detection Rate (`automated_detection_rate`)
- **Overall Effect Size**: Spread = 3.36 pp (YouTube 98.89% vs Instagram 95.53%; TikTok 97.25% vs YouTube 98.89% = -1.63 pp; TikTok vs Instagram = +1.72 pp). Rate ratios: 0.98x to 1.04x.
- **Represented SoR Denominator**: 661,664,998 SoRs.
- **Category Support**: Broad across almost all non-sparse categories (>85%), with exceptions only in Intellectual Property.
- **Temporal Support**: Stable across all 11 months (monthly spread never exceeds 4.5 pp).
- **Major Caveats**: It is an absence of difference (null finding). Does not capture the operational reality of what occurs after detection.
- **Trust & Safety Implication**: Safety leadership cannot measure moderation posture or technological maturity using detection rates alone; competitive evaluation must shift to decision-stage handoffs.

### Candidate 2: Autonomous Decision Execution Gap (TikTok Overall Fully Automated Decisions)
- **Statement**: TikTok reports a substantially higher share of content moderation decisions taken exclusively by automated means (92.44% fully automated decisions) than YouTube (49.80%, a 42.64 pp gap; 1.86x ratio) and Instagram (0.00%, a 92.44 pp gap).
- **Platforms**: TikTok vs YouTube, TikTok vs Instagram
- **Metric**: Fully Automated Decision Rate (`fully_automated_decision_rate`)
- **Overall Effect Size**: TT vs YT = +42.64 pp (1.86x); TT vs IG = +92.44 pp.
- **Represented SoR Denominator**: 568,908,711 SoRs (TT + YT); 573,288,440 SoRs (TT + IG).
- **Category Support**: TikTok is higher than YouTube across all 6 shared non-sparse categories.
- **Temporal Support**: TikTok > YouTube in 11 of 11 months (monthly gap ranges from +31.42 pp to +64.27 pp, median +40.23 pp).
- **Major Caveats**: 
  1. Confounded by Instagram's DSA reporting architecture, which classifies all automated decisions as `PARTIALLY` (yielding 0.00% `FULLY`).
  2. The overall +42.64 pp gap between TikTok and YouTube is substantially driven by category composition rather than uniform within-category differences.
- **Trust & Safety Implication**: Highlights scale differences in autonomous enforcement, but raises questions regarding how platforms handle edge cases, false positives, and appeals.

### Candidate 3: The Scams & Fraud Decision-Automation Divide (Primary Headline Candidate)
- **Statement**: Automated detection is nearly universal across TikTok, YouTube, and Instagram, but decision-stage automation diverges sharply in Scams & Fraud: YouTube reports only 0.25% of scam/fraud decisions with any automation, versus 84.94% for TikTok and 99.45% for Instagram.
- **Platforms**: YouTube vs TikTok vs Instagram
- **Metric**: Decision with Any Automation Rate (`decision_with_any_automation_rate`) and Fully Automated Decision Rate in `STATEMENT_CATEGORY_SCAMS_AND_FRAUD`.
- **Overall Effect Size**:
  - Decision with Any Automation: YouTube (0.25%) vs TikTok (84.94%): **-84.69 pp** (rate ratio: 0.0029x); YouTube (0.25%) vs Instagram (99.45%): **-99.20 pp** (rate ratio: 0.0025x); TikTok vs Instagram: -14.51 pp (rate ratio: 0.854x).
  - Fully Automated Decisions: YouTube (0.18%) vs TikTok (84.94%): **-84.77 pp** (rate ratio: 0.0021x); YouTube vs Instagram (0.00%): +0.18 pp.
- **Represented SoR Denominator**: **90,782,865 SoRs** (YouTube: 32,688,662; TikTok: 10,121,069; Instagram: 47,973,134) — representing 13.72% of the entire benchmark dataset.
- **Category Support**: Self-contained within `SCAMS_AND_FRAUD`, which is the second-largest category in the benchmark and YouTube's largest single category (36.99% of volume).
- **Temporal Support**: **100% consistent across all 11 months with zero rank reversals**. YouTube's monthly Any Automation rate never exceeds 0.57% (min 0.11%, median 0.25%). TikTok ranges between 75.70% and 95.16%. Instagram ranges between 97.83% and 99.77%.
- **Major Caveats**: DSA data records whether decisions involved automated means; it does not measure specific internal reviewer tools (such as AI confidence scores shown to human decision-makers).
- **Trust & Safety Implication**: Demonstrates a fundamental operational divide in scam moderation between decisions taken with automated means and decisions taken without automated means, warranting targeted audits of handling times, accuracy, and reversal rates.

### Candidate 4: Enforcement Architecture Divergence (Account Termination vs. Content Removal)
- **Statement**: Cross-platform enforcement actions reflect fundamentally divergent compliance architectures: Instagram enforces 88.47% of its SoRs via account termination (`ACCOUNT_TERMINATED`, 82.06M SoRs) and only 7.86% via content removal, whereas YouTube enforces 91.07% via content removal (`CONTENT_REMOVED`, 80.48M SoRs) and 0.00% via account termination, and TikTok splits between non-removal visibility restrictions (`VISIBILITY_OTHER`, 52.57%) and content removal (`CONTENT_REMOVED`, 44.76%).
- **Platforms**: Instagram vs YouTube vs TikTok
- **Metric**: Normalized Enforcement Action Prevalence (`enforcement_action_prevalence.csv`, `overall.csv`).
- **Overall Effect Size**:
  - Account Termination: Instagram 88.47% vs YouTube 0.00% (+88.47 pp); Instagram 88.47% vs TikTok 0.71% (+87.76 pp).
  - Content Removal: YouTube 91.07% vs Instagram 7.86% (+83.21 pp); YouTube 91.07% vs TikTok 44.76% (+46.31 pp).
  - Visibility Other: TikTok 52.57% vs YouTube 0.00% (+52.57 pp); TikTok 52.57% vs Instagram 0.00% (+52.57 pp).
- **Represented SoR Denominator**: 661,664,998 SoRs.
- **Category Support**: Driven strongly by Scams & Fraud (Instagram: 98.77% account terminated; YouTube: 99.39% content removed) and Terms of Service (Instagram: 80.12% account terminated; YouTube: 84.45% content removed).
- **Temporal Support**: Stable across all 11 months.
- **Major Caveats**: Confounded by platform reporting architecture and entity definitions. Instagram reports SoRs primarily per account sanction, whereas YouTube reports SoRs per video takedown.
- **Trust & Safety Implication**: Highlights that platforms tackle violations at different entity layers (user account vs individual content asset).

### Candidate 5: Category Mix as a Driver of Platform Differences (Secondary Supporting Finding)
- **Statement**: Platform-wide decision-automation differences between TikTok (92.44%) and YouTube (54.67%) are substantially associated with differences in category composition: in their largest shared category (`OTHER_VIOLATION_TC`, 400.8M SoRs), YouTube and TikTok report nearly identical decision-automation rates (93.78% vs 93.84%, a 0.06 pp difference), while YouTube's monthly decision-automation variation is strongly associated with shifting category mix.
- **Platforms**: YouTube vs TikTok
- **Metric**: Decomposition of Decision Automation Rates & Monthly Composition.
- **Overall Effect Size**: A substantial portion of the overall 37.76 pp gap is associated with category composition differences. In `OTHER_VIOLATION_TC`, the Any Automation gap collapses to just +0.06 pp.
- **Represented SoR Denominator**: 400,777,274 SoRs in `OTHER_VIOLATION_TC` across both platforms (TT: 359.97M, YT: 40.81M); 42,809,731 SoRs in `SCAMS_AND_FRAUD`.
- **Category Support**: Bridges all 16 categories.
- **Temporal Support**: YouTube's monthly decision automation variations correlate strongly ($r = -0.98$) with the monthly volume share of Scams & Fraud.
- **Major Caveats**: The exact percentage attributed to composition depends on the decomposition convention and reference weights used.
- **Trust & Safety Implication**: Prevents leadership from assuming uniform, platform-wide automation differences; overall platform averages obscure category-specific operational realities.

### Candidate 6: The Spectrum of Human Involvement (Reporting Enum Semantics)
- **Statement**: Platforms report distinct configurations of human and automated participation in moderation decisions: TikTok reports 92.44% fully automated decisions and <0.001% partial automation, Instagram reports 95.53% partially automated decisions and 0.00% fully automated decisions, and YouTube reports a hybrid distribution (49.80% fully automated, 4.87% partially automated, and 45.33% decisions taken without automated means).
- **Platforms**: TikTok vs Instagram vs YouTube
- **Metric**: Distribution of `AUTOMATED_DECISION_FULLY`, `AUTOMATED_DECISION_PARTIALLY`, and `AUTOMATED_DECISION_NOT_AUTOMATED`.
- **Overall Effect Size**: 92.44 pp gap in `FULLY` between TT and IG; 90.66 pp gap in `PARTIALLY` between IG (95.53%) and YT (4.87%).
- **Represented SoR Denominator**: 661,664,998 SoRs.
- **Major Caveats**: Captures legal compliance reporting conventions and schema interpretation as much as underlying algorithmic workflows.
- **Trust & Safety Implication**: Highlights the need for standardizing operational criteria for "partial" automation across platforms.

---

## 4. Category-Level Decision Automation (Cross-Platform Analysis)

Across the 16 standard DSA categories, 28 platform/category combinations have non-sparse, non-zero volume. Cross-platform comparisons for categories shared by at least two non-sparse platforms:

### Cross-Platform Decision Automation in Shared Non-Sparse Categories:
| Category | Platform | Represented SoRs | Category Share | Automated Detection Rate | Fully Automated Decision Rate | Decision with Any Automation Rate | Substantive Category Dynamic |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`OTHER_VIOLATION_TC`** | **TikTok**<br>**YouTube**<br>**Instagram** | 359,970,117<br>40,807,157<br>31,018,501 | 74.91%<br>46.17%<br>33.44% | 97.68%<br>99.19%<br>90.47% | 93.84%<br>86.97%<br>0.00% | **93.84%**<br>**93.78%**<br>**90.47%** | **Near-identical decision automation**: Between TikTok and YouTube, the Any Automation gap is **only +0.06 pp**. |
| **`SCAMS_AND_FRAUD`** | **TikTok**<br>**YouTube**<br>**Instagram** | 10,121,069<br>32,688,662<br>47,973,134 | 2.11%<br>36.99%<br>51.72% | 91.44%<br>99.93%<br>99.45% | 84.94%<br>0.18%<br>0.00% | **84.94%**<br>**0.25%**<br>**99.45%** | **Sharp operational divide**: YouTube reports 0.25% with any automation; TikTok & Instagram report $>84.9\%$. |
| **`PROTECTION_OF_MINORS`** | **TikTok**<br>**YouTube**<br>**Instagram** | 6,667,794<br>892,667<br>1,359,964 | 1.39%<br>1.01%<br>1.47% | 88.12%<br>99.99%<br>87.63% | 42.23%<br>0.02%<br>0.00% | **42.24%**<br>**99.98%**<br>**87.63%** | YouTube heavily reports `PARTIALLY` automated decisions (99.96%); TikTok splits (42.2% fully, 57.8% without automation). |
| **`NEGATIVE_EFFECTS_CIVIC`**| **TikTok**<br>**YouTube**<br>**Instagram** | 14,679,391<br>1,181,064<br>*Sparse* | 3.05%<br>1.34%<br>0.00% | 99.08%<br>99.70%<br>— | 97.74%<br>6.25%<br>— | **97.74%**<br>**6.25%**<br>— | **TikTok highly automated (+91.49 pp)**; YouTube reports 93.75% decisions taken without automated means. |
| **`DATA_PROTECTION_PRIVACY`**| **TikTok**<br>**YouTube**<br>**Instagram** | 2,143,309<br>93,724<br>8,463,282 | 0.45%<br>0.11%<br>9.12% | 96.49%<br>68.38%<br>99.82% | 96.21%<br>0.00%<br>0.00% | **96.21%**<br>**68.33%**<br>**99.82%** | TikTok & Instagram $>96\%$ automated; YouTube at 68.3% (and 0% fully). |
| **`IP_INFRINGEMENTS`** | **TikTok**<br>**YouTube**<br>**Instagram** | 627,729<br>398,842<br>349,957 | 0.13%<br>0.45%<br>0.38% | 43.54%<br>14.21%<br>45.97% | 70.13%<br>0.10%<br>0.00% | **70.18%**<br>**66.60%**<br>**45.97%** | Lower detection across all (<46%); YouTube & TikTok reach ~67%–70% any-automation. |
| **`UNSAFE_PRODUCTS`** | **TikTok**<br>**YouTube**<br>**Instagram** | *Sparse*<br>5,369,201<br>657,406 | 0.00%<br>6.08%<br>0.71% | —<br>98.37%<br>87.49% | —<br>88.37%<br>0.00% | —<br>**92.83%**<br>**87.49%** | YouTube reports 88.37% fully automated decisions; Instagram reports 87.49% partially automated. |

#### Category Groupings:
1. **TikTok Materially Above Competitors**:
   - `NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS`: TikTok reports 97.74% fully automated decisions vs YouTube's 6.25% (+91.49 pp).
   - `DATA_PROTECTION_AND_PRIVACY_VIOLATIONS`: TikTok reports 96.21% fully automated decisions vs YouTube's 0.00% (+96.21 pp).
2. **YouTube Materially Above Competitors**:
   - `PROTECTION_OF_MINORS`: On *Decision with Any Automation*, YouTube reports 99.98% (almost entirely `PARTIALLY`), compared to TikTok's 42.24% (+57.74 pp) and Instagram's 87.63% (+12.35 pp).
3. **Instagram Materially Above Competitors**:
   - `SCAMS_AND_FRAUD`: On *Decision with Any Automation*, Instagram reports 99.45% across 47.97M SoRs, exceeding TikTok (84.94%, +14.51 pp) and YouTube (0.25%, +99.20 pp).
4. **Platforms Are Similar**:
   - `OTHER_VIOLATION_TC`: On *Decision with Any Automation*, TikTok (93.84%), YouTube (93.78%), and Instagram (90.47%) are clustered within 3.37 pp. Between TikTok and YouTube, the difference is **only +0.06 percentage points**.
5. **Structurally Misleading Comparisons (Asymmetric Usage)**:
   - `ILLEGAL_OR_HARMFUL_SPEECH`: TikTok reports 73,417,484 SoRs (15.28% of its volume; 90.59% automated decisions), whereas YouTube reports 49,113 SoRs (sparse, 0.06% share) and Instagram reports 618,295 SoRs (0.67% share). Direct cross-platform comparison is structurally misleading because YouTube categorizes speech violations under other policy headings or general terms of service.
   - `CONSUMER_INFORMATION`: YouTube reports 6,853,913 SoRs (7.76% of its volume; 52.98% automated decisions), whereas TikTok reports 0 SoRs and Instagram reports 0 SoRs.

---

## 5. Category Consistency & Decomposition Sensitivity Analysis

### A. Sensitivity of the Oaxaca-Kitagawa Decomposition (Candidate 5)
In evaluating the 37.76 pp overall gap in *Decision with Any Automation* between TikTok (92.44%) and YouTube (54.67%), we audited how decomposition assumptions affect the estimated share attributed to category composition versus within-category rates.

#### 1. Zero-Volume Categories Identified:
Across the 16 DSA categories:
- **`CONSUMER_INFORMATION`**: YouTube has 6,853,913 SoRs (rate = 52.98%), while TikTok has **0 SoRs** (rate is unobserved / NaN).
- **`SELF_HARM`**: TikTok has 894,159 SoRs (rate = 65.95%), while YouTube has **0 SoRs** (rate is unobserved / NaN).
- **`SCOPE_OF_PLATFORM_SERVICE`**: TikTok has 555 SoRs (rate = 50.27%), while YouTube has **0 SoRs** (rate is unobserved / NaN).
- **`PORNOGRAPHY_OR_SEXUALIZED_CONTENT`**: TikTok has 137 SoRs (rate = 0.73%), while YouTube has **0 SoRs** (rate is unobserved / NaN).

Non-overlapping categories represent **7.76% of YouTube's total volume** (6.85M SoRs) and **0.19% of TikTok's volume** (895K SoRs).

#### 2. Decomposition Results Under Alternative Reference Conventions:
$$\Delta Y = Y_{\text{TT}} - Y_{\text{YT}} = 37.7649 \text{ percentage points}$$

| Decomposition Convention | Reference / Imputation Assumption | Estimated Composition Effect | Estimated Rate Effect | Composition Share of Gap | Rate Share of Gap |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Symmetric (Impute 0 for NaN)** | Category rates for zero-volume slices imputed as 0.0; symmetric midpoint weights $\bar{w}$ and $\bar{r}$. | +23.93 pp | +13.84 pp | **63.4%** | **36.6%** |
| **2. TikTok Rates as Reference** | Counterfactual evaluates weighting with TikTok rates; unobserved categories assume peer rate. | +11.02 pp | +26.75 pp | **29.2%** | **70.8%** |
| **3. YouTube Rates as Reference** | Counterfactual evaluates weighting with YouTube rates; unobserved categories assume peer rate. | +32.85 pp | +4.92 pp | **87.0%** | **13.0%** |
| **4. Overlapping Subset (12 Categories)** | Re-normalized on the 12 categories where both platforms have volume $> 0$ (gap = 37.67 pp). | +20.71 pp | +16.96 pp | **55.0%** | **45.0%** |

#### 3. Methodological Takeaway:
Because the estimated composition share varies from **29.2% to 87.0%** depending on the reference convention chosen (and is **55.0%** on the strictly overlapping subset), "63.4%" must not be cited as a singular, definitive fact.

Instead, the defensible methodological conclusion is:
> **"A substantial portion of the overall gap is associated with differences in category composition."**

Independent empirical support for this conclusion comes from YouTube's monthly time series: YouTube's platform-wide decision-automation rate varies from 30.55% (Nov 2025) to 62.52% (Apr 2026), and this variation correlates strongly ($r = -0.98$) with shifts in the volume share of Scams & Fraud.

---

## 6. Temporal Robustness Analysis (11-Month Window)

Using `automation_monthly.csv` and `automation_category_monthly.csv` across all 11 monthly partitions (`2025-07-01` through `2026-05-01`):

| Candidate Finding | Min Monthly Effect | Max Monthly Effect | Median Monthly Effect | Consistent Direction Months | Rank Reversals | Validated Robustness Caveat |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **C1: Detection Saturation** | 1.84 pp spread | 4.48 pp spread | 3.25 pp spread | 11 / 11 months | 0 | Unaffected by monthly swings |
| **C2: TikTok vs YouTube Fully Automated** | +31.42 pp (Apr 2026) | +64.27 pp (Nov 2025) | +40.23 pp (Oct 2025) | 11 / 11 months | 0 | TikTok Jan delayed-batch surge shifts rates by <0.25 pp |
| **C3: Scams & Fraud Divide (YT vs TT/IG)** | **-75.59 pp** (Nov 2025) | **-94.25 pp** (May 2026) | **-84.69 pp** (Jan 2026) | **11 / 11 months** | **0** | **Rock-solid: YouTube Scams Any Automation rate never exceeds 0.57% in any month** |
| **C4: Instagram Account Termination** | 84.70% (May 2026) | 99.90% (Nov 2025) | 99.77% (Jan 2026) | 11 / 11 months | 0 | Consistently >84% in every month |
| **C5: YouTube Composition Volatility** | 33.09% (Nov 2025) | 67.97% (Apr 2026) | 51.92% (Jan 2026) | 11 / 11 months | 0 | Shifts correlate $r = -0.98$ with monthly Scams SoR volume share |

---

## 7. Enforcement Behavior Candidate Analysis

From `data/processed/enforcement_action_overall.csv` and `enforcement_action_prevalence.csv`:

### Cross-Platform Normalized Action Prevalence:
| Normalized Action | Instagram Prevalence (Numerators) | TikTok Prevalence (Numerators) | YouTube Prevalence (Numerators) | Primary Platform Concentration |
| :--- | :---: | :---: | :---: | :--- |
| **`ACCOUNT_TERMINATED`** | **88.47%** (82,062,141) | **0.71%** (3,394,132) | **0.00%** (0) | **Instagram-centric**: Accounts for 96.0% of all account terminations across the study. |
| **`CONTENT_REMOVED`** | **7.86%** (7,293,475) | **44.76%** (215,104,597) | **91.07%** (80,483,494) | **YouTube/TikTok primary**: YouTube enforces almost exclusively via content removal. |
| **`VISIBILITY_OTHER`** | **0.00%** (0) | **52.57%** (252,603,089) | **0.00%** (0) | **TikTok exclusive**: Over half of TikTok enforcements are non-removal visibility restrictions. |
| **`CONTENT_DISABLED`** | **0.00%** (2,874) | **0.10%** (478,023) | **6.49%** (5,736,894) | **YouTube secondary**: Feature-level disabling (e.g. disabling comments/embeds). |
| **`CONTENT_DEMOTED`** | **3.66%** (3,396,796) | **0.00%** (16,585) | **0.00%** (0) | **Instagram secondary**: Downranking / distribution reduction. |

#### Verified Fact on Instagram Scams Enforcement:
In `STATEMENT_CATEGORY_SCAMS_AND_FRAUD`, Instagram's 47,973,134 represented SoRs break down into:
- **`ACCOUNT_TERMINATED`**: **47,384,761 SoRs (98.7735%)**
- **`CONTENT_REMOVED`**: **587,837 SoRs (1.2253%)**
- **`CONTENT_DISABLED`**: **510 SoRs (0.0011%)**
- **`ACCOUNT_SUSPENDED`**: **26 SoRs (0.0001%)**
*(Sum = 47,973,134 SoRs, 100.0000%)*. The earlier 100% figure was strictly an illustrative preview truncation, not a processed-data error.

---

## 8. Root-Cause Analysis (Demarcating Observations, Interpretations, Follow-Up Questions)

### A. The Scams & Fraud Decision-Automation Divide (Candidate 3)

#### 1. OBSERVATION (Established Directly by DSA Data):
- In `STATEMENT_CATEGORY_SCAMS_AND_FRAUD`, YouTube reported **32,688,662 SoRs**. While 99.93% (32,664,570 SoRs) were flagged by automated detection, **99.75% (32,607,614 SoRs) were reported as `AUTOMATED_DECISION_NOT_AUTOMATED`** (decisions taken without automated means). Only 0.25% (81,048 SoRs) involved automation in the decision stage.
- In the same category, TikTok reported **10,121,069 SoRs**, of which **84.94% (8,597,108 SoRs) were reported as `AUTOMATED_DECISION_FULLY`** (decisions taken exclusively through automated means).
- Instagram reported **47,973,134 SoRs**, of which **99.45% (47,710,406 SoRs) were reported as `AUTOMATED_DECISION_PARTIALLY`**, with 98.77% resulting in `ACCOUNT_TERMINATED`.
- This cross-platform divergence is stable across all 11 monthly partitions without a single rank reversal.

#### 2. INTERPRETATION (Plausible Operational Context):
- The platforms report fundamentally different decision-making arrangements in scam moderation. In YouTube's reporting, scam enforcements are almost universally decided without automated means. In TikTok and Instagram's reporting, automated systems participate in or execute the decision for the vast majority of scam enforcements.

#### 3. QUESTIONS FOR FOLLOW-UP (Not Established by Data):
- What internal interfaces or AI-generated signals assist the decision-makers in YouTube's scam workflow?
- How do false-positive rates, user appeal volumes, and appeal overturn rates compare across the automated versus non-automated decision pipelines?
- Does YouTube's concentration on non-automated decisions reflect specific policy safeguards around creator monetization or channel termination?
- Do TikTok and Instagram experience higher rates of erroneous account terminations or content removals in financial fraud categories?

---

### B. Category Mix Driving Platform Differences (Candidate 5)

#### 1. OBSERVATION (Established Directly by DSA Data):
- In their largest shared category, `OTHER_VIOLATION_TC` (Terms of Service, representing 400.78M SoRs combined), YouTube's Decision with Any Automation Rate is **93.78%** (40.81M SoRs) and TikTok's is **93.84%** (359.97M SoRs) — a difference of **just +0.06 percentage points**.
- YouTube's monthly platform-wide decision-automation rate varies from 30.55% (Nov 2025) to 62.52% (Apr 2026). This variation is strongly associated ($r = -0.98$) with the monthly share of Scams & Fraud in YouTube's SoR volume (which ranged from 63.47% in Nov 2025 to 26.51% in Apr 2026).
- Sensitivity testing demonstrates that between 29.2% and 87.0% (55.0% on the overlapping category subset) of the overall 37.76 pp Any Automation gap between TikTok and YouTube is associated with category composition differences.

#### 2. INTERPRETATION (Plausible Operational Context):
- Platform-wide average automation rates can be misleading because they aggregate policy areas with substantially different operational workflows. YouTube is not uniformly less automated across all policies; its overall automation rate is heavily weighted down by its large volume of scam decisions taken without automated means.

#### 3. QUESTIONS FOR FOLLOW-UP (Not Established by Data):
- Why did YouTube's volume of scam enforcements surge to 63.5% of its total submissions in November 2025? Does this reflect an external spike in adversarial activity, a periodic administrative sweep, or changes in internal logging?

---

## 9. Structured Candidate Scorecard

Candidates evaluated on a 1 (poor / severe limitation) to 5 (excellent / highly robust) scale:

| Candidate Finding | Effect Magnitude | Category Consistency | Temporal Consistency | Volume Support | Measurement Comparability | Operational Relevance | Caveat Burden (5=few caveats) | TOTAL SCORE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: Detection Saturation** | 1 | 4 | 5 | 5 | 5 | 3 | 5 | **28** |
| **C2: Autonomous Decision Gap** | 5 | 3 | 5 | 5 | 2 | 4 | 2 | **26** |
| **C3: Scams & Fraud Decision-Automation Divide** | **5** | **5** | **5** | **5** | **4** | **5** | **4** | **33** |
| **C4: Enforcement Architecture** | 5 | 4 | 5 | 5 | 2 | 4 | 2 | **27** |
| **C5: Category Mix Decomposition**| **4** | **5** | **5** | **5** | **4** | **5** | **4** | **32** |
| **C6: Spectrum of Human Review** | 5 | 3 | 5 | 5 | 2 | 3 | 1 | **24** |

**Scorecard Decision**: Candidate 3 remains the highest-scoring candidate (33/35). Because it focuses on a single category with 90.78M SoRs, consistent direction across all 11 months (0 rank reversals), and exact enum definitions, it is not subject to the between-category composition issue affecting platform-wide averages. Within-category differences in content type, geography, source type, or other unobserved composition may still exist. Candidate 5 serves as the ideal secondary finding (32/35) to provide vital methodological context.

---

## 10. Headline Recommendation

### PRIMARY HEADLINE CANDIDATE:
> **The Scams & Fraud Decision-Automation Divide (Candidate 3)**  
> *"Automated detection is nearly universal across TikTok, YouTube, and Instagram, but decision-stage automation diverges sharply in Scams & Fraud: YouTube reports only 0.25% of scam/fraud decisions with any automation, versus 84.94% for TikTok and 99.45% for Instagram."*

- **Exact Effect Sizes**:
  - Decision with Any Automation: YouTube (0.25%) vs TikTok (84.94%): **-84.69 percentage points** (ratio: 0.0029x); YouTube (0.25%) vs Instagram (99.45%): **-99.20 percentage points** (ratio: 0.0025x).
  - Fully Automated Decisions: YouTube (0.18%) vs TikTok (84.94%): **-84.77 percentage points** (ratio: 0.0021x).
- **Represented SoR Support**: **90,782,865 SoRs** across all three platforms (YouTube: 32,688,662; Instagram: 47,973,134; TikTok: 10,121,069) — 13.72% of the entire benchmark dataset.
- **Category Consistency**: Evaluates a single major policy category, eliminating between-category composition distortions.
- **Temporal Consistency**: Consistent across all 11 monthly partitions with **zero rank reversals**; YouTube's monthly Any Automation rate in scams never exceeds 0.57%.
- **Relevant Caveats**: DSA data records administrative Statements of Reasons; it does not measure specific tooling shown to human reviewers.
- **What Data Does NOT Establish**: Does not establish which approach achieved higher precision, lower false-positive rates, or better protected users from net financial harm.

---

### SECONDARY SUPPORTING FINDING:
> **Category Composition Explains Overall Platform Gaps (Candidate 5)**  
> *"Platform-wide decision-automation differences between TikTok (92.44%) and YouTube (54.67%) are substantially associated with differences in category composition: in their largest shared category (`OTHER_VIOLATION_TC`, 400.8M SoRs), YouTube and TikTok report nearly identical decision-automation rates (93.78% vs 93.84%, a 0.06 pp difference), while YouTube's monthly decision-automation variation is strongly associated with changes in category composition."*

---

## 11. Concrete Trust & Safety Recommendations

Derived directly from the primary and secondary findings without assuming that higher automation is inherently superior:

1. **Audit the Decision-Stage Automation Boundary in High-Volume Queues**: Safety teams should audit the decision-stage automation boundary in Scams & Fraud. Where a platform reports unusually low or unusually high decision automation relative to peers, evaluate false-positive rates, appeal/reversal rates, handling time, harm severity, and reviewer escalation patterns before changing the automation/human-review mix.
2. **Evaluate Risk Trade-Offs Before Rebalancing Automation**: 
   - Platforms with near-zero decision automation in scams (such as YouTube's reported 0.25%) should investigate whether decision backlogs, handling latency, or reviewer fatigue impact enforcement effectiveness, and evaluate whether high-confidence fraud patterns can safely incorporate automated decision assistance.
   - Platforms with high autonomous decision rates (such as TikTok's 84.94% fully automated decisions) and high account termination rates (such as Instagram's 98.77%) should rigorously audit account recovery pathways, false-positive appeals, and adversarial evasion dynamics to ensure legitimate users are not wrongfully disenfranchised.
3. **Standardize Regulatory Compliance Definitions for Human-AI Workflows**: Industry working groups and regulatory bodies should establish precise, standardized criteria for `AUTOMATED_DECISION_PARTIALLY` to ensure public transparency data accurately reflects operational distinctions between automated decisioning and human oversight.

---

## 12. Assessment of TikTok Historical Context

- **Historical Data**: TikTok's first-party transparency reports document that its self-reported automated removal share grew from **14.26% in 2021Q1 to 96.74% in 2026Q1**.
- **Role in Report**: TikTok's self-reported automated-removal share rose substantially over the five-year period, providing historical context consistent with the high automation observed in its later DSA submissions.
- **Strict Methodological Safeguards**:
  - Labeled explicitly as *TikTok self-reported platform data*.
  - Unit is *removed short-form videos* (distinct from DSA *Statements of Reasons*).
  - Kept strictly as narrative context; never merged mathematically with DSA numbers.
  - Supplementary YouTube and Instagram metrics remain strictly excluded.
