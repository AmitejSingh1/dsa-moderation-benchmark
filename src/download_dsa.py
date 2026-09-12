"""
DSA Transparency Database Data Acquisition Module.

This script manages downloading and extracting Statement of Reasons (SoR) aggregated
data from the EU DSA Transparency Database repository using `dsa-tdb`.

SAFETY GUARDS:
1. Explicit `--from-date` and `--to-date` CLI arguments are mandatory.
   Running without explicit dates will terminate immediately without downloading.
2. The output directory is strictly restricted to `data/raw/` to prevent accidental
   writes to other project folders or root directories.
3. Existing, valid monthly partitions are detected and reused to prevent unnecessary
   re-downloads.
4. `--dry-run` performs zero dataset network downloads.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from dsa_tdb.fetch import fetch_aggregate_month
from dsa_tdb.types import (
    ADVANCED_FILE_AGGREGATE_FILE_PATTERN,
    TDB_agg_data_format,
    TDB_dailyDumpsVersion,
)

# Core benchmark services for primary analysis
CORE_BENCHMARK_SERVICES = ["tiktok", "youtube", "instagram"]


def validate_date(date_str: str) -> datetime:
    """Validate and parse a YYYY-MM-DD date string."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format '{date_str}'. Expected format is YYYY-MM-DD (e.g., 2026-01-01)."
        )


def get_month_range(from_date_str: str, to_date_str: str) -> List[str]:
    """Return a sorted list of first-of-month strings (YYYY-MM-01) covering the date range."""
    start_dt = validate_date(from_date_str)
    end_dt = validate_date(to_date_str)

    if start_dt > end_dt:
        raise ValueError(
            f"Start date (--from-date: {from_date_str}) cannot be after end date (--to-date: {to_date_str})."
        )

    months = []
    curr = datetime(start_dt.year, start_dt.month, 1)
    end_month = datetime(end_dt.year, end_dt.month, 1)

    while curr <= end_month:
        months.append(curr.strftime("%Y-%m-01"))
        if curr.month == 12:
            curr = datetime(curr.year + 1, 1, 1)
        else:
            curr = datetime(curr.year, curr.month + 1, 1)

    return months


def validate_output_directory(output_dir: Path, repo_root: Path) -> Path:
    """Ensure the output directory resides strictly within data/raw/."""
    resolved_dir = (repo_root / output_dir).resolve()
    raw_dir = (repo_root / "data" / "raw").resolve()

    try:
        resolved_dir.relative_to(raw_dir)
    except ValueError:
        raise ValueError(
            f"Safety Violation: Output directory '{resolved_dir}' must be inside '{raw_dir}'."
        )

    return resolved_dir


def check_existing_month(
    output_dir: Path, month_str: str, aggregation: str
) -> bool:
    """
    Check if a valid partitioned parquet dataset folder already exists for this month.
    """
    partition_folder = (
        output_dir
        / f"aggregated-{aggregation}.parquet"
        / f"created_at_month={month_str}"
    )
    if partition_folder.exists() and any(partition_folder.glob("*.parquet")):
        return True

    zip_file = (
        output_dir
        / ADVANCED_FILE_AGGREGATE_FILE_PATTERN.format(
            aggregation=aggregation,
            month=month_str,
            dump_format="parquet",
            extension="zip",
        )
    )
    if zip_file.exists() and zip_file.stat().st_size > 0:
        return True

    return False


def plan_download(
    from_date: str,
    to_date: str,
    output_dir: Path,
    aggregation: str = "complete",
    dump_format: str = "parquet",
    force: bool = False,
) -> Tuple[List[str], List[str]]:
    """Determine which months need downloading vs. which already exist locally."""
    months = get_month_range(from_date, to_date)
    to_download = []
    existing = []

    for m in months:
        if not force and check_existing_month(output_dir, m, aggregation):
            existing.append(m)
        else:
            to_download.append(m)

    return months, to_download, existing


