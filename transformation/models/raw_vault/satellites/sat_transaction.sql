{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_transaction_h',
    src_hashdiff='hd_transaction_s',
    src_payload=['transaction_date', 'transaction_type', 'transaction_amount'],
    source_model='v_stg_transaction'
) }}
