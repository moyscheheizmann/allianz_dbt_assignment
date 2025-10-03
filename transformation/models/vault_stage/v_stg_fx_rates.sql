{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: 'stg_staging_intermediate__fx_rates'
hashed_columns:
    hk_currency_h:
        - currency_iso_code
    hd_fx_rates_s:
        is_hashdiff: true
        columns:
            - fx_rate
            - fx_rate_date
ldts: "CURRENT_TIMESTAMP"
rsrc: '!intermediate.fx_rates'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ datavault4dbt.stage(include_source_columns=true,
                        source_model=metadata_dict['source_model'],
                        hashed_columns=metadata_dict['hashed_columns'],
                        ldts=metadata_dict['ldts'],
                        rsrc=metadata_dict['rsrc']) }}