def execute_download(
    from_date: str,
    to_date: str,
    output_dir: Path,
    aggregation: str = "complete",
    dump_format: str = "parquet",
    force: bool = False,
    dry_run: bool = False,
) -> None:
    """Execute or simulate downloading aggregated dataset files."""
    months, to_download, existing = plan_download(
        from_date=from_date,
        to_date=to_date,
        output_dir=output_dir,
        aggregation=aggregation,
        dump_format=dump_format,
        force=force,
    )

    print("=" * 60)
    print("DSA TRANSPARENCY DATABASE ACQUISITION PLAN")
    print("=" * 60)
    print(f"Date Range Requested : {from_date} to {to_date}")
    print(f"Total Months Covered : {len(months)}")
    print(f"Aggregation Level    : {aggregation}")
    print(f"Data Format          : {dump_format}")
    print(f"Target Directory     : {output_dir}")
    print(f"Existing Local Files : {len(existing)} month(s)")
    print(f"To Be Downloaded     : {len(to_download)} month(s)")
    print("-" * 60)
    print(f"Core Benchmark Scope : {', '.join(CORE_BENCHMARK_SERVICES)}")
    print("  * Note: Official aggregate downloads are global.")
    print("  * Raw files will be preserved intact under data/raw/.")
    print("  * Service filtering will be applied during Phase 5 processing.")
    print("-" * 60)

    for i, m in enumerate(months, 1):
        status = "ALREADY EXISTS" if m in existing else "QUEUED FOR DOWNLOAD"
        fname = ADVANCED_FILE_AGGREGATE_FILE_PATTERN.format(
            aggregation=aggregation,
            month=m,
            dump_format=dump_format,
            extension="zip",
        )
        print(f"  [{i:02d}/{len(months):02d}] {m} -> {fname} [{status}]")

    print("=" * 60)

    if dry_run:
        print("\n[DRY RUN COMPLETE] Zero dataset network requests were executed.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    format_enum = (
        TDB_agg_data_format.parquet
        if dump_format == "parquet"
        else TDB_agg_data_format.csv
    )

    failed_months = []
    for m in to_download:
        print(f"\nDownloading and extracting month {m}...")
        success = False
        for attempt in range(1, 3):
            try:
                res = fetch_aggregate_month(
                    out_folder=str(output_dir),
                    platform="global",
                    aggregation=aggregation,
                    month=m,
                    version=TDB_dailyDumpsVersion.full,
                    dump_format=format_enum,
                    unzip=True,
                    with_aux_files=True,
                )
                if res and check_existing_month(output_dir, m, aggregation):
                    print(f"Successfully unpacked {m}.")
                    success = True
                    break
                else:
                    print(f"Attempt {attempt} returned empty or incomplete for {m}.")
            except Exception as e:
                print(f"Attempt {attempt} failed for {m} with error: {e}")

        if not success:
            failed_months.append(m)
            print(f"[FAILED] Failed to acquire month {m} after retries.")

    if failed_months:
        raise RuntimeError(
            f"Data acquisition incomplete. Failed months: {failed_months}"
        )

    print("\nAcquisition completed successfully for all requested months.")


def main():
    repo_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Acquire official EU DSA Transparency Database aggregated Parquet files."
    )
    parser.add_argument(
        "--from-date",
        type=str,
        required=True,
        help="Start date in YYYY-MM-DD format (required)",
    )
    parser.add_argument(
        "--to-date",
        type=str,
        required=True,
        help="End date in YYYY-MM-DD format (required)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/dsa_aggregates"),
        help="Output subdirectory inside data/raw/ (default: data/raw/dsa_aggregates)",
    )
    parser.add_argument(
        "--aggregation",
        type=str,
        choices=["complete", "simple"],
        default="complete",
        help="Aggregation configuration (default: complete)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["parquet", "csv"],
        default="parquet",
        help="File format (default: parquet)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if files already exist locally",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the acquisition plan and print files without downloading",
    )

    args = parser.parse_args()

    try:
        valid_output_dir = validate_output_directory(args.output_dir, repo_root)
        execute_download(
            from_date=args.from_date,
            to_date=args.to_date,
            output_dir=valid_output_dir,
            aggregation=args.aggregation,
            dump_format=args.format,
            force=args.force,
            dry_run=args.dry_run,
        )
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
