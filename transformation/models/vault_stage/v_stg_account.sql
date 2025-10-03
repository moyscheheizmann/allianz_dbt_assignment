{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'stg_staging_intermediate__accounts'
hashed_columns:
    hk_account_h:
        - account_id
    hk_customer_h:
        - customer_id
    hk_customer_account_l:
        - customer_id
        - account_id
    hd_account_s:
        is_hashdiff: true
        columns:
            - account_type
            - account_opening_date
ldts: "CURRENT_TIMESTAMP"
rsrc: '!intermediate.accounts'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ datavault4dbt.stage(include_source_columns=true,
                        source_model=metadata_dict['source_model'],
                        hashed_columns=metadata_dict['hashed_columns'],
                        ldts=metadata_dict['ldts'],
                        rsrc=metadata_dict['rsrc']) }}
