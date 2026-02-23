{% snapshot apps_snapshot %}
{{
    config(
      target_schema='main',
      strategy='check',
      unique_key='app_id',
      check_cols=['rating'],
    )
}}
select * from {{ ref('stg_playstore_apps') }}
{% endsnapshot %}