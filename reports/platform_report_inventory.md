# Platform Transparency Report Inventory

**Phase 3 Deliverable — Platform Transparency Source Inventory & Verification**  
**Date**: September 2026  
**Status**: Verified & Acquired (Phase 3B Complete; 2021Q1–2026Q1 Acquired under data/raw/supplementary/)  
**Primary Source**: EU Digital Services Act (DSA) Transparency Database (`data/raw/dsa_aggregates/`)  
**Supplementary Sources**: Official Quarterly Transparency & Community Guidelines Enforcement Reports (`data/raw/supplementary/`)  

---

## 1. Executive Summary

This inventory evaluates the official, first-party transparency and enforcement reporting systems operated by the three core benchmark services: **YouTube**, **Instagram (Meta)**, and **TikTok**.

While the EU DSA Transparency Database provides the authoritative, harmonized, event-level record of moderation decisions (Statements of Reasons) within the European Union from late September 2023 onward, each platform has published voluntary or regulatory quarterly transparency reports for several years prior.

These platform-published reports serve as valuable **supplementary context** for:
1. Establishing long-term baseline enforcement trajectories before the DSA came into force (2018–2023).
2. Cross-validating high-level directional trends (e.g., shifts in automation reliance, changes in dominant violation categories).
3. Understanding platform-specific definitions, enforcement funnels, and operational constraints that do not map 1:1 to DSA legal categories.

> **CRITICAL METHODOLOGICAL PRINCIPLE**  
> Platform-reported metrics and EU DSA Statements of Reasons (SoRs) **cannot be directly equated or merged**. DSA SoRs measure statutory decision notices issued within the EU regulatory scope, whereas platform transparency reports count physical content items (videos, posts, accounts) actioned globally under platform terms of service. They must be evaluated directionally and comparatively as distinct analytical layers.

---

## 2. Official Platform Transparency Sources (Verified Endpoints)

