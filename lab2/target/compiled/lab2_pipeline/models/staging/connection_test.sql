-- Connection test to prove dbt can create objects in DuckDB [cite: 140]
select 
    1 as ok, 
    current_timestamp as created_at