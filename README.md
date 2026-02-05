# App-Market-Research

A small Python-only pipeline scaffold to ingest Google Play metadata and reviews, transform into tabular CSVs, and compute simple serving metrics.

Project structure:

App-Market-Research/
├── data/
│   ├── raw/           <-- Untransformed JSON/JSONL (created by src/ingest.py)
│   └── processed/     <-- Cleaned CSV outputs (created by src/transform.py and src/serving.py)
├── src/               <-- Python scripts
│   ├── ingest.py      <-- Fetch metadata and reviews (google_play_scraper)
│   ├── transform.py   <-- Transform raw JSON/JSONL into tabular CSVs
│   └── serving.py     <-- Compute KPIs and daily metrics CSVs
├── .gitignore
├── requirements.txt
└── README.md

Quickstart

1. Create virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Ingest raw data (example)
```bash
# Default in the script attempts a few common apps. Replace with verified package names for your target apps.
python src/ingest.py --apps com.aisense.otter com.evernote com.google.android.keep --reviews 150
```
Or provide a JSON file containing a list of app package names:
```bash
python src/ingest.py --apps-file my_apps.json --reviews 200
```

4. Transform raw -> processed
```bash
python src/transform.py
# Produces:
# - data/processed/apps_catalog.csv
# - data/processed/apps_reviews.csv
```

5. Generate serving outputs
```bash
python src/serving.py
# Produces:
# - data/processed/app_kpis.csv
# - data/processed/daily_metrics.csv
```

Notes & Next steps
- Verify Android package names for the target AI note-taking apps (Otter.ai, Notion AI, Mem, etc.). The scraper requires exact package ids.
- The `google_play_scraper` package version may change API return shapes; scripts defensively handle common return formats but you should test locally.
- For large-scale scraping consider rate limiting, proxies, or an API that supports higher throughput; respect terms of service.
- Add logging and error handling for production usage.
- Add unit tests for transform functions (small sample JSON & expected CSV rows).