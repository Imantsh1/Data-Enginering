select
    -- Standardize naming and cast types
    cast(appId as varchar) as app_id,
    cast(title as varchar) as app_name,
    cast(score as float) as rating,
    cast(genre as varchar) as category,
    cast(developer as varchar) as developer_name
from read_json_auto('raw_data/apps.json')
