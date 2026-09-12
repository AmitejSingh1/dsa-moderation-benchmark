# Supplementary Historical Data Manifest

**EU DSA Moderation Benchmark — Phase 3B Deliverable**  
**Acquisition Window**: 2021Q1 through 2026Q1 inclusive (21 continuous calendar quarters)  
**Status**: Verified Complete  
**Total Supplementary Storage**: ~928 KB (90 source files)  
**Storage Path**: `data/raw/supplementary/` *(strictly excluded from version control)*  

---

## 1. Overview & Methodological Boundary

This manifest documents the official, first-party supplementary transparency datasets acquired for the three core benchmark services: **YouTube**, **Instagram (Meta)**, and **TikTok**.

### Fundamental Analytical Boundary:
1. **Separation of Layers**: Supplementary platform datasets are **never merged or added** to the EU DSA Statements of Reasons (SoR) database.
2. **Distinct Analytical Functions**:
   - **EU DSA Transparency Database**: Primary, harmonized, event-level legal record of moderation actions within the European Union (late September 2023 onward).
   - **Supplementary Platform Reports**: External macro-historical baselines, automation adoption trajectories, and exposure/viewership context (2021 to 2026).
3. **Temporal Alignment**:
   - The approved supplementary window spans **2021Q1 through 2026Q1** (21 quarters).
   - *Note on baseline comparison*: The EU DSA Transparency Database came into legal force on **September 25, 2023** (late in 2023Q3). Consequently, 2023Q3 represents a partial/mixed transition quarter in the DSA data. The supplementary dataset covers 10 full pre-DSA quarters (2021Q1 through 2023Q2), 1 transition quarter (2023Q3), and 10 post-DSA quarters (2023Q4 through 2026Q1).

---

## 2. Platform Manifests

### A. YouTube

| Dimension | Details |
| :--- | :--- |
| **Service** | YouTube (Google LLC / Alphabet Inc.) |
| **Official Source** | Google Transparency Report — YouTube Community Guidelines Transparency Report |
| **Base Endpoint** | `https://transparencyreport.google.com/transparencyreport/api/v3/youtubepolicy/` |
| **Retrieval Mechanism** | Direct HTTP GET queries to verified public REST API JSON endpoints |
| **Reporting Periods** | **2021Q1 through 2026Q1** (21 continuous quarters; 100% complete) |
| **Raw Storage Architecture** | `data/raw/supplementary/youtube/<QUARTER>/<ENDPOINT>.json` |
| **Number of Raw Files** | **84 files** (21 quarters × 4 endpoints) |
| **Raw Format** | Raw JSON payloads (preserving official Google XSSI prefix `)]}'\n`) |
| **Total Disk Usage** | ~8.2 KB |
| **Retrieval Date** | September 2026 |

#### Endpoints Acquired per Quarter:
1. `videoremovalsbyreason.json`: Removal counts and shares by Community Guidelines policy reason (IDs 1–11).
2. `contentremovedbyuser.json`: Breakdown of video removals by first detection source (Automated Flagging [ID 2], Individual Trusted Flagger [ID 3], Government Agency [ID 4], User [ID 5], NGO [ID 6], Organization [ID 7]).
3. `totalvideoremovalsbyviews.json`: Breakdown by views received prior to removal (0 views, 1–10 views, >10 views).
4. `totalvideosremoved.json`: Total short-form and long-form video removals (`flagger_type=all`).

#### Known Limitations & Invariants:
- **Detection vs Decision**: YouTube's automated metric measures *Automated Flagging* (detection stage). The final removal decision may have been executed by human review or automated systems; YouTube does not publish an automated decision split.
- **Geographic Scope**: Removals by policy and detection source are reported as global aggregates.
- **Taxonomy Revisions**: Reason 10 (*Suicide, self-harm, or eating disorders*) was added in 2023Q1; Reason 11 (*Violent or graphic*) appeared in recent quarters.

---

### B. Instagram (Meta)

