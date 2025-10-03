{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'stg_staging_intermediate__loans'
hashed_columns:
    hk_loan_h:
        - loan_id
    hk_customer_h:
        - customer_id
    hk_customer_loan_l:
        - customer_id
        - loan_id
    hd_loan_s:
        is_hashdiff: true
        columns:
            - loan_amount
            - loan_type
            - interest_rate
            - loan_term
            - approval_rejection_date
            - loan_status
ldts: "CURRENT_TIMESTAMP"
rsrc: '!intermediate.loans'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ datavault4dbt.stage(include_source_columns=true,
                        source_model=metadata_dict['source_model'],
                        hashed_columns=metadata_dict['hashed_columns'],
                        ldts=metadata_dict['ldts'],
                        rsrc=metadata_dict['rsrc']) }}
