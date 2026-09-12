# Raw Data Directory

This directory contains untouched, original source datasets downloaded for the Cross-Platform Content Moderation Benchmark project, specifically:

- Daily Statement of Reasons (SoR) files downloaded via the `dsa-tdb` package from the EU Digital Services Act (DSA) Transparency Database (`transparency.dsa.ec.europa.eu`) for TikTok, YouTube, and Meta (Instagram / Facebook).
- Supplementary raw data or historical platform transparency reports (Community Standards / Guidelines Enforcement reports).

## Data Exclusion Notice

All raw data files in this directory are excluded from Git version control (via `.gitignore`) due to their large file size (potentially gigabytes of CSV/Parquet records) and because they are programmatically reproducible using the data acquisition scripts in this repository.

Only this `README.md` is tracked in version control.