| Dimension | Details |
| :--- | :--- |
| **Service** | Instagram (Meta Platforms, Inc.) |
| **Official Source** | Meta Transparency Center — Community Standards Enforcement Report (CSER) |
| **Official URL** | `https://transparency.meta.com/reports/community-standards-enforcement/` |
| **Retrieval Mechanism** | Official GraphQL Query (`TransparencyReportCSERRootCSVQuery`, Doc ID `31742207542036840`) with dynamic session token extraction |
| **Official File Name** | `CSER-2026_Q2.csv` (Preserved completely untouched in raw storage) |
| **Reporting Periods** | **2021Q1 through 2026Q1** (Instagram rows verified complete; full file spans 2017Q4–2026Q2) |
| **Raw Storage Path** | `data/raw/supplementary/instagram/CSER-2026_Q2.csv` |
| **Number of Raw Files** | **1 file** (5,409 rows total: 2,527 Instagram rows, 2,882 Facebook rows) |
| **Raw Format** | Untouched CSV (`app,policy_area,metric,period,value`) |
| **Total Disk Usage** | ~423 KB |
| **Retrieval Date** | September 2026 |

#### Relevant Metrics Contained:
- `Content Actioned`: Total pieces of content (posts, reels, stories, comments) actioned by policy area.
- `Proactive rate`: Percentage of actioned content detected by Meta before being reported by users.
- `Content Appealed`, `Content Restored with appeal`, `Content Restored without appeal`: Redress and restoration volumes.
- `Prevalence`, `Lowerbound Prevalence`, `Upperbound Prevalence`: Estimated share of views that violated policy.

#### Known Limitations & Invariants:
- **Preservation of Untouched Source**: In accordance with raw storage rules, Facebook data is retained in the raw file and will be filtered strictly at `app == 'Instagram'` during ETL processing.
- **Proactive Rate Definition**: Meta's proactive rate measures *Automated Detection*. Proactively flagged content is frequently routed to human review teams; Meta does not publish an automated decision rate.
- **Policy Taxonomy Splits**: In 2021Q1, child exploitation was reported under `Child Nudity & Sexual Exploitation`; starting in 2021Q2, Meta split this into `Child Endangerment: Sexual Exploitation` and `Child Endangerment: Nudity and Physical Abuse`. `Violence and Incitement` reporting begins in 2021Q3. `Spam` reporting on Instagram begins in 2024Q3.

---

### C. TikTok

| Dimension | Details |
| :--- | :--- |
| **Service** | TikTok (ByteDance Ltd.) |
| **Official Source** | TikTok Transparency Center — Community Guidelines Enforcement Reports |
| **Official Source Path** | `https://sf16-va.tiktokcdn.com/obj/eden-va2/zkyhviozhk_YLNJ/ljhwZthlaukjlkulzlp/2026Q1/` |
| **Retrieval Mechanism** | Direct HTTP retrieval of official published dashboard HTML/JS artifacts containing `window.injectedData` |
| **Reporting Periods** | **2021Q1 through 2026Q1** (21 continuous quarters; 100% complete) |
| **Raw Storage Architecture** | `data/raw/supplementary/tiktok/<ARTIFACT_NAME>` |
| **Number of Raw Files** | **5 artifacts** (`2_Volume_English.html`, `3_Speed_English.html`, `4_Policies_English.html`, `1_Prevalence_English.html`, `5_Geography_English.html`) |
| **Raw Format** | Untouched HTML/JS dashboard artifacts containing structured JSON in `window.injectedData` |
| **Total Disk Usage** | ~446 KB |
| **Retrieval Date** | September 2026 |

#### Relevant Metrics Contained:
- `v_tot`: Total short-form video removals per quarter.
- `v_auto`: Videos removed solely by automated systems without human review.
- `v_auto / v_tot`: **Automated Removal Rate** (moderation decision without human review).
- `proactive`: **Proactive Removal Rate** (percentage removed before user report).
- `lt24`: Removal rate within 24 hours of posting.
- `vv_data`: Removal distribution across view volume tiers (including zero-view removals).
- `v_res`: Videos restored upon appeal.
- `a_u13` / `a_fake`: Under-13 and fake accounts terminated.

#### Known Limitations & Invariants:
- **Published Boundary**: TikTok publishes on a quarterly lag; `2026Q1` is the latest officially published quarter (`2026Q2` is unpublished).
- **Closest Conceptual Analogue to DSA automated_decision**: TikTok's automated removal rate (`v_auto / v_tot`) serves as the closest conceptual analogue to DSA `automated_decision`. TikTok measures the share of removed videos removed automatically without human review, whereas the DSA field is defined at the Statement-of-Reasons level. Therefore the concepts are closely related but the units and reporting systems differ.

