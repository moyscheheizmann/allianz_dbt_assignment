{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_transaction': {
        'bk_columns': ['transaction_id']
    }
} -%}

{{ datavault4dbt.hub(
    hashkey='hk_transaction_h',
    business_keys=['transaction_id'],
    source_models=source_models
) }}
