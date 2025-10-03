{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_account_h',
    src_hashdiff='hd_account_s',
    src_payload=['account_type', 'account_opening_date'],
    source_model='v_stg_account'
) }}
