"""
src/load_dsa.py
Reproducible DSA aggregate data loader for Phase 5 content moderation benchmark.

Loads official EU DSA Transparency Database complete aggregates for the
primary harmonized era (2025-07-01 through 2026-05-31) and the three core
platforms (TikTok, YouTube, Instagram), enforcing strict schema and boundary
validation according to MAPPING.md.
"""

from pathlib import Path
from typing import Generator, List, Optional, Tuple
import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq

# Default paths and filtering parameters
DEFAULT_DSA_PATH = Path("data/raw/dsa_aggregates/aggregated-complete.parquet")
CORE_PLATFORMS = ("TikTok", "YouTube", "Instagram")
WINDOW_START_DATE = "2025-07-01"
WINDOW_END_DATE = "2026-05-31"

# Target month partitions in Era 2 (11 months)
TARGET_MONTHS = (
    [f"2025-{m:02d}-01" for m in range(7, 13)]
    + [f"2026-{m:02d}-01" for m in range(1, 6)]
)

# Core analytical columns required for Phase 5 metrics
REQUIRED_COLUMNS = [
    "platform_name",
    "created_at",
    "category",
    "count",
    "automated_detection",
    "automated_decision",
    "DECISION_VISIBILITY_CONTENT_REMOVED",
    "DECISION_VISIBILITY_OTHER",
    "DECISION_VISIBILITY_CONTENT_DISABLED",
    "DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED",
    "DECISION_VISIBILITY_CONTENT_DEMOTED",
    "DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED",
    "DECISION_VISIBILITY_CONTENT_LABELLED",
    "decision_account",
    "decision_provision",
    "decision_monetary",
]


def validate_dsa_source(dsa_path: Path = DEFAULT_DSA_PATH) -> None:
    """
    Validate that the DSA complete aggregate dataset exists, contains all 11
    target month partitions, and has the required schema columns.
    Raises FileNotFoundError or ValueError if validation fails.
    """
    if not dsa_path.exists():
        raise FileNotFoundError(f"DSA aggregate Parquet dataset not found at {dsa_path}")

    # Verify all 11 target month partition directories exist
    missing_partitions = []
    for m in TARGET_MONTHS:
        part_dir = dsa_path / f"created_at_month={m}"
        if not part_dir.exists() or not any(part_dir.glob("*.parquet")):
            missing_partitions.append(m)

    if missing_partitions:
        raise FileNotFoundError(
            f"Missing {len(missing_partitions)} target month partitions in {dsa_path}: "
            f"{missing_partitions}"
        )

    # Inspect schema using the first partition
    sample_file = next((dsa_path / f"created_at_month={TARGET_MONTHS[0]}").glob("*.parquet"))
    schema = pq.read_schema(sample_file)
    schema_cols = set(schema.names)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in schema_cols]
    if missing_cols:
        raise ValueError(
            f"DSA dataset schema missing required columns: {missing_cols}"
        )


def iter_harmonized_monthly_batches(
    dsa_path: Path = DEFAULT_DSA_PATH,
    columns: Optional[List[str]] = None,
) -> Generator[Tuple[str, pd.DataFrame], None, None]:
    """
    Generator yielding (month_str, pd.DataFrame) for each of the 11 target months
    (2025-07 through 2026-05) filtered to the 3 core platforms and validated
    against date boundaries and data consistency invariants.

    Parameters:
        dsa_path: Path to the partitioned parquet dataset directory.
        columns: List of columns to load. Defaults to REQUIRED_COLUMNS.

    Yields:
        (month_label, batch_df): e.g. ("2025-07", DataFrame)
    """
    validate_dsa_source(dsa_path)

    cols_to_load = columns if columns is not None else REQUIRED_COLUMNS
    dataset = ds.dataset(dsa_path, partitioning="hive")

    start_ts = pd.Timestamp(f"{WINDOW_START_DATE} 00:00:00")
    end_ts = pd.Timestamp(f"{WINDOW_END_DATE} 23:59:59.999999999")

    for month_partition in TARGET_MONTHS:
        month_label = month_partition[:7]

        # Construct pushdown filter on partition and platform
        filt = (
            (ds.field("created_at_month") == month_partition)
            & ds.field("platform_name").isin(list(CORE_PLATFORMS))
        )

        table = dataset.to_table(columns=cols_to_load, filter=filt)
        df = table.to_pandas()

        if len(df) == 0:
            raise ValueError(
                f"Unexpected empty dataset for partition {month_partition} and core platforms."
            )

        # Validate date boundaries
        if "created_at" in df.columns:
            min_ts = df["created_at"].min()
            max_ts = df["created_at"].max()
            if min_ts < start_ts or max_ts > end_ts:
                raise ValueError(
                    f"Partition {month_partition} contains timestamps outside primary window: "
                    f"min={min_ts}, max={max_ts}"
                )

        # Validate platform names
        if "platform_name" in df.columns:
            unexpected_platforms = set(df["platform_name"].unique()) - set(CORE_PLATFORMS)
            if unexpected_platforms:
                raise ValueError(
                    f"Partition {month_partition} contains unexpected platforms: {unexpected_platforms}"
                )

        # Validate weights
        if "count" in df.columns:
            if (df["count"] <= 0).any():
                raise ValueError(
                    f"Partition {month_partition} contains non-positive count values."
                )

        # Attach standard month column for easy aggregation
        df["month"] = month_label

        yield month_label, df


def load_harmonized_population(
    dsa_path: Path = DEFAULT_DSA_PATH,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Load the complete 11-month harmonized primary population into a single DataFrame.
    """
    batches = []
    for _, batch_df in iter_harmonized_monthly_batches(dsa_path=dsa_path, columns=columns):
        batches.append(batch_df)
    return pd.concat(batches, ignore_index=True)


if __name__ == "__main__":
    print(f"Validating DSA dataset at {DEFAULT_DSA_PATH}...")
    validate_dsa_source()
    print("DSA dataset validation successful.")

    total_rows = 0
    total_sors = 0
    platform_totals = {p: 0 for p in CORE_PLATFORMS}

    for month_label, batch_df in iter_harmonized_monthly_batches():
        rows = len(batch_df)
        sors = int(batch_df["count"].sum())
        total_rows += rows
        total_sors += sors
        for p, s in batch_df.groupby("platform_name")["count"].sum().items():
            platform_totals[p] += int(s)
        print(f"  [{month_label}] Loaded {rows:,} rows, {sors:,} SoRs")

    print("\nPopulation Summary:")
    print(f"  Total Rows: {total_rows:,}")
    print(f"  Total SoRs: {total_sors:,}")
    for p, s in platform_totals.items():
        print(f"    - {p}: {s:,} SoRs")