| Service | Parent Entity | Official Portal / Report Series | Verified Access Mechanism & Endpoints | Publishing Frequency | Verified Coverage | Output Data Formats |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **YouTube** | Google LLC / Alphabet Inc. | YouTube Community Guidelines Transparency Report | • [Policy Overview](https://transparencyreport.google.com/youtube-policy/overview)<br>• [Removals Dashboard](https://transparencyreport.google.com/youtube-policy/removals)<br>• REST API: `https://transparencyreport.google.com/transparencyreport/api/v3/youtubepolicy/`<br>*(No static public CSV download files exist on Google downloads portal for Community Guidelines removals; data is queried dynamically per quarter via official REST JSON endpoints)* | Quarterly | **Q4 2017 – Q2 2026** (35 quarters) | REST API JSON payload (with XSSI prefix `)]}'\n`) |
| **Instagram** | Meta Platforms, Inc. | Community Standards Enforcement Report (CSER) | • [Meta Transparency Center CSER](https://transparency.meta.com/reports/community-standards-enforcement/)<br>• GraphQL Endpoint: `https://transparency.meta.com/api/graphql/`<br>• Operation: `TransparencyReportCSERRootCSVQuery`<br>• Verified Doc ID: `31742207542036840`<br>*(Client-side ZIP `community-standards.zip` containing verified CSV `CSER-2026_Q2.csv`)* | Quarterly | **Q4 2017 – Q2 2026** (35 quarters; Instagram non-N/A data begins **Q2 2019**) | Direct CSV export (`CSER-2026_Q2.csv`) |
| **TikTok** | ByteDance Ltd. | Community Guidelines Enforcement Report (CGER) | • [TikTok Transparency Center](https://www.tiktok.com/transparency/en/community-guidelines-enforcement/)<br>• Official CDN Structured Payloads: `https://sf16-va.tiktokcdn.com/obj/eden-va2/zkyhviozhk_YLNJ/ljhwZthlaukjlkulzlp/2026Q1/`<br>*(Dashboards `2_Volume_English.html`, `3_Speed_English.html`, `4_Policies_English.html` contain structured JSON in `window.injectedData`)* | Quarterly | **Q3 2020 – Q1 2026** (23 continuous quarters; Q2 2026 not yet published) | Structured JSON (`window.injectedData`) |

---

## 3. Platform Coverage Comparison

| Attribute | YouTube (Google) | Instagram (Meta) | TikTok (ByteDance) |
| :--- | :--- | :--- | :--- |
| **Earliest Available Data** | Q4 2017 (Oct–Dec 2017) | Q4 2017 (Facebook); **Q2 2019** (Instagram earliest non-N/A) | Q3 2020 (Continuous quarterly series in modern format) |
| **Latest Available Data** | Q2 2026 | Q2 2026 | **Q1 2026** (Q2 2026 not published as of Sept 2026) |
| **Cadence Consistency** | Highly consistent calendar quarters | Consistent calendar quarters | Regular calendar quarters from Q3 2020 |
| **Geographic Disaggregation** | **Yes**: Country-level breakdown available for video removals (`videoremovalsbycountry`) | **No**: Global figures only for Instagram CSER export | **Partial**: Global figures + country-level breakdown in `5_Geography_English.html` |
| **EU-Specific Filter Available?** | Can isolate EU member states from `videoremovalsbycountry` | No EU breakout in CSER (DSA compliance reports published separately) | No EU breakout in CGER (DSA compliance reports published separately) |
| **Scope of Content Tracked** | Videos, Channels, Comments | Posts, Comments, Stories, Reels (aggregated as "pieces of content") | Videos, Live streams, Accounts, Comments |
| **Service Disaggregation** | Distinct YouTube platform metrics | Distinctly filtered via `app = 'Instagram'` column in `CSER-2026_Q2.csv` | Dedicated single platform |

---

## 4. Metric Taxonomy and Cross-Platform Comparison

| Benchmark Dimension | YouTube Metric | Instagram (Meta) Metric | TikTok Metric | DSA SoR Benchmark Conceptual Analogue |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Volume Metric** | Total videos removed (`totalvideosremoved`) | Content Actioned (`metric = 'Content Actioned'`) | Total Videos Removed (`v_tot` in `2_Volume_English.html`) | Total Statements of Reasons (`total_sor_count`) — *Directionally comparable; not equivalent* |
| **Detection Method** | First Flagged By: Automated Flagging [ID 2] vs Human [IDs 3–7] (`contentremovedbyuser`) | Proactive Rate (`metric = 'Proactive rate'`) | Proactive Removal Rate (`proactive` in `3_Speed_English.html`) | `automated_detection` — *Closest conceptual analogue (measures detection prior to user flag)* |
| **Decision Method** | Not published in removal data (automated vs human decision split unavailable) | **Not published** (Meta does not disclose automated vs human decision split) | **Automated Removal Rate** (`v_auto / v_tot` in `2_Volume_English.html`) | `automated_decision` — *Closest conceptual analogue (moderation executed purely by automation)* |
| **Speed / Exposure** | Views before removal buckets: 0 views, 1–10 views, >10 views (`totalvideoremovalsbyviews`) | Not published by view bucket in standard CSER export | Removed at 0 views (`vv_data`), Removed within 24 hours (`lt24`) | Latency delta (`created_at` minus `application_date`) — *Context only* |
| **User Redress / Appeals** | Appeals submitted, Reinstatements (`totalvideosappealed`, `totalvideosreinstated`) | Content Appealed, Content Restored with appeal, Content Restored without appeal | Restored videos (`v_res`), Appeals submitted | Redress mechanism availability, internal complaint handling — *Directionally comparable* |
| **Prevalence / Exposure** | Violative View Rate (VVR, aggregate YouTube level) | Prevalence, Lowerbound Prevalence, Upperbound Prevalence per policy area | Violative View Rate / Prevalence (`videoData` in `1_Prevalence_English.html`) | None (DSA measures notices issued, not platform impressions) |

---

## 5. Content Violation Category Availability & Mapping Feasibility

Platforms categorize violations according to their respective Terms of Service and Community Guidelines:

| Analytical Category | YouTube Policy Category (Verified IDs) | Meta / Instagram Policy Area (`policy_area`) | TikTok Rule / Heading (Verified) | Mapping Feasibility to DSA Era 2 |
| :--- | :--- | :--- | :--- | :--- |
| **Child Safety & Exploitation** | Child abuse [ID 2] / Child safety | Child Endangerment: Sexual Exploitation; Child Endangerment: Nudity and Physical Abuse | Youth Safety and Well-Being (Youth Sexual and Physical Abuse, Minimum Age Requirement) | **High**: Closest conceptual analogue to child exploitation/safety grounds |
| **Adult Nudity & Sexual Content** | Sexual [ID 6] / Nudity or sexual | Adult Nudity & Sexual Activity | Sensitive and Mature Themes (Body Exposure and Sexualized Behaviors) | **High**: Closest conceptual analogue to `PORNOGRAPHY_OR_SEXUAL_CONTENT` |
| **Hate Speech & Discrimination** | Hateful or abusive [ID 4] | Hateful Conduct *(formerly Hate Speech)* | Safety and Civility (Hate Speech and Hateful Behavior) | **Moderate**: Platform definitions and protected thresholds differ |
| **Harassment & Bullying** | Harassment and cyberbullying [ID 2 in alt map] | Bullying & Harassment | Safety and Civility (Harassment and Bullying) | **Moderate**: Differing boundaries between cyberbullying, defamation, and harassment |
| **Violence, Extremism & Harm** | Violent or repulsive [ID 8]; Promotes terrorism [ID 7] | Violent and Graphic Content; Dangerous Organizations (Terrorism, Organized Hate) | Safety and Civility (Violent and Hateful Organizations, Violent and Criminal Behavior) | **High**: Closest conceptual analogue to `VIOLENCE` and `TERRORISM` |
| **Suicide & Self-Harm** | Suicide, self-harm, or eating disorders [ID 10] | Suicide, Self-Injury, and Eating Disorders | Mental and Behavioral Health (Suicide and Self-Harm, Disordered Eating) | **High**: Closest conceptual analogue to `SELF_HARM` |
| **Regulated & Illegal Goods** | Regulated goods and services [ID 22 in authority map] | Restricted Goods & Services (Drugs, Firearms) | Regulated Goods, Services, and Commercial Activities | **Moderate**: Differences in commercial solicitation and alcohol/tobacco inclusion |
| **Spam, Scams & Integrity** | Spam or misleading [ID 5] | Spam; Fake Accounts | Integrity and Authenticity (Deceptive Behaviors, Fake Engagement, Frauds & Scams) | **Low**: Structural disparity (account-level enforcement on Meta vs content sweeps on YouTube/TikTok) |
| **Misinformation / Civic** | Misinformation [ID 12 in alt map] | Fact-checked misinformation (separate reporting) | Integrity and Authenticity (Civic and Election Integrity, Misinformation, Edited Media/AIGC) | **Moderate**: Differing civic integrity and synthetic media policies |

---

## 6. Comparability Assessment Matrix

We classify the comparability of supplementary platform reports against EU DSA data into four distinct levels:

| Level | Definition | Applicable Metrics & Categories | Methodological Guidance |
| :--- | :--- | :--- | :--- |
| **Direct** | Statistically equivalent or 1:1 interchangeable. | **NONE** | **Never combine, equate, or directly subtract DSA counts from platform report counts.** |
| **Directional** | Metrics track the same underlying operational phenomenon over time, allowing trend and growth rate comparisons. | • Direction of automated detection adoption (proactive detection trend).<br>• Relative share of top violation categories (e.g., adult content vs hate speech).<br>• Appeal reinstatement success rates. | Compare % changes quarter-over-quarter and relative proportions across platforms. |
| **Context Only** | Informs qualitative or structural understanding of platform architecture and historical baselines, but cannot be quantitatively normalized. | • Absolute content volumes actioned globally.<br>• Account terminations.<br>• Pre-2023 baseline enforcement activity. | Use to contextualize the scale and historical maturation of moderation systems prior to DSA. |
| **Not Useful** | Metrics that appear similar but suffer from incompatible definitions, scope, or missing denominators. | • Comparing raw Instagram "Content Actioned" to YouTube "Videos Removed".<br>• Equating Meta's "Proactive Rate" with DSA's `automated_decision = True`. | Do not present on identical chart axes without explicit distinction warnings. |

---

## 7. Critical Automation Terminology & Measurement Mismatch

The single greatest source of misinterpretation in content moderation benchmarking is conflating **detection** with **decision**:

```
Enforcement Pipeline:
[ Content Upload ] 
       │
       ▼
[ Detection Stage ] ──────► Stage A/B: Proactive / Automated Flagging vs User Flagging
       │
       ▼
[ Review & Triage ] ──────► Human Moderator vs. Automated Decision Engine
       │
       ▼
[ Action / Removal ] ─────► Stage C: Moderation Decision Executed (Automated vs Human)
```

### Automation Dimensions:
- **Dimension A**: Detection before user report (Proactive detection).
- **Dimension B**: Automated / system flagging (System detection).
- **Dimension C**: Moderation decision without human review (Automated enforcement).

### Verified Platform Metrics and DSA Classification:

1. **YouTube "Automated Flagging"**:
   - *Official Definition*: Removals where the first flag was generated by automated detection systems.
   - *Denominator*: Total videos removed for Community Guidelines violations.
   - *Enforcement Stage*: **Stage B (Automated Flagging / Detection)**. Once flagged, videos may be routed to human review or automated removal. YouTube does not report the automated decision split.
   - *Classification vs DSA*:
     - `automated_detection`: **Closest conceptual analogue** (both measure whether system automation initiated the detection).
     - `automated_decision`: **Not equivalent** (does not indicate whether enforcement occurred without human review).

2. **Meta / Instagram "Proactive Rate"**:
   - *Official Definition*: Percentage of actioned content detected by Meta's systems before users reported it.
   - *Denominator*: Total Content Actioned under the specific policy area on Instagram.
   - *Enforcement Stage*: **Stage A/B (Proactive Detection)**. Proactively detected content is frequently routed to human review teams; Meta does not publish an automated decision rate.
   - *Classification vs DSA*:
     - `automated_detection`: **Closest conceptual analogue** (directionally comparable indicator of proactive machine detection).
     - `automated_decision`: **Not equivalent** (does NOT measure automated enforcement without human review).

3. **TikTok "Proactive Removal Rate"**:
   - *Official Definition*: Percentage of short-form video removals identified and removed before receiving any user report.
   - *Denominator*: Total short-form videos removed for Community Guidelines violations.
   - *Enforcement Stage*: **Stage A (Proactive Detection)**. Includes both human-reviewed and automated removals.
   - *Classification vs DSA*:
     - `automated_detection`: **Closest conceptual analogue** (measures proactive system discovery prior to external user notice).
     - `automated_decision`: **Not equivalent** (measures detection timing, not decision agency).

4. **TikTok "Automated Removal Rate"**:
   - *Official Definition*: Percentage of short-form videos removed where the removal decision was executed **solely by automated systems without human review**.
   - *Denominator*: Total short-form videos removed for Community Guidelines violations (`v_auto / v_tot`).
   - *Enforcement Stage*: **Stage C (Automated Decision / Enforcement)**.
   - *Classification vs DSA*:
     - `automated_detection`: **Not equivalent** (decision-level, not detection-level).
     - `automated_decision`: **Closest conceptual analogue to DSA automated_decision**. TikTok measures the share of removed videos removed automatically without human review, whereas the DSA field is defined at the Statement-of-Reasons level. Therefore the concepts are closely related but the units and reporting systems differ.

---

## 8. Historical Context Value Analysis (Pre-September 2023)

The EU DSA Transparency Database began operations on **September 25, 2023**. Any data before that date in the DSA represents delayed backlog processing (< 0.002% of records).

Official platform transparency reports provide substantial historical depth that DSA data cannot offer:

1. **Pre-DSA Baseline Establishment (2021–2023)**:
   - Evaluates whether moderation volume shifts in 2024–2026 are genuine increases in platform enforcement or artifacts of DSA compliance reporting obligations.
   - Captures multi-year baseline trends across platforms (e.g., YouTube automated flagging consistently >90%, Meta proactive detection >90% across mature categories, and TikTok `v_auto / v_tot` rising from 14.26% in 2021Q1 to 96.74% in 2026Q1, noting that official artifacts document the metric as removals not requiring human moderator intervention without establishing the internal operational drivers of the increase).

2. **Exposure and Denominator Context**:
   - YouTube reports "Views before removal" (<1 view, 1–10 views, >10 views).
   - TikTok reports zero-view removal rates (82.2% in 2026Q1) and removal within 24 hours (94.4%).
   - Meta reports "Prevalence" estimates per policy area.
   - DSA data records only the numerator (enforcement notices) with zero platform impression data.

---

## 9. Recommended Acquisition Scope: Option A (Q1 2021 through Q1 2026)

Based on empirical source verification, **OPTION A (Q1 2021 through Q1 2026 — 21 continuous quarters)** is recommended over Option B:

### Rationale:
1. **TikTok Availability**: TikTok's official reporting currently ends at **`2026Q1`** (`2026Q2` returned 404 and is unpublished). Selecting Option B would result in a missing quarter for TikTok, undermining cross-platform parity.
2. **Temporal Alignment with DSA**: Our DSA complete-aggregate dataset extends to `2026-05-31`. Q2 2026 includes June 2026, which falls outside the DSA dataset. Comparing a complete Q2 platform quarter (April–June) to an incomplete DSA Q2 (April–May only) would introduce an asymmetric, misleading cross-source comparison.
3. **Longitudinal Alignment**: Q1 2021 through Q1 2026 spans 21 continuous calendar quarters across all three platforms. Because the EU DSA Transparency Database came into legal force on September 25, 2023, 2023Q3 serves as a partial/mixed transition quarter; this supplementary window covers 10 full pre-DSA quarters (2021Q1–2023Q2), 1 transition quarter (2023Q3), and 10 post-DSA quarters (2023Q4–2026Q1), avoiding any partial-quarter misalignment with the DSA dataset.

### Target Source Endpoints for Phase 3B:

#### A. YouTube (Q1 2021 – Q1 2026)
- **Verified Mechanism**: REST API queries to `https://transparencyreport.google.com/transparencyreport/api/v3/youtubepolicy/`
- **Target Endpoints**:
  - `videoremovalsbyreason?period={PERIOD}` (reasons 1–11)
  - `contentremovedbyuser?period={PERIOD}` (flagger type: automated vs human)
  - `totalvideoremovalsbyviews?period={PERIOD}` (view distribution)
  - `totalvideosremoved?period={PERIOD}` (total removals)
- **Local Storage Target**: `data/raw/supplementary/youtube/youtube_quarterly_metrics.json`

#### B. Instagram / Meta (Q1 2021 – Q1 2026)
- **Verified Mechanism**: Meta GraphQL endpoint `https://transparency.meta.com/api/graphql/`
  - Query: `TransparencyReportCSERRootCSVQuery` (doc_id `31742207542036840`)
- **Target Data**: Official CSV export (`CSER-2026_Q2.csv`), filtered during processing for `app = 'Instagram'` and periods `2021Q1` through `2026Q1`.
- **Target Metrics**: `Content Actioned`, `Proactive rate`, `Content Appealed`, `Content Restored with appeal`, `Prevalence`.
- **Local Storage Target**: `data/raw/supplementary/instagram/CSER-2026_Q2.csv` (preserved untouched; filtered during ETL).

#### C. TikTok (Q1 2021 – Q1 2026)
- **Verified Mechanism**: Official CDN structured dashboard payloads from `https://sf16-va.tiktokcdn.com/obj/eden-va2/zkyhviozhk_YLNJ/ljhwZthlaukjlkulzlp/2026Q1/`
- **Target Files & Variables**:
  - `2_Volume_English.html` (`window.injectedData`: `v_tot`, `v_auto`, `v_res`)
  - `3_Speed_English.html` (`window.injectedData`: `proactive`, `lt24`, `vv_data`)
  - `4_Policies_English.html` (`window.injectedData`: policy headings and rules)
- **Local Storage Target**: `data/raw/supplementary/tiktok/tiktok_quarterly_metrics.json`

---

## 10. Top 5 Methodological Warnings & Caveats

1. **Unit of Analysis Disparity**:
   - DSA measures **legal enforcement notices** (Statements of Reasons). One SoR can theoretically encompass multiple items, or multiple SoRs can apply to one multi-party item.
   - Platform reports measure **physical content units** (videos, posts, accounts). Never merge, equate, or subtract counts across sources.

2. **Geographic Incompatibility**:
   - DSA data is strictly confined to the **European Union** (27 member states).
   - Meta CSER and TikTok CGER primary reports are **global**.
   - YouTube provides country-level video counts by uploader IP, but its category breakdowns are global.

3. **Detection vs. Decision Conflation**:
   - Meta "Proactive Rate" = Automated **Detection** (system flagged content before user report; does not measure automated decision).
   - TikTok "Automated Removal Rate" = Closest conceptual analogue to DSA `automated_decision` (TikTok measures the share of removed videos removed automatically without human review, whereas the DSA field is defined at the Statement-of-Reasons level; therefore the concepts are closely related but the units and reporting systems differ).
   - DSA SoR distinguishes both via separate flags (`automated_detection` and `automated_decision`). Comparing detection rates to decision rates is methodologically invalid.

4. **Category Semantic Drift**:
   - A violation classified as "Bullying and Harassment" on Instagram may fall under "Defamation" or "Negative reputation" in DSA SoR taxonomy, or "Harassment & cyberbullying" on YouTube.
   - High-level category comparisons must rely on explicit concordance crosswalks.

5. **Impression / Prevalence Asymmetry**:
   - High removal counts do not necessarily indicate high platform risk; they may indicate aggressive automated sweeps of zero-view spam.
   - Platform reports partially mitigate this via view-at-removal buckets, whereas DSA contains zero exposure metrics.

---

## 11. Project Integration & Boundary Summary

1. **Isolated Storage**:
   - All supplementary raw files reside in `data/raw/supplementary/` and are strictly excluded from version control.
2. **Authoritative Primacy**:
   - The EU DSA Transparency Database remains the primary quantitative benchmark. Platform reports provide supplementary macro-historical baselines and exposure context only.
3. **Decoupled Processing Bridge (Phase 4)**:
   - Separate data loaders will process DSA aggregates (`src/load_dsa.py`) and supplementary quarterly reports (`src/load_supplementary.py`) without cross-contaminating datasets.

