
      update "google_play"."main"."apps_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "apps_snapshot__dbt_tmp20260222144507571368" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "google_play"."main"."apps_snapshot" ("app_id", "app_name", "rating", "category", "developer_name", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."app_id",DBT_INTERNAL_SOURCE."app_name",DBT_INTERNAL_SOURCE."rating",DBT_INTERNAL_SOURCE."category",DBT_INTERNAL_SOURCE."developer_name",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "apps_snapshot__dbt_tmp20260222144507571368" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  