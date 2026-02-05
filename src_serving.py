#!/usr/bin/env python3
"""
serving.py

Generates two CSV outputs in data/processed/:

1) app_kpis.csv
   Columns:
     app_id, app_name, num_reviews, avg_rating, pct_low_ratings, first_review_at, last_review_at

2) daily_metrics.csv
   Columns:
     app_id, app_name, date, daily_reviews, daily_avg_rating

Usage:
  python src/serving.py
"""
from pathlib import Path

import pandas as pd

PROC_DIR = Path("data/processed")
APPS_FILE = PROC_DIR / "apps_catalog.csv"
REVIEWS_FILE = PROC_DIR / "apps_reviews.csv"
KPIS_OUT = PROC_DIR / "app_kpis.csv"
DAILY_OUT = PROC_DIR / "daily_metrics.csv"


def load_inputs():
    if not APPS_FILE.exists() or not REVIEWS_FILE.exists():
        raise SystemExit("Missing processed inputs. Run transform.py first.")
    apps = pd.read_csv(APPS_FILE, dtype={"appId": str})
    reviews = pd.read_csv(REVIEWS_FILE, parse_dates=["at"], dtype={"app_id": str})
    return apps, reviews


def compute_app_kpis(apps: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    # Ensure columns exist
    r = reviews.copy()
    r = r.dropna(subset=["app_id"])
    # Number of reviews and average rating
    grp = r.groupby("app_id").agg(
        num_reviews=("reviewId", "count"),
        avg_rating=("score", "mean"),
        pct_low_ratings=("score", lambda s: (s < 2).sum() / (s.count()) if s.count() else 0),
        first_review_at=("at", "min"),
        last_review_at=("at", "max"),
    ).reset_index()
    # Join app name from apps or reviews
    apps_map = apps.set_index("appId")["title"] if "title" in apps.columns else apps.set_index("appId").index
    grp["app_name"] = grp["app_id"].map(apps_map).fillna("")
    # Reorder columns
    grp = grp[["app_id", "app_name", "num_reviews", "avg_rating", "pct_low_ratings", "first_review_at", "last_review_at"]]
    return grp


def compute_daily_metrics(reviews: pd.DataFrame) -> pd.DataFrame:
    r = reviews.copy()
    if "at" not in r.columns:
        raise SystemExit("Reviews do not contain 'at' timestamps.")
    r["date"] = pd.to_datetime(r["at"]).dt.date
    grp = r.groupby(["app_id", "date"]).agg(
        daily_reviews=("reviewId", "count"),
        daily_avg_rating=("score", "mean"),
    ).reset_index()
    # Optional: map app names using latest seen app_name in reviews
    if "app_name" in r.columns:
        latest_names = r.groupby("app_id")["app_name"].last()
        grp["app_name"] = grp["app_id"].map(latest_names)
        grp = grp[["app_id", "app_name", "date", "daily_reviews", "daily_avg_rating"]]
    else:
        grp = grp[["app_id", "date", "daily_reviews", "daily_avg_rating"]]
    return grp


def main():
    apps, reviews = load_inputs()
    kpis = compute_app_kpis(apps, reviews)
    daily = compute_daily_metrics(reviews)

    kpis.to_csv(KPIS_OUT, index=False)
    daily.to_csv(DAILY_OUT, index=False)

    print(f"Wrote app KPIs to {KPIS_OUT} ({len(kpis)} rows)")
    print(f"Wrote daily metrics to {DAILY_OUT} ({len(daily)} rows)")


if __name__ == "__main__":
    main()