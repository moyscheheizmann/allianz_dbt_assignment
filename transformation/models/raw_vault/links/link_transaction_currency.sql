{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_transaction': {}
} -%}

{{ datavault4dbt.link(
    link_hashkey='hk_transaction_currency_l',
    foreign_hashkeys=['hk_transaction_h', 'hk_currency_h'],
    source_models=source_models
) }}
