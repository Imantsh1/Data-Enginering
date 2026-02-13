select
    -- Flattening and casting
    cast(reviewId as varchar) as review_id,
    cast(appId as varchar) as app_id,
    cast(score as integer) as review_score,
    cast(at as timestamp) as review_date,
    cast(content as varchar) as review_text
from read_json_auto('raw_data/reviews.json')
