"""
Acquisition Pipeline for Supplementary Platform Transparency Reports
====================================================================
Reproducible data acquisition script for official transparency reporting:
  - YouTube: Google Transparency Report Policy API (2021Q1 - 2026Q1)
  - Instagram: Meta Transparency Center CSER Export (CSER-2026_Q2.csv)
  - TikTok: TikTok Transparency Center CDN Artifacts (2021Q1 - 2026Q1)

Scope: Supplementary historical context for the EU DSA Moderation Benchmark.
Raw data is preserved untransformed and is strictly excluded from version control.

Usage:
  python src/download_supplementary.py --platform youtube [--start-quarter 2021Q1] [--end-quarter 2026Q1]
  python src/download_supplementary.py --platform instagram
  python src/download_supplementary.py --platform tiktok
  python src/download_supplementary.py --platform all
"""

import argparse
import csv
import datetime
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("download_supplementary")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0


def fetch_with_retry(
    req: urllib.request.Request,
    retries: int = MAX_RETRIES,
    backoff: float = RETRY_BACKOFF,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """Execute an HTTP request with exponential backoff on transient errors."""
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                sleep_sec = backoff**attempt
                logger.warning(
                    f"HTTP {e.code} on attempt {attempt}/{retries}. Retrying in {sleep_sec:.1f}s..."
                )
                time.sleep(sleep_sec)
            else:
                logger.error(f"HTTP Error {e.code}: {e.reason} for {req.full_url}")
                raise
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                sleep_sec = backoff**attempt
                logger.warning(
                    f"Network error ({e}) on attempt {attempt}/{retries}. Retrying in {sleep_sec:.1f}s..."
                )
                time.sleep(sleep_sec)
            else:
                logger.error(f"Network error failed after {retries} attempts: {e}")
                raise
    raise RuntimeError(f"Failed to fetch {req.full_url} after {retries} attempts")


def generate_quarters(start_q: str, end_q: str) -> List[str]:
    """Generate quarterly strings from start_q to end_q inclusive (e.g., 2021Q1 to 2026Q1)."""
    start_year, start_quarter = int(start_q[:4]), int(start_q[-1])
    end_year, end_quarter = int(end_q[:4]), int(end_q[-1])

    quarters = []
    y = start_year
    q = start_quarter
    while (y < end_year) or (y == end_year and q <= end_quarter):
        quarters.append(f"{y}Q{q}")
        q += 1
        if q > 4:
            q = 1
            y += 1
    return quarters


# ==============================================================================
# 1. YOUTUBE ACQUISITION
# ==============================================================================
YOUTUBE_BASE_URL = "https://transparencyreport.google.com/transparencyreport/api/v3/youtubepolicy/"
YOUTUBE_ENDPOINTS = [
    "videoremovalsbyreason",
    "contentremovedbyuser",
    "totalvideoremovalsbyviews",
    "totalvideosremoved",
]


def download_youtube(
    output_dir: str,
    start_quarter: str = "2021Q1",
    end_quarter: str = "2026Q1",
    force: bool = False,
) -> List[Dict[str, Any]]:
    """Download raw YouTube Transparency Report API responses per quarter and endpoint."""
    quarters = generate_quarters(start_quarter, end_quarter)
    logger.info(
        f"Starting YouTube acquisition for {len(quarters)} quarters ({start_quarter} to {end_quarter})..."
    )

    manifest_entries = []
    os.makedirs(output_dir, exist_ok=True)

    for q in quarters:
        q_dir = os.path.join(output_dir, q)
        os.makedirs(q_dir, exist_ok=True)

        for ep in YOUTUBE_ENDPOINTS:
            filename = f"{ep}.json"
            filepath = os.path.join(q_dir, filename)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 0 and not force:
                logger.debug(f"[YouTube] Skipping existing file: {q}/{filename}")
                manifest_entries.append({
                    "platform": "youtube",
                    "quarter": q,
                    "endpoint": ep,
                    "filepath": os.path.relpath(filepath).replace("\\", "/"),
                    "status": "existing",
                    "size_bytes": os.path.getsize(filepath),
                })
                continue

            params = {'period': q}
            if ep == "totalvideosremoved":
                params['flagger_type'] = 'all'
            query_url = f"{YOUTUBE_BASE_URL}{ep}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(query_url, headers={"User-Agent": USER_AGENT})

            try:
                raw_bytes = fetch_with_retry(req)
                # Verify parseability (handling Google XSSI prefix )]}')
                text_content = raw_bytes.decode("utf-8", errors="ignore")
                json_str = text_content
                if json_str.startswith(")]}'"):
                    json_str = json_str[4:].strip()
                _ = json.loads(json_str)

                # Save raw untouched response bytes
                with open(filepath, "wb") as f:
                    f.write(raw_bytes)

                size = os.path.getsize(filepath)
                logger.info(f"[YouTube] Acquired {q}/{filename} ({size} bytes)")
                manifest_entries.append({
                    "platform": "youtube",
                    "quarter": q,
                    "endpoint": ep,
                    "filepath": os.path.relpath(filepath).replace("\\", "/"),
                    "status": "downloaded",
                    "size_bytes": size,
                    "retrieval_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                })
            except Exception as e:
                logger.error(f"[YouTube] Failed {q}/{ep}: {e}")
                manifest_entries.append({
                    "platform": "youtube",
                    "quarter": q,
                    "endpoint": ep,
                    "filepath": os.path.relpath(filepath).replace("\\", "/"),
                    "status": f"failed: {e}",
                    "size_bytes": 0,
                })

    return manifest_entries


# ==============================================================================
# 2. INSTAGRAM / META ACQUISITION
# ==============================================================================
META_PAGE_URL = "https://transparency.meta.com/reports/community-standards-enforcement/"
META_GRAPHQL_URL = "https://transparency.meta.com/api/graphql/"
META_DOC_ID = "31742207542036840"
META_FRIENDLY_NAME = "TransparencyReportCSERRootCSVQuery"


def get_meta_lsd_token() -> str:
    """Dynamically fetch the live LSD token from the Meta Transparency Center page."""
    logger.info("Fetching Meta page to extract dynamic LSD token...")
    req = urllib.request.Request(META_PAGE_URL, headers={"User-Agent": USER_AGENT})
    html = fetch_with_retry(req).decode("utf-8", errors="ignore")

    # Match ["LSD",[],{"token":"..."}]
    matches = re.findall(r'\["LSD",\[\],\{"token":"([^"]+)"\}', html)
    if matches:
        token = matches[0]
        logger.info(f"Dynamically extracted live LSD token (length {len(token)})")
        return token

    # Fallback to any "lsd":"..." or name="lsd" value
    fallback = re.findall(r'name=["\']lsd["\']\s+value=["\']([^"\']+)["\']', html)
    if fallback:
        logger.info(f"Extracted fallback LSD token: {fallback[0]}")
        return fallback[0]

    raise RuntimeError("Could not find LSD token in Meta Transparency Center page HTML")


def download_instagram(output_dir: str, force: bool = False) -> List[Dict[str, Any]]:
    """Download official consolidated Meta CSER CSV via official GraphQL query."""
    os.makedirs(output_dir, exist_ok=True)
    target_filename = "CSER-2026_Q2.csv"
    target_filepath = os.path.join(output_dir, target_filename)

    if os.path.exists(target_filepath) and os.path.getsize(target_filepath) > 0 and not force:
        logger.info(f"[Meta/Instagram] Skipping existing file: {target_filename}")
        return [{
            "platform": "instagram",
            "file": target_filename,
            "filepath": os.path.relpath(target_filepath).replace("\\", "/"),
            "status": "existing",
            "size_bytes": os.path.getsize(target_filepath),
        }]

    lsd = get_meta_lsd_token()
    payload = urllib.parse.urlencode({
        "lsd": lsd,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": META_FRIENDLY_NAME,
        "variables": "{}",
        "server_timestamps": "true",
        "doc_id": META_DOC_ID,
    }).encode("utf-8")

    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://transparency.meta.com",
        "Referer": META_PAGE_URL,
        "X-FB-Friendly-Name": META_FRIENDLY_NAME,
        "X-FB-LSD": lsd,
    }

    req = urllib.request.Request(META_GRAPHQL_URL, data=payload, headers=headers)
    logger.info(f"Querying Meta GraphQL endpoint for {META_FRIENDLY_NAME} (doc_id {META_DOC_ID})...")

    raw_response = fetch_with_retry(req)
    res_data = json.loads(raw_response.decode("utf-8", errors="ignore"))

    if "data" not in res_data or not res_data["data"] or "csv" not in res_data["data"]:
        raise RuntimeError(f"Invalid GraphQL response structure from Meta: {str(res_data)[:200]}")

    csv_node = res_data["data"]["csv"]
    official_filename = csv_node.get("filename", target_filename)
    raw_content = csv_node.get("content", "")

    # Reconstruct exact CSV text (handling JSON escaping \\n -> \n, \\" -> ")
    normalized_content = raw_content.replace("\\r\\n", "\n").replace("\\n", "\n").replace('\\"', '"')

    # Basic integrity validation
    lines = [l for l in normalized_content.split("\n") if l.strip()]
    if len(lines) < 100 or "app" not in lines[0]:
        raise ValueError(f"Extracted CSV appears malformed or truncated ({len(lines)} lines)")

    with open(target_filepath, "w", encoding="utf-8", newline="") as f:
        f.write(normalized_content)

    size = os.path.getsize(target_filepath)
    logger.info(
        f"[Meta/Instagram] Successfully saved official {official_filename} to {target_filepath} ({size} bytes, {len(lines)} lines)"
    )

    return [{
        "platform": "instagram",
        "file": target_filename,
        "official_filename": official_filename,
        "filepath": os.path.relpath(target_filepath).replace("\\", "/"),
        "status": "downloaded",
        "size_bytes": size,
        "row_count": len(lines),
        "retrieval_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }]


# ==============================================================================
# 3. TIKTOK ACQUISITION
# ==============================================================================
TIKTOK_CDN_BASE = "https://sf16-va.tiktokcdn.com/obj/eden-va2/zkyhviozhk_YLNJ/ljhwZthlaukjlkulzlp/2026Q1/"
TIKTOK_ARTIFACTS = [
    "2_Volume_English.html",
    "3_Speed_English.html",
    "4_Policies_English.html",
    "1_Prevalence_English.html",
    "5_Geography_English.html",
]


def download_tiktok(output_dir: str, force: bool = False) -> List[Dict[str, Any]]:
    """Download official TikTok Transparency Center CDN dashboard artifacts containing window.injectedData."""
    os.makedirs(output_dir, exist_ok=True)
    manifest_entries = []

    logger.info(f"Starting TikTok acquisition for official 2026Q1 artifacts from {TIKTOK_CDN_BASE}...")

    for artifact in TIKTOK_ARTIFACTS:
        target_path = os.path.join(output_dir, artifact)

        if os.path.exists(target_path) and os.path.getsize(target_path) > 0 and not force:
            logger.debug(f"[TikTok] Skipping existing file: {artifact}")
            manifest_entries.append({
                "platform": "tiktok",
                "artifact": artifact,
                "filepath": os.path.relpath(target_path).replace("\\", "/"),
                "status": "existing",
                "size_bytes": os.path.getsize(target_path),
            })
            continue

        artifact_url = f"{TIKTOK_CDN_BASE}{artifact}"
        req = urllib.request.Request(artifact_url, headers={"User-Agent": USER_AGENT})

        try:
            raw_bytes = fetch_with_retry(req)
            content_str = raw_bytes.decode("utf-8", errors="ignore")

            # Verify that window.injectedData exists and parses
            match = re.search(r"window\.injectedData\s*=\s*(\{.*?\});\s*(?:new Chart|\n)", content_str, re.DOTALL)
            if not match:
                raise ValueError(f"Could not locate window.injectedData in {artifact}")
            _ = json.loads(match.group(1))

            with open(target_path, "wb") as f:
                f.write(raw_bytes)

            size = os.path.getsize(target_path)
            logger.info(f"[TikTok] Acquired {artifact} ({size} bytes, verified window.injectedData)")
            manifest_entries.append({
                "platform": "tiktok",
                "artifact": artifact,
                "filepath": os.path.relpath(target_path).replace("\\", "/"),
                "status": "downloaded",
                "size_bytes": size,
                "retrieval_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            })
        except Exception as e:
            logger.error(f"[TikTok] Failed to acquire {artifact}: {e}")
            manifest_entries.append({
                "platform": "tiktok",
                "artifact": artifact,
                "filepath": os.path.relpath(target_path).replace("\\", "/"),
                "status": f"failed: {e}",
                "size_bytes": 0,
            })

    return manifest_entries


# ==============================================================================
# MAIN RUNNER & MANIFEST
# ==============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Acquire official supplementary platform transparency datasets (Phase 3B)."
    )
    parser.add_argument(
        "--platform",
        choices=["youtube", "instagram", "tiktok", "all"],
        required=True,
        help="Target platform source to acquire.",
    )
    parser.add_argument(
        "--start-quarter",
        default="2021Q1",
        help="Earliest quarter for time-series acquisition (default: 2021Q1).",
    )
    parser.add_argument(
        "--end-quarter",
        default="2026Q1",
        help="Latest quarter for time-series acquisition (default: 2026Q1).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if files already exist.",
    )
    parser.add_argument(
        "--output-root",
        default=os.path.join("data", "raw", "supplementary"),
        help="Root directory for raw supplementary data storage.",
    )

    args = parser.parse_args()

    base_dir = os.path.abspath(args.output_root)
    yt_dir = os.path.join(base_dir, "youtube")
    ig_dir = os.path.join(base_dir, "instagram")
    tt_dir = os.path.join(base_dir, "tiktok")

    manifest_path = os.path.join(base_dir, "manifest.json")
    existing_manifest: Dict[str, Any] = {}
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                existing_manifest = json.load(f)
        except Exception:
            existing_manifest = {}

    manifest_records: List[Dict[str, Any]] = existing_manifest.get("records", [])

    logger.info("==================================================")
    logger.info(f"Supplementary Acquisition: platform={args.platform}, range={args.start_quarter}..{args.end_quarter}")
    logger.info(f"Target directory: {base_dir}")
    logger.info("==================================================")

    if args.platform in ("youtube", "all"):
        yt_records = download_youtube(yt_dir, args.start_quarter, args.end_quarter, args.force)
        manifest_records.extend(yt_records)

    if args.platform in ("instagram", "all"):
        ig_records = download_instagram(ig_dir, args.force)
        manifest_records.extend(ig_records)

    if args.platform in ("tiktok", "all"):
        tt_records = download_tiktok(tt_dir, args.force)
        manifest_records.extend(tt_records)

    # Save manifest
    manifest_data = {
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "target_window": f"{args.start_quarter} through {args.end_quarter}",
        "records": manifest_records,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    logger.info(f"Manifest written to {manifest_path} with {len(manifest_records)} entries.")
    logger.info("Phase 3B acquisition execution finished.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: No arguments provided. Use --platform [youtube|instagram|tiktok|all]. See --help.")
        sys.exit(1)
    sys.exit(main())

