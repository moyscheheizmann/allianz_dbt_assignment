{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_transaction': {}
} -%}

{{ datavault4dbt.link(
    link_hashkey='hk_account_transaction_l',
    foreign_hashkeys=['hk_account_h', 'hk_transaction_h'],
    source_models=source_models
) }}
