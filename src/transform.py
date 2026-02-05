#!/usr/bin/env python3
"""
transform.py

Read raw metadata JSON files and reviews JSONL, produce tabular CSVs:

- data/processed/apps_catalog.csv
  schema: appId, title, developer, score, ratings, installs, genre, price

- data/processed/apps_reviews.csv
  schema: app_id, app_name, reviewId, userName, score, content, thumbsUpCount, at

Usage:
  python src/transform.py
"""
import json
from pathlib import Path
from typing import List

import pandas as pd

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)


def load_metadata_files() -> List[dict]:
    metas = []
    for p in sorted(RAW_DIR.glob("*_meta.json")):
        try:
            with p.open("r", encoding="utf-8") as f:
                metas.append(json.load(f))
        except Exception as e:
            print(f"Skipping {p}: {e}")
    return metas


def load_reviews_files() -> List[dict]:
    recs = []
    for p in sorted(RAW_DIR.glob("*_reviews.jsonl")):
        app_id = p.name.split("_reviews.jsonl")[0]
        try:
            with p.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    # annotate with app context
                    r["_source_app_id"] = app_id
                    recs.append(r)
        except Exception as e:
            print(f"Skipping {p}: {e}")
    return recs


def build_apps_catalog(metas: List[dict]) -> pd.DataFrame:
    rows = []
    for m in metas:
        # Map to required schema; handle missing keys gracefully
        rows.append({
            "appId": m.get("appId") or m.get("app_id") or m.get("appID"),
            "title": m.get("title"),
            "developer": m.get("developer"),
            "score": m.get("score"),
            "ratings": m.get("ratings"),
            "installs": m.get("installs"),
            "genre": m.get("genre"),
            "price": m.get("price"),
        })
    df = pd.DataFrame(rows)
    # Basic normalization
    df = df.drop_duplicates(subset=["appId"])
    return df


def build_apps_reviews(recs: List[dict]) -> pd.DataFrame:
    rows = []
    for r in recs:
        rows.append({
            "app_id": r.get("_source_app_id"),
            "app_name": r.get("appName") or r.get("app_name") or r.get("appTitle"),
            "reviewId": r.get("reviewId"),
            "userName": r.get("userName"),
            "score": r.get("score"),
            "content": r.get("content"),
            "thumbsUpCount": r.get("thumbsUpCount"),
            "at": r.get("at"),  # typically an ISO datetime object or string
        })
    df = pd.DataFrame(rows)
    # Convert 'at' to datetime
    if "at" in df.columns:
        df["at"] = pd.to_datetime(df["at"], errors="coerce")
    return df


def main():
    metas = load_metadata_files()
    reviews = load_reviews_files()

    if not metas and not reviews:
        print("No raw files found in data/raw/. Run ingest.py first.")
        return

    if metas:
        apps_df = build_apps_catalog(metas)
        apps_out = PROC_DIR / "apps_catalog.csv"
        apps_df.to_csv(apps_out, index=False)
        print(f"Wrote {len(apps_df)} apps to {apps_out}")
    else:
        print("No metadata files to transform.")

    if reviews:
        reviews_df = build_apps_reviews(reviews)
        reviews_out = PROC_DIR / "apps_reviews.csv"
        reviews_df.to_csv(reviews_out, index=False)
        print(f"Wrote {len(reviews_df)} reviews to {reviews_out}")
    else:
        print("No reviews files to transform.")


if __name__ == "__main__":
    main()
