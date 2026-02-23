

select
    cast("reviewId" as varchar) as review_id,
    cast(app_id as varchar) as app_id,
    cast(content as varchar) as review_text,
    try_cast(score as integer) as review_score,
    try_cast("at" as timestamp) as review_date
from read_csv_auto('raw_data/note_taking_ai_reviews_dirty.csv')


  -- This tells dbt to only load reviews that are newer than the newest review already in the table
  where try_cast("at" as timestamp) > (select max(review_date) from "google_play"."main"."stg_playstore_reviews")
