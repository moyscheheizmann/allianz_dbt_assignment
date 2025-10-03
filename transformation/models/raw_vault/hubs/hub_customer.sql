{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_customer': {
        'bk_columns': ['customer_id']
    }
} -%}

{{ datavault4dbt.hub(
    hashkey='hk_customer_h',
    business_keys=['customer_id'],
    source_models=source_models
) }}
