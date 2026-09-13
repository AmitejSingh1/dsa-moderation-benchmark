# Cross-Platform Content Moderation Benchmark

**Authoritative Source**: EU Digital Services Act (DSA) Transparency Database  
**Observation Window**: July 1, 2025 – May 31, 2026 (11 continuous monthly partitions)  
**Population Analyzed**: 661,664,998 represented Statements of Reasons across TikTok, YouTube, and Instagram  
**Methodological Specification**: [MAPPING.md](file:///c:/dsa-moderation-benchmark/MAPPING.md) | **Audit Report**: [phase5_validation.md](file:///c:/dsa-moderation-benchmark/reports/phase5_validation.md)  

---

## Executive Summary

As regulatory scrutiny and algorithmic complexity intensify across the tech industry, Trust & Safety leaders, operational planners, and regulators face a persistent challenge: **how to evaluate and benchmark content moderation automation across major platforms on an objective, comparable basis.**

This report delivers a rigorous cross-platform content moderation benchmark analyzing **661,664,998 official Statements of Reasons (SoRs)** submitted under Article 17 of the EU Digital Services Act (DSA) by **TikTok (480.5M SoRs)**, **YouTube (88.4M SoRs)**, and **Instagram (92.8M SoRs)** across an 11-month harmonized schema window (July 1, 2025 through May 31, 2026).

```
========================================================================================
PRIMARY HEADLINE FINDING:
"Automated detection is nearly universal across TikTok, YouTube, and Instagram, but
decision-stage automation diverges sharply in Scams & Fraud: YouTube reports only 0.25%
of scam/fraud decisions with any automation, versus 84.94% for TikTok and 99.45% for Instagram."
========================================================================================
```

Our investigation yields three core empirical findings:

1. **Universal Detection Saturation**: Automated detection is nearly universal across all three platforms (TikTok: 97.25%, YouTube: 98.89%, Instagram: 95.53%). The cross-platform spread is only 3.36 percentage points. Front-end automated detection is standard industry practice and provides negligible differentiation between competitors.
2. **Sharp Decision Divergence in High-Risk Queues**: In **Scams & Fraud** (representing 90,782,865 SoRs, or 13.72% of the entire benchmark), reported decision-stage automation diverges radically. YouTube reports only **0.25%** of scam decisions involving automated means (99.75% reported as decisions taken without automated means across 32.7M SoRs), whereas TikTok automates **84.94%** of decisions fully, and Instagram reports **99.45%** of decisions involving automated assistance (with 98.77% resulting in account termination). This pattern is consistent across all 11 monthly partitions with zero rank reversals.
3. **Platform-Wide Averages Obscure Category Realities**: While TikTok leads YouTube by **37.76 percentage points** in overall decision automation (92.44% vs 54.67%), this gap is substantially associated with differences in category composition. In their largest shared category (**Terms of Service violations**, representing 400.8M SoRs), YouTube and TikTok report virtually identical decision automation rates (**93.78% vs 93.84%**, a 0.06 pp difference).

**Actionable Recommendation**: Safety teams and Trust & Safety executives should audit the decision-stage automation boundary in Scams & Fraud. Where a platform reports unusually low or unusually high decision automation relative to peers, teams should systematically evaluate **false-positive rates, appeal and reversal rates, handling time, harm severity, and escalation patterns** before changing the automation mix.

---

## 1. Why This Benchmark

Content moderation has historically been evaluated through first-party corporate transparency reports. However, first-party reports lack common definitions, unified taxonomies, and standardized metrics. Platforms report non-comparable concepts: YouTube reports video removals and automated flagging; Meta reports "proactive rates" on actioned posts; TikTok reports automated video removals. Comparing these disparate self-reported figures creates false equivalences across operational stages.

The EU Digital Services Act Transparency Database (DSA TDB) provides the world's first standardized regulatory repository of individual moderation actions. Under Article 17, Very Large Online Platforms (VLOPs) must submit a Statement of Reasons for every restriction applied to user content or accounts within the European Union. 

### Separating Detection from Decision Execution
A critical methodological distinction enforced throughout this study is separating:
- **`automated_detection`** (`Yes` / `No`): Did an automated system initially detect or flag the content before or concurrent with action?
- **`automated_decision`** (`FULLY` / `PARTIALLY` / `NOT_AUTOMATED`): Was the final sanction applied exclusively by automated means, with automated assistance, or without automated means?

Conflating detection with decision execution obscures the actual division of labor between algorithms and human personnel. As this benchmark demonstrates, platforms can have near-identical automated detection rates while maintaining fundamentally different decision-making architectures.

---

## 2. Data & Method

This benchmark is built upon the official EU DSA Complete Aggregated Parquet repository (`aggregated-complete.parquet`), acquired reproducibly via the European Commission's public endpoints:

- **Target Platforms**: TikTok, YouTube, Instagram (Meta).
- **Observation Window**: July 1, 2025 through May 31, 2026 (11 continuous monthly partitions). This period reflects the stable, harmonized DSA schema following the European Commission's June 2025 specification overhaul.
- **Population Analyzed**: Exactly **661,664,998 represented Statements of Reasons** across 17,223,049 physical Parquet rows.
  - **TikTok**: 480,532,153 SoRs (72.62% of benchmark volume)
  - **YouTube**: 88,376,558 SoRs (13.36%)
  - **Instagram**: 92,756,287 SoRs (14.02%)
- **Weighting Invariant**: All aggregations, category shares, and platform-wide rates are strictly volume-weighted using `SUM(count)` (MAPPING.md Rule 4).
- **Taxonomy Standard**: Analysis uses the official 16-category DSA regulatory schema string values. Zero-volume combinations report rates as `NaN`/null (never false 0.0%), and categories representing $<0.10\%$ of a platform's volume are flagged as sparse (MAPPING.md Rule 6).
- **Practical Effect Sizes Over P-Values**: In accordance with MAPPING.md Rule 12, differences are evaluated by substantive effect magnitude (percentage-point differences and rate ratios) rather than null-hypothesis significance tests ($p$-values), which become uninformative on hundreds of millions of records.

For complete verification logs and independent replication scripts, see [MAPPING.md](file:///c:/dsa-moderation-benchmark/MAPPING.md) and [phase5_validation.md](file:///c:/dsa-moderation-benchmark/reports/phase5_validation.md).

---

## 3. Finding 1 — Detection Is Nearly Universal

Across all 661.7 million moderation decisions, front-end automated detection has achieved universal industry saturation:

| Platform | Total Represented SoRs | Automated Detection Numerator | Automated Detection Rate |
| :--- | :---: | :---: | :---: |
| **YouTube** | 88,376,558 | 87,392,106 | **98.89%** |
| **TikTok** | 480,532,153 | 467,328,339 | **97.25%** |
| **Instagram** | 92,756,287 | 88,610,815 | **95.53%** |

![Chart 1: Detection vs Decision Automation](file:///c:/dsa-moderation-benchmark/reports/charts/01_detection_vs_decision.png)

### Key Analytical Takeaways:
- **Zero Meaningful Differentiation**: The spread across platforms is only **3.36 percentage points** (rate ratios range from 0.98x to 1.04x). All three platforms deploy automated computer vision, text classifiers, and perceptual hashes to flag content at massive scale.
- **Detection Is Not Moderation Quality**: Automated detection measures whether machine systems flagged content; it does not measure detection precision, recall, or user harm mitigation.
- **Strategic Implications for Trust & Safety**: Benchmarking safety organizations based solely on automated detection rates is an uninformative exercise. Automated detection is a commodity baseline across major services; the true strategic and operational choices occur at the decision-execution stage.

---

## 4. Finding 2 — Scams & Fraud Decision-Automation Divide (Primary Headline)

While automated detection is universally high, platforms diverge diametrically in how they resolve moderation decisions in high-stakes violation queues. This divergence is epitomized by **Scams & Fraud** (`STATEMENT_CATEGORY_SCAMS_AND_FRAUD`), which constitutes **90,782,865 represented SoRs** (13.72% of the primary benchmark dataset, and YouTube's single largest moderation burden).

```
========================================================================================
"Automated detection is nearly universal across TikTok, YouTube, and Instagram, but
decision-stage automation diverges sharply in Scams & Fraud: YouTube reports only 0.25%
of scam/fraud decisions with any automation, versus 84.94% for TikTok and 99.45% for Instagram."
========================================================================================
```

### Quantitative Breakdown in Scams & Fraud:
| Platform | Category Volume (SoRs) | Category Share of Platform | Automated Detection Rate | Decision with Any Automation Rate | Fully Automated Decision Rate | Decisions Without Automated Means (`NOT_AUTOMATED`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **YouTube** | 32,688,662 | 36.99% | **99.93%** (32.66M) | **0.25%** (81,048) | **0.18%** (57,597) | **99.75%** (32,607,614) |
| **TikTok** | 10,121,069 | 2.11% | **91.44%** (9.26M) | **84.94%** (8.60M) | **84.94%** (8.60M) | **15.06%** (1,523,925) |
| **Instagram** | 47,973,134 | 51.72% | **99.45%** (47.71M) | **99.45%** (47.71M) | **0.00%** (0) | **0.55%** (262,728) |

![Chart 2: HERO CHART — Scams & Fraud Decision Automation Divide](file:///c:/dsa-moderation-benchmark/reports/charts/02_scams_decision_automation.png)

### Understanding Official DSA Decision Semantics
Under the DSA Article 17 schema:
- **`AUTOMATED_DECISION_NOT_AUTOMATED`**: Enforces that the decision was taken without automated means.
- **`AUTOMATED_DECISION_PARTIALLY`**: Enforces that automated means assisted or participated in the decision.
- **`AUTOMATED_DECISION_FULLY`**: Enforces that the decision was taken exclusively by automated means without human involvement.

YouTube reports **32,607,614 scam decisions (99.75%)** as taken without automated means, despite detecting 99.93% automatically. Conversely, TikTok reports **84.94%** of scam decisions as fully automated, while Instagram reports **99.45%** as decisions taken with automated means (with 98.77% resulting in account termination).

### 11-Month Temporal Persistence
This cross-platform divide is not a seasonal spike or batch artifact:

![Chart 3: Monthly Persistence of Scams Decision Automation Gap](file:///c:/dsa-moderation-benchmark/reports/charts/03_scams_monthly_consistency.png)

- **Consistent Direction Across All 11 Months**: Across all 11 continuous monthly partitions (July 2025 through May 2026), there were **zero rank reversals**.
- **YouTube Monthly Range**: YouTube's Decision with Any Automation rate in scams never exceeded **0.57%** in any month (min: 0.11% in Nov 2025; median: 0.25% in Jan 2026).
- **TikTok Monthly Range**: TikTok's rate remained bounded between **75.70%** (Nov 2025) and **95.16%** (May 2026).
- **Instagram Monthly Range**: Instagram's rate remained bounded between **97.83%** (Apr 2026) and **99.77%** (Nov 2025).

*Analytical Note*: Higher automation does not indicate higher moderation quality or effectiveness. Different reported profiles may reflect distinct enforcement arrangements, entity targets, or operational trade-offs between decision speed and appeal risks.

---

## 5. Finding 3 — Overall Platform Averages Can Mislead

A central hazard in Trust & Safety analytics is drawing sweeping operational conclusions from aggregate platform-level averages. 

At first glance, platform-wide metrics suggest that TikTok's decision pipeline is vastly more automated than YouTube's:
- **TikTok Overall Decision with Any Automation**: **92.44%**
- **YouTube Overall Decision with Any Automation**: **54.67%**
- **Observed Headline Gap**: **+37.76 percentage points** (Rate Ratio: 1.69x)

However, analyzing the single largest shared category—**Terms of Service Violations** (`OTHER_VIOLATION_TC`, representing **400,777,274 SoRs** across both platforms)—reveals that the apparent gap virtually disappears:

| Decision Automation Metric | TikTok (`OTHER_VIOLATION_TC`) | YouTube (`OTHER_VIOLATION_TC`) | Percentage-Point Difference | Rate Ratio |
| :--- | :---: | :---: | :---: | :---: |
| **Decision with Any Automation Rate** | **93.84%** (337.80M / 359.97M) | **93.78%** (38.27M / 40.81M) | **+0.06 pp** | **1.0007x (Virtual Parity)** |
| **Fully Automated Decision Rate** | **93.84%** (337.80M / 359.97M) | **86.97%** (35.49M / 40.81M) | **+6.87 pp** | **1.0790x** |

![Chart 4: Category Mix Context](file:///c:/dsa-moderation-benchmark/reports/charts/04_category_mix_context.png)

### The Role of Category Composition
The 37.76 pp overall gap is heavily driven by **category composition** rather than a uniform gap in algorithmic capability:
1. On YouTube, **36.99% of all SoRs** are in Scams & Fraud, where reported decision automation is only 0.25%. This single category heavily depresses YouTube's overall average.
2. On TikTok, only **2.11% of SoRs** are in Scams & Fraud, while **74.91%** are concentrated in Terms of Service (where automation is 93.84%) and **15.28%** in Illegal/Harmful Speech (where automation is 90.59%).
3. Formal sensitivity testing across decomposition conventions demonstrates that between **29.2% and 87.0%** (and **55.0%** on the strictly overlapping category subset) of the TikTok–YouTube decision automation gap is associated with category composition differences.
4. Furthermore, YouTube's platform-wide monthly automation swings (ranging from 30.55% in Nov 2025 to 62.52% in Apr 2026) correlate strongly ($r = -0.98$) with shifts in the volume share of Scams & Fraud.

**Key Analytical Takeaway**: Safety teams must compare category-level behavior before drawing operational conclusions from platform-wide averages.

---

## 6. Enforcement Context

Platforms apply distinct compliance architectures when taking enforcement action against violative content or accounts:

![Chart 5: Enforcement Action Prevalence](file:///c:/dsa-moderation-benchmark/reports/charts/05_enforcement_actions.png)

### Normalized Multi-Label Action Prevalence:
| Normalized Action Type | Instagram (92.76M SoRs) | TikTok (480.53M SoRs) | YouTube (88.38M SoRs) | Primary Operational Target |
| :--- | :---: | :---: | :---: | :--- |
| **`ACCOUNT_TERMINATED`** | **88.47%** (82,062,141) | **0.71%** (3,394,132) | **0.00%** (0) | **Account Entity (Identity)** |
| **`CONTENT_REMOVED`** | **7.86%** (7,293,475) | **44.76%** (215,104,597) | **91.07%** (80,483,494) | **Content Asset (Item)** |
| **`VISIBILITY_OTHER`** | **0.00%** (0) | **52.57%** (252,603,089) | **0.00%** (0) | **Distribution / Feed Restriction** |
| **`CONTENT_DISABLED`** | **0.00%** (2,874) | **0.10%** (478,023) | **6.49%** (5,736,894) | **Feature Disabling (Comments/Embeds)** |
| **`CONTENT_DEMOTED`** | **3.66%** (3,396,796) | **0.00%** (16,585) | **0.00%** (0) | **Downranking / Demotion** |

*Methodological Note*: Under DSA reporting, enforcement actions are multi-label; percentages represent independent action prevalence and do not sum to 100%.

### Confirmed Empirical Dynamics:
- **Instagram Targets the Account Identity**: Across all categories, 88.47% of Instagram SoRs record account termination. In Scams & Fraud, **98.7735% (47,384,761 of 47,973,134 SoRs)** record `ACCOUNT_TERMINATED`, while only 1.2253% record content removal. Instagram's compliance reporting reflects a model that addresses financial fraud by disabling the user account entity.
- **YouTube Targets Content Assets**: 91.07% of YouTube SoRs record `CONTENT_REMOVED` (video takedown), with 0.00% recording account termination in DSA aggregates.
- **TikTok Deploys Hybrid Restrictions**: TikTok splits enforcement between non-removal visibility restrictions (`VISIBILITY_OTHER`: 52.57%) and direct removals (`CONTENT_REMOVED`: 44.76%).

These variations reflect divergent enforcement philosophies and reporting architectures rather than superior or inferior compliance strategies.

---

## 7. Historical Context — TikTok Only

To contextualize TikTok's high autonomous decision rate (92.44% overall; 84.94% in scams), first-party transparency data from TikTok's official Community Guidelines Enforcement Reports was reviewed across 21 continuous calendar quarters (2021Q1 through 2026Q1):

- **Historical Trajectory**: TikTok's self-reported share of videos removed by automated systems without human review (`v_auto / v_tot`) rose from **14.26% in 2021Q1** to **96.74% in 2026Q1**.

### Strict Methodological Boundaries:
- **Narrative Context Only**: This multi-year trajectory provides historical context consistent with the high automation observed in TikTok's later DSA submissions.
- **Non-Comparable Units**: The supplementary metric measures *removed short-form videos* globally, whereas the DSA benchmark measures *EU Statements of Reasons*. The two metrics cannot be directly equated or merged mathematically.
- **Exclusion of Competitor Supplementary Data**: Supplementary automated flagging metrics from YouTube and Instagram measure detection stages rather than automated decision execution, and are strictly excluded from quantitative benchmarking to avoid false equivalences.

---

## 8. Actionable Recommendations for Trust & Safety

Derived directly from the empirical findings without presuming that higher automation is inherently optimal:

```
========================================================================================
RECOMMENDATION:
Safety teams should audit the decision-stage automation boundary in Scams & Fraud.
Where automation is unusually low or high relative to peers, evaluate:
- false-positive rates
- appeal rates
- reversal rates
- handling time
- harm severity
- escalation patterns
before changing the automation mix.
========================================================================================
```

### Specific Operational Priorities:

1. **For Platforms with Low Scam Decision Automation (YouTube-like)**:
   - YouTube reported 32.6M Scams & Fraud decisions taken without automated means during the benchmark window.
   - Safety teams should audit the decision-stage automation boundary in Scams & Fraud. Where a platform reports unusually low or unusually high decision automation relative to peers, evaluate false-positive rates, appeal and reversal rates, handling time, harm severity, and escalation patterns before changing the automation mix.
2. **For Platforms with High Autonomous Scam Execution (TikTok-like)**:
   - Where decision automation is high (e.g. TikTok reporting 84.94% fully automated scam decisions), operations should audit false-positive rates, appeal volumes, and reversal workflows.
3. **For Platforms with High Account Termination Rates (Instagram-like)**:
   - Where enforcement heavily targets the account identity (e.g. Instagram reporting 98.77% account termination in Scams & Fraud), safety teams should verify that account redress and appeal mechanisms are accessible and prompt.
4. **For Executive Leadership & Policy Teams**:
   - **De-Averaged Benchmarking**: Cease comparing cross-platform moderation using company-wide aggregate metrics. Require all operational and competitive benchmarking to be conducted at the policy category level.

---

## 9. Limitations & Evidence Boundaries

To maintain scientific integrity, the findings of this benchmark must be interpreted within documented boundaries:

1. **Statements of Reasons Measure Administrative Actions, Not Moderation Quality**: DSA SoRs capture actions taken and reported by platforms; they do not measure the total prevalence of violative content on platforms, user exposure, or underlying platform safety.
2. **Decision Automation Does Not Measure Accuracy**: DSA data records whether automated means participated in or executed a decision; it does not measure precision, recall, false-positive rates, or false-negative rates.
3. **Absence of Appeal and Outcome Data in Aggregates**: The complete aggregate DSA Parquet repository does not link initial Statements of Reasons to subsequent appeal outcomes, user dispute success rates, or content restorations.
4. **Within-Category Composition Differences**: While analyzing at the category level controls for broad policy mix, unobserved differences in content format (long-form video vs short-form video vs photo/story), language, user geography, or source flagger type may still exist.
5. **TikTok January 2026 Delayed Batch Submissions**: Over 80% of TikTok's January 2026 SoRs reflect decisions applied in late 2025. However, sensitivity testing confirms that excluding January 2026 changes TikTok's automation metrics by **less than 0.25 percentage points**, confirming the finding's robustness.
6. **Platform Reporting Architecture Disparities**: Disparities in enforcement action prevalence (e.g. account terminations vs content removals) reflect differences in compliance logging architectures and entity targeting rather than platform effectiveness.

---

*Report authored and validated as part of the EU DSA Moderation Benchmark Project.*  
*Full analytical codebase and reproducible metrics available in the project repository.*
