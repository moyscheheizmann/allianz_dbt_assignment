{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_currency_h',
    src_hashdiff='hd_fx_rates_s',
    src_payload=['fx_rate', 'fx_rate_date'],
    source_model='v_stg_fx_rates'
) }}
