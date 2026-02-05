#!/usr/bin/env python3
"""
data/processed.py

Orchestrator to run transform and serving steps:

•⁠  ⁠Calls src/transform.py to produce apps_catalog.csv and apps_reviews.csv
•⁠  ⁠Calls src/serving.py to produce app_kpis.csv and daily_metrics.csv

Examples:
  python data/processed.py
  python data/processed.py --no-serve       # only run transform
  python data/processed.py --no-transform   # only run serving (requires prior transform)
"""
from pathlib import Path
import argparse
import subprocess
import sys

REPO_ROOT = Path(_file_).resolve().parent.parent
TRANSFORM_SCRIPT = REPO_ROOT / "src" / "transform.py"
SERVING_SCRIPT = REPO_ROOT / "src" / "serving.py"

def run_script(script_path: Path):
    if not script_path.exists():
        raise SystemExit(f"Cannot find script at {script_path}")
    cmd = [sys.executable, str(script_path)]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Run transform and serving steps to create processed CSVs")
    parser.add_argument("--no-transform", action="store_true", help="Skip transform step")
    parser.add_argument("--no-serve", action="store_true", help="Skip serving step")
    args = parser.parse_args()

    try:
        if not args.no_transform:
            run_script(TRANSFORM_SCRIPT)
        else:
            print("Skipping transform step.")

        if not args.no_serve:
            run_script(SERVING_SCRIPT)
        else:
            print("Skipping serving step.")

        print("Processed outputs completed.")
    except subprocess.CalledProcessError as e:
        print("A step failed:", e)
        sys.exit(e.returncode)

if _name_ == "_main_":
    main()
