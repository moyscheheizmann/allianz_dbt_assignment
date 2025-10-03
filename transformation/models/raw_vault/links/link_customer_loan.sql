{{ config(materialized='incremental') }}

{%- set source_models = {
    'v_stg_loan': {}
} -%}

{{ datavault4dbt.link(
    link_hashkey='hk_customer_loan_l',
    foreign_hashkeys=['hk_customer_h', 'hk_loan_h'],
    source_models=source_models
) }}
