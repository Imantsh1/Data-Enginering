import src.ingest as ingest
import src.transform as transform
import src.serving as serving

def main():
    # 1. Configuration
    QUERY = "AI productivity"
    MAX_APPS = 3
    MAX_REVIEWS_PER_APP = 100

    print("--- Phase 1: Ingestion ---")
    app_ids = ingest.fetch_apps_by_query(QUERY, n_results=MAX_APPS)
    for app_id in app_ids:
        ingest.ingest_app_data(app_id, max_reviews=MAX_REVIEWS_PER_APP)

    print("\n--- Phase 2: Transformation ---")
    transform.main()

    print("\n--- Phase 3: Serving Metrics ---")
    serving.main()
    
    print("\nPipeline execution complete.")

if __name__ == "__main__":
    main()
