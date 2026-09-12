# Cross-Platform Content Moderation Benchmark

> **Current Project Status: Phase 1 — Setup**  
> This repository is currently in the initial setup phase. Data acquisition, processing pipelines, metrics computation, and report generation will be implemented in subsequent phases.

---

## Overview & Problem Statement

As major digital platforms handle massive volumes of user-generated content daily, understanding how content moderation decisions are executed has become critical for Trust & Safety policy and operations. 

This project addresses the core question:
> **How does one platform's content moderation automation and enforcement behavior compare to its competitors, and where should a safety team focus its efforts as a result?**

We benchmark content moderation across three major platforms:
- **TikTok**
- **YouTube** (Google)
- **Meta** (Instagram / Facebook)

By analyzing standardized disclosures from the **EU Digital Services Act (DSA) Transparency Database** ([transparency.dsa.ec.europa.eu](https://transparency.dsa.ec.europa.eu)), all three platforms can be evaluated on an equal footing. Under DSA compliance mandates, platforms must systematically submit Statements of Reasons (SoRs) when restricting or removing content.

---

## Core Metrics

### Primary Metrics: Automation Rates
To understand the degree of human-in-the-loop oversight versus algorithmic intervention:
- **`automated_detection`**: Indicates whether automated mechanisms were used to identify the potentially infringing content before human review or action.
- **`automated_decision`**: Indicates whether the final decision and enforcement action were taken entirely through automated means without individual human intervention.

These metrics are broken down across DSA policy categories to assess platform operational reliance on automation per policy domain (e.g., hate speech, intellectual property, child safety, harassment).

### Secondary Metric: Enforcement Provisions
- **`decision_provision`**: Measures the specific enforcement actions executed by the platform (e.g., full content removal, account suspension, demonetization, or visibility restriction / algorithmic de-amplification), analyzed across categories and platforms.

---

## Planned Analysis Workflow

1. **Phase 1 — Setup (Current)**: Project structure, dependencies, git configurations, and tracking setup.
2. **Phase 2 — Data Acquisition**: Bulk-downloading Statements of Reasons (SoR) records via the `dsa-tdb` package for TikTok, YouTube, and Meta.
3. **Phase 3 — Supplementary Historical Data**: Extracting quarterly platform enforcement reports (Meta Community Standards, YouTube Community Guidelines, TikTok Community Guidelines) for longitudinal comparison outside the rolling 6-month DSA window.
4. **Phase 4 — Schema Reconciliation**: Harmonizing platform-specific categorization taxonomies with the DSA canonical taxonomy.
5. **Phase 5 — Core Metrics**: Calculating automation rates (detection vs. decision) and provision distributions per platform, category, and timeframe.
6. **Phase 6 — Analysis & Headline Findings**: In-depth exploratory analysis pinpointing notable cross-platform divergences and root causes.
7. **Phase 7 — Deliverable & Reporting**: Generating visual charts, executive writeups, and actionable Trust & Safety recommendations.

---

## Repository Structure

```text
dsa-moderation-benchmark/
├── .gitignore               # Excludes raw data, virtual environments, caches, and credentials
├── requirements.txt         # Core dependencies for analysis and visualization
├── README.md                # Project documentation and setup guide
├── data/
│   ├── raw/                 # Untouched downloaded SoR files and platform reports (gitignored)
│   │   └── README.md        # Documentation on raw data storage and reproducibility
│   └── processed/           # Cleaned, reconciled, and aggregate datasets (.gitkeep)
├── notebooks/               # Jupyter notebooks for exploratory data analysis (.gitkeep)
├── src/                     # Reusable Python modules (data download, cleaning, metrics) (.gitkeep)
└── reports/                 # Analysis writeups, exports, and benchmark charts (.gitkeep)
```

---

## Setup & How to Run

### 1. Prerequisites
- Python 3.10+ recommended
- Git

### 2. Environment Setup
Clone the repository and create a virtual environment:
```bash
git clone https://github.com/AmitejSingh1/dsa-moderation-benchmark.git
cd dsa-moderation-benchmark

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note**: Subsequent stages (data download scripts in `src/` and exploration notebooks in `notebooks/`) will be populated in Phase 2 through Phase 7.

