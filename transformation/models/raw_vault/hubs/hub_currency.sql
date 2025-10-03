{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_currency': {
        'bk_columns': ['currency_iso_code']
    }
} -%}

{{ datavault4dbt.hub(
    hashkey='hk_currency_h',
    business_keys=['currency_iso_code'],
    source_models=source_models
) }}
