{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_account': {
        'bk_columns': ['account_id']
    }
} -%}

{{ datavault4dbt.hub(
    hashkey='hk_account_h',
    business_keys=['account_id'],
    source_models=source_models
) }}