---

## 3. Cross-Source 21-Quarter Coverage Matrix (2021Q1 – 2026Q1)

All 21 calendar quarters are 100% covered across all three platforms:

| Quarter | YouTube Available | Instagram Available | TikTok Available | Alignment Status |
| :---: | :---: | :---: | :---: | :---: |
| **2021Q1** | YES | YES | YES | 100% Aligned |
| **2021Q2** | YES | YES | YES | 100% Aligned |
| **2021Q3** | YES | YES | YES | 100% Aligned |
| **2021Q4** | YES | YES | YES | 100% Aligned |
| **2022Q1** | YES | YES | YES | 100% Aligned |
| **2022Q2** | YES | YES | YES | 100% Aligned |
| **2022Q3** | YES | YES | YES | 100% Aligned |
| **2022Q4** | YES | YES | YES | 100% Aligned |
| **2023Q1** | YES | YES | YES | 100% Aligned |
| **2023Q2** | YES | YES | YES | 100% Aligned |
| **2023Q3** | YES | YES | YES | 100% Aligned *(DSA Transition Quarter)* |
| **2023Q4** | YES | YES | YES | 100% Aligned *(First full post-DSA quarter)* |
| **2024Q1** | YES | YES | YES | 100% Aligned |
| **2024Q2** | YES | YES | YES | 100% Aligned |
| **2024Q3** | YES | YES | YES | 100% Aligned |
| **2024Q4** | YES | YES | YES | 100% Aligned |
| **2025Q1** | YES | YES | YES | 100% Aligned |
| **2025Q2** | YES | YES | YES | 100% Aligned |
| **2025Q3** | YES | YES | YES | 100% Aligned *(DSA Harmonized Schema Era)* |
| **2025Q4** | YES | YES | YES | 100% Aligned *(DSA Harmonized Schema Era)* |
| **2026Q1** | YES | YES | YES | 100% Aligned *(DSA Harmonized Schema Era)* |

---

## 4. Metric-Level Evolution & Missingness Details

| Service | Metric Group | Continuous 21-Quarter Availability | Notes & Historical Adjustments |
| :--- | :--- | :--- | :--- |
| **YouTube** | Total Removals | 21/21 Quarters (100%) | Steady ~4.5M to ~9.8M videos/quarter. |
| **YouTube** | Flagger Source | 21/21 Quarters (100%) | Automated flagging represents >90% of removals across the series. |
| **YouTube** | View Distribution | 21/21 Quarters (100%) | Buckets: 0 views, 1–10 views, >10 views. |
| **YouTube** | Policy Reasons | 21/21 Quarters (100%) | 9 categories through 2022; suicide/eating disorders added 2023Q1; violent/graphic re-indexed in 2026Q1. |
| **Instagram** | Core Actioned | 21/21 Quarters (100%) | 8 core policy areas present for all 21 quarters. |
| **Instagram** | Child Safety | 20/21 Quarters (split) | Split from single category into 2 sub-policies in 2021Q2. |
| **Instagram** | Violence & Incitement | 19/21 Quarters (90.5%) | First reported in 2021Q3. |
| **Instagram** | Spam (Instagram) | 7/21 Quarters (33.3%) | First reported in 2024Q3 (previously Facebook only). |
| **Instagram** | Criminal Orgs | 1/21 Quarters (4.8%) | First reported in 2026Q1. |
| **TikTok** | Total & Auto Removals | 21/21 Quarters (100%) | Continuous time series; automated removal volume grows from 8.8M (14.3%) in 2021Q1 to 178.0M (96.7%) in 2026Q1. |
| **TikTok** | Proactive & <24h Rates | 21/21 Quarters (100%) | Proactive rate exceeds 91% in 2021Q1 and reaches 99.3% in 2026Q1. |
| **TikTok** | Zero-View Removals | 10/21 Quarters (granular) | Detailed view volume distributions available for recent quarters (82.2% at 0 views in 2026Q1). |

