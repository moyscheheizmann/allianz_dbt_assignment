{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_loan': {
        'bk_columns': ['loan_id']
    }
} -%}

{{ datavault4dbt.hub(
    hashkey='hk_loan_h',
    business_keys=['loan_id'],
    source_models=source_models
) }}
