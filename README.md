# Cross-Platform Content Moderation Benchmark

> **Current Project Status: Phase 2 — Data Acquisition (Complete)**  
> All 33 monthly complete-aggregate Parquet partitions covering the full historical window (**2023-09-25 through 2026-05-31**) have been successfully acquired and validated locally under `data/raw/dsa_aggregates/`. All raw source datasets are preserved in their original global format and excluded from Git. Subsequent phases will handle supplementary historical data, schema reconciliation, metric computation, and report generation.

---

## Overview & Problem Statement

As major digital platforms handle massive volumes of user-generated content daily, understanding how content moderation decisions are executed has become critical for Trust & Safety policy and operations. 

This project addresses the core question:
> **How does one platform's content moderation automation and enforcement behavior compare to its competitors, and where should a safety team focus its efforts as a result?**

### Core Benchmark Platforms
We benchmark content moderation across three primary services:
- **TikTok**
- **YouTube**
- **Instagram**

> **Deliberate Scope Decision**: In the EU DSA Transparency Database, platforms submit Statements of Reasons (SoRs) individually. Facebook and Threads are registered as distinct services with separate Platform UIDs (`32` and `80`). Facebook and Threads are deliberately excluded from our primary benchmark scope to focus the comparative analysis on consumer short-form video and visual sharing ecosystems, not due to lack of data availability. Instagram and Facebook are never collapsed into a generic "Meta" platform.

