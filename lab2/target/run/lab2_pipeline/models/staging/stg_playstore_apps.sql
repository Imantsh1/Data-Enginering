
  
  create view "google_play"."main"."stg_playstore_apps__dbt_tmp" as (
    select
    cast(appid as varchar) as app_id,
    cast(title as varchar) as app_name,
    try_cast(score as float) as rating,
    cast(genre as varchar) as category,
    cast(developer as varchar) as developer_name
from read_csv(
    'raw_data/note_taking_ai_apps_updated.csv',
    header=true,
    delim=',',
    normalize_names=true,
    ignore_errors=true,
    null_padding=true,
    strict_mode=false
)
-- Keeps the unique app by prioritizing the highest rating (and puts NULLs at the bottom)
qualify row_number() over (partition by app_id order by try_cast(score as float) desc nulls last) = 1
  );
