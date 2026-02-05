#!/usr/bin/env python3
"""
ingest.py

Fetch app metadata and reviews from Google Play using google_play_scraper.

Saves:
- data/raw/{app_id}_meta.json   (metadata JSON)
- data/raw/{app_id}_reviews.jsonl (one JSON review per line)

Usage:
  python src/ingest.py --apps com.aisense.otter com.evernote com.google.android.keep --reviews 150
  python src/ingest.py --apps-file apps.json --reviews 200
  python src/ingest.py                      # uses defaults (edit defaults in the script)
"""
import argparse
import json
from pathlib import Path
from typing import List

from google_play_scraper import app as gp_app
from google_play_scraper import reviews as gp_reviews, Sort

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def save_json(obj, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def save_jsonl(records: List[dict], path: Path):
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def fetch_metadata(app_id: str):
    print(f"Fetching metadata for {app_id} ...")
    meta = gp_app(app_id, lang="en", country="us")
    return meta


def fetch_reviews(app_id: str, count: int = 100, sleep_milliseconds: int = 0):
    """
    Fetch reviews using google_play_scraper.reviews. Returns list of review dicts.
    (The function may return (reviews, continuation_token) depending on library version.)
    """
    print(f"Fetching up to {count} reviews for {app_id} ...")
    result = gp_reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=count,
        sleep_milliseconds=sleep_milliseconds,
    )
    # Some versions return (reviews, continuation_token)
    if isinstance(result, tuple):
        reviews_list = result[0]
    else:
        reviews_list = result
    return reviews_list


def main():
    parser = argparse.ArgumentParser(description="Ingest app metadata and reviews from Google Play")
    parser.add_argument("--apps", nargs="+", help="List of app package names (space separated)")
    parser.add_argument("--apps-file", help="Path to a JSON file with a list of app ids")
    parser.add_argument("--reviews", type=int, default=100, help="Number of reviews to fetch per app")
    args = parser.parse_args()

    # Default app ids: replace with verified package names for your target AI note apps
    default_apps = [
        "com.aisense.otter",            # Otter.ai (verify package name)
        "com.evernote",                 # Evernote (general note app)
        "com.google.android.keep",      # Google Keep (general note app)
    ]

    if args.apps_file:
        apps_path = Path(args.apps_file)
        if not apps_path.exists():
            raise SystemExit(f"Apps file not found: {apps_path}")
        apps = json.loads(apps_path.read_text(encoding="utf-8"))
        if not isinstance(apps, list):
            raise SystemExit("apps-file must contain a JSON list of app package names.")
    elif args.apps:
        apps = args.apps
    else:
        apps = default_apps
        print("No apps provided on the CLI. Using default apps (edit defaults in the script).")

    for app_id in apps:
        try:
            meta = fetch_metadata(app_id)
            meta_path = RAW_DIR / f"{app_id}_meta.json"
            save_json(meta, meta_path)
            reviews = fetch_reviews(app_id, count=args.reviews)
            reviews_path = RAW_DIR / f"{app_id}_reviews.jsonl"
            save_jsonl(reviews, reviews_path)
            print(f"Saved metadata to {meta_path} and {len(reviews)} reviews to {reviews_path}")
        except Exception as e:
            print(f"Error fetching {app_id}: {e}")


if __name__ == "__main__":
    main()