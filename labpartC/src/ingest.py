import json
from pathlib import Path
from google_play_scraper import search, app, reviews, Sort

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_apps_by_query(query: str, n_results: int = 5):
    """Search for apps based on a keyword rather than hardcoded IDs."""
    print(f"Searching for apps related to: '{query}'")
    results = search(query, n_results=n_results)
    return [res['appId'] for res in results]

def ingest_app_data(app_id: str, max_reviews: int = 100):
    """Fetches metadata and streams reviews to a JSONL file."""
    print(f"Ingesting: {app_id}")
    
    # 1. Fetch and save metadata
    info = app(app_id)
    with open(RAW_DIR / f"{app_id}_meta.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)

    # 2. Fetch and append reviews (Safety measure)
    review_file = RAW_DIR / f"{app_id}_reviews.jsonl"
    
    # Clear file if it exists or start fresh
    with open(review_file, "w", encoding="utf-8") as f:
        result, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=max_reviews
        )
        
        for r in result:
            # Convert datetime objects to string for JSON serialization
            if 'at' in r:
                r['at'] = r['at'].isoformat()
            
            # Write line by line: if the script crashes, previous lines are saved
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    # Example usage for standalone testing
    apps = fetch_apps_by_query("AI note taking", n_results=3)
    for a_id in apps:
        ingest_app_data(a_id, max_reviews=50)