By analyzing standardized disclosures from the **EU Digital Services Act (DSA) Transparency Database** ([transparency.dsa.ec.europa.eu](https://transparency.dsa.ec.europa.eu)), all three platforms are evaluated on an equal footing.

---

## Core Metrics

### Primary Metrics: Automation Rates
To assess operational reliance on automation versus human review:
- **`automated_detection`**: Indicates whether automated mechanisms initially detected the flagged content.
- **`automated_decision`**: Indicates whether the final decision and enforcement action were taken entirely through automated means without individual human intervention.

### Secondary Metric: Enforcement Action Distribution
Under Article 17 of the DSA, platforms report different types of enforcement actions across multiple distinct schema fields:
- **`DECISION_VISIBILITY_*` flags**: Content-level actions (e.g., content removal, disablement, demotion/de-amplification, age restriction, labeling).
- **`decision_account`**: Account-level actions (e.g., account suspension, account termination).
- **`decision_monetary`**: Financial actions (e.g., demonetization, suspension of monetary benefits).
- **`decision_provision`**: Service-level restrictions under Article 17(1)(c) (e.g., suspension or termination of service provision).

> **Methodological Note on Enforcement Metrics**:  
> In the raw DSA schema, `decision_provision` specifically captures service termination/suspension and is null for the vast majority of individual content-level moderation actions (which are recorded under `DECISION_VISIBILITY_*`). Therefore, `decision_provision` alone does not represent overall enforcement. In Phase 5, the processing pipeline will construct a consolidated enforcement-action dimension combining visibility, account, monetary, and service provision actions before comparing enforcement distributions across platforms.

---

## Data Acquisition & Coverage

- **Data Source**: EU DSA Transparency Database ([transparency.dsa.ec.europa.eu](https://transparency.dsa.ec.europa.eu)).
- **Acquisition Format**: Official complete aggregated Parquet archives (`aggregated-complete`) downloaded via `dsa-tdb`.
- **Historical Source Coverage**: **2023-09-25 through 2026-05-31** (inception of the DSA Transparency Database through the latest available aggregate dump).
- **Partitions Acquired**: **33 consecutive monthly partitions** (2023-09 through 2026-05), verified with zero missing months.
- **Primary Comparable Analysis Window**: **2025-07-01 through 2026-05-31** (an **11-month period** under the harmonized reporting schema).
- **Core Benchmark Services**: TikTok, YouTube, Instagram (present across all 33 monthly partitions).
- **Raw Data Integrity Policy**: Official aggregate downloads are generated globally across all platforms and are preserved completely unchanged under `data/raw/dsa_aggregates/` (~5.15 GB local storage). Raw datasets are strictly excluded from Git via `.gitignore`. Platform filtering will be executed downstream during Phase 5 processing.

---

## DSA Schema Transition & Analysis Windows

The European Commission introduced a major reporting and submission schema revision taking effect on **2025-07-01**. To maintain methodological rigor, records from the legacy and harmonized schema eras are tracked separately:

1. **Primary Analysis Window (Harmonized Schema Era)**:
   - **Coverage**: **2025-07-01 through 2026-05-31** (an **11-month period**).
   - Core cross-platform comparisons in Phases 5 and 6 focus exclusively on this window where reporting fields are fully harmonized.
2. **Supplementary Historical Context (Legacy Schema Era)**:
   - **Coverage**: **2023-09-25 through 2025-06-30** (22 months).
   - Preserved locally as supplementary historical context; not blended directly into the primary comparative benchmark without explicit schema reconciliation.
3. **Conceptual Distinction: `created_at` vs. `application_date`**:
   - **`created_at`**: The timestamp when the Statement of Reasons was submitted and ingested into the DSA database. It represents submission timing and governs monthly source partitioning, schema-era classification (`created_at >= 2025-07-01`), and membership in the primary analysis window.
   - **`application_date`**: The date when the moderation action was applied by the platform to the content or account.

---

## Data Quality & Application Date QA Note

A comprehensive diagnostic of `application_date` across all 33 downloaded monthly partitions for the three core benchmark services confirmed high temporal data quality:
- **TikTok**: **0** future-dated represented SoRs (`application_date > 2026-05-31`); **47,201** SoRs (**0.00191%**) have `application_date < 2023-09-25`.
- **YouTube**: **0** future-dated represented SoRs; **0** SoRs (**0.00000%**) before 2023-09-25.
- **Instagram**: **0** future-dated represented SoRs; **688** SoRs (**0.00029%**) have `application_date < 2023-09-25`.

> **Key Takeaway**:  
> Out-of-window dates for the core services are negligible (< 0.002% overall and 0% future-dated). These records are preserved intact in `data/raw/` without alteration and will be handled explicitly during downstream validation and processing. Membership in the harmonized comparative analysis window continues to be determined strictly by `created_at`.

---

## Planned Analysis Workflow

1. **Phase 1 — Setup (Complete)**: Repository structure, dependencies, git configurations, and tracking setup.
2. **Phase 2 — Data Acquisition (Complete)**: Bulk acquisition and QA of official DSA complete aggregated Parquet files via `dsa-tdb` covering 33 months (2023-09-25 to 2026-05-31).
3. **Phase 3 — Supplementary Historical Data (Next)**: Extracting quarterly platform enforcement reports (Meta Community Standards, YouTube Community Guidelines, TikTok Community Guidelines) for longitudinal comparison.
4. **Phase 4 — Schema Reconciliation**: Harmonizing platform-specific categorization taxonomies with the DSA canonical taxonomy.
5. **Phase 5 — Core Metrics**: Calculating automation rates and consolidated enforcement-action distributions for the harmonized era (2025-07-01 to 2026-05-31).
6. **Phase 6 — Analysis & Headline Findings**: In-depth exploratory analysis pinpointing notable cross-platform divergences.
7. **Phase 7 — Deliverable & Reporting**: Generating visual charts, executive writeups, and actionable Trust & Safety recommendations.

---

## Repository Structure

```text
dsa-moderation-benchmark/
├── .gitignore               # Excludes raw data, virtual environments, caches, and credentials
├── requirements.txt         # Core dependencies with EC package registry URL
├── README.md                # Project documentation and setup guide
├── data/
│   ├── raw/                 # Untouched downloaded SoR files and platform reports (gitignored)
│   │   ├── dsa_aggregates/  # Official DSA pre-computed complete aggregates (Parquet)
│   │   └── README.md        # Documentation on raw data storage and reproducibility
│   └── processed/           # Cleaned, reconciled, and aggregate datasets (.gitkeep)
├── notebooks/               # Jupyter notebooks for exploratory data analysis (.gitkeep)
├── src/
│   ├── download_dsa.py      # DSA data acquisition module with strict safety guards
│   └── .gitkeep             # Reusable Python modules
└── reports/                 # Analysis writeups, exports, and benchmark charts (.gitkeep)
```

---

## Setup & How to Run

### 1. Prerequisites
- Python 3.10+ recommended
- Git

### 2. Environment Setup & Dependency Installation
Clone the repository and create a virtual environment:
```bash
git clone https://github.com/AmitejSingh1/dsa-moderation-benchmark.git
cd dsa-moderation-benchmark

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note on `dsa-tdb` Package Registry**:  
> The official `dsa-tdb` package is hosted on the European Commission's GitLab package registry rather than standard PyPI. `requirements.txt` includes `--extra-index-url https://code.europa.eu/api/v4/projects/943/packages/pypi/simple` at the top, allowing standard `pip install -r requirements.txt` to seamlessly locate and install the package without manual registry configuration.

### 3. Data Acquisition
The data acquisition script enforces safety guards requiring explicit dates:
```bash
# Dry run to inspect files without downloading:
python src/download_dsa.py --from-date 2023-09-25 --to-date 2026-05-31 --dry-run

# Run full acquisition (skips already-downloaded partitions):
python src/download_dsa.py --from-date 2023-09-25 --to-date 2026-05-31
```
