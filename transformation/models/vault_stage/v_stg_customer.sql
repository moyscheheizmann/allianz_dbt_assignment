{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'stg_staging_intermediate__customers'
hashed_columns:
    hk_customer_h:
        - customer_id
    hd_customer_s:
        is_hashdiff: true
        columns:
            - firstname
            - lastname
            - age
            - branch_id
ldts: "CURRENT_TIMESTAMP"
rsrc: '!intermediate.customers'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ datavault4dbt.stage(include_source_columns=true,
                        source_model=metadata_dict['source_model'],
                        hashed_columns=metadata_dict['hashed_columns'],
                        ldts=metadata_dict['ldts'],
                        rsrc=metadata_dict['rsrc']) }}
