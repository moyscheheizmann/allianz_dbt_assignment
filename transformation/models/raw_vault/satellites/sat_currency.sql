{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_currency_h',
    src_hashdiff='hd_currency_s',
    src_payload=['currency'],
    source_model='v_stg_currency'
) }}
