{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'stg_staging_intermediate__transactions'
hashed_columns:
    hk_transaction_h:
        - transaction_id
    hk_account_h:
        - account_id
    hk_currency_h:
        - transaction_currency
    hk_account_transaction_l:
        - account_id
        - transaction_id
    hk_transaction_currency_l:
        - transaction_id
        - transaction_currency
    hd_transaction_s:
        is_hashdiff: true
        columns:
            - transaction_date
            - transaction_type
            - transaction_amount
ldts: "CURRENT_TIMESTAMP"
rsrc: '!intermediate.transactions'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ datavault4dbt.stage(include_source_columns=true,
                        source_model=metadata_dict['source_model'],
                        hashed_columns=metadata_dict['hashed_columns'],
                        ldts=metadata_dict['ldts'],
                        rsrc=metadata_dict['rsrc']) }}
