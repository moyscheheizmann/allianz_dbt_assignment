{{ config(materialized='incremental') }}

{{ datavault4dbt.sat_v0(
    parent_hashkey='hk_loan_h',
    src_hashdiff='hd_loan_s',
    src_payload=['loan_amount', 'loan_type', 'interest_rate', 'loan_term', 'approval_rejection_date', 'loan_status'],
    source_model='v_stg_loan'
) }}
