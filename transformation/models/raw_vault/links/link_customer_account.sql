{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_account': {}
} -%}

{{ datavault4dbt.link(
    link_hashkey='hk_customer_account_l',
    foreign_hashkeys=['hk_customer_h', 'hk_account_h'],
    source_models=source_models
) }}
