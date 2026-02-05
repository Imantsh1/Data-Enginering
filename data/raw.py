#!/usr/bin/env python3
"""
data/raw.py

Orchestrator that calls src/ingest.py to fetch metadata and reviews for a list of apps.

Examples:
  python data/raw.py
  python data/raw.py --reviews 150
  python data/raw.py --apps com.otter.ai com.feraset.ainote com.appzone.noteai
  python data/raw.py --apps-file my_apps.json --reviews 200
"""
from pathlib import Path
import argparse
import subprocess
import sys
import json

REPO_ROOT = Path(_file_).resolve().parent.parent
INGEST_SCRIPT = REPO_ROOT / "src" / "ingest.py"

def run_ingest(apps, reviews):
    if not INGEST_SCRIPT.exists():
        raise SystemExit(f"Cannot find ingest script at {INGEST_SCRIPT}")
    cmd = [sys.executable, str(INGEST_SCRIPT), "--reviews", str(reviews)]
    # If apps are provided, pass them on the CLI
    if apps:
        cmd += ["--apps"] + apps
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def read_apps_file(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("apps-file must contain a JSON list of app package names.")
    return data

def main():
    parser = argparse.ArgumentParser(description="Run ingestion for a set of Google Play apps")
    parser.add_argument("--apps", nargs="+", help="List of app package names")
    parser.add_argument("--apps-file", help="Path to JSON file containing list of app package names")
    parser.add_argument("--reviews", type=int, default=100, help="Number of reviews to fetch per app")
    args = parser.parse_args()

    # Default apps - replace/verify these package names
    default_apps = ["com.otter.ai", "com.feraset.ainote", "com.appzone.noteai"]

    if args.apps_file:
        apps = read_apps_file(Path(args.apps_file))
    elif args.apps:
        apps = args.apps
    else:
        apps = default_apps
        print("No apps provided; using default list:", apps)

    try:
        run_ingest(apps, args.reviews)
        print("Ingest completed.")
    except subprocess.CalledProcessError as e:
        print("Ingest script failed:", e)
        sys.exit(e.returncode)

if _name_ == "_main_":
    main()
