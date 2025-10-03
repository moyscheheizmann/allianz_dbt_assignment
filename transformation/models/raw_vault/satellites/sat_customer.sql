{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_customer_h',
    src_hashdiff='hd_customer_s',
    src_payload=['firstname', 'lastname', 'age', 'branch_id'],
    source_model='v_stg_customer'
) }}
