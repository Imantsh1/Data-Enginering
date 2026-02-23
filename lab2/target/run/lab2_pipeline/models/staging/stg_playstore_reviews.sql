
        
            delete from "google_play"."main"."stg_playstore_reviews"
            where (
                review_id) in (
                select (review_id)
                from "stg_playstore_reviews__dbt_tmp20260222135036541030"
            );

        
    

    insert into "google_play"."main"."stg_playstore_reviews" ("review_id", "app_id", "review_text", "review_score", "review_date")
    (
        select "review_id", "app_id", "review_text", "review_score", "review_date"
        from "stg_playstore_reviews__dbt_tmp20260222135036541030"
    )
  