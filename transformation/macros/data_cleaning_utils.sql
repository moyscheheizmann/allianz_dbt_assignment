-- macros/date_utils.sql

{% macro date_format_case(column_name) %}
CASE
    -- Handle NULL and empty strings
    WHEN {{ column_name }} IS NULL OR TRIM({{ column_name }}) = '' THEN NULL

    -- First try DD.MM.YYYY format (German format with dots)
    WHEN {{ column_name }} ~ '^\d{1,2}\.\d{1,2}\.\d{4}$'
        THEN TO_DATE({{ column_name }}, 'DD.MM.YYYY')

    -- Then try DD/MM/YYYY format (with slashes)
    WHEN {{ column_name }} ~ '^\d{1,2}/\d{1,2}/\d{4}$'
        AND CAST(SPLIT_PART({{ column_name }}, '/', 1) AS INTEGER) <= 31
        AND CAST(SPLIT_PART({{ column_name }}, '/', 2) AS INTEGER) <= 12
        THEN TO_DATE({{ column_name }}, 'DD/MM/YYYY')

    -- Try MM/DD/YYYY format (US format with slashes)
    WHEN {{ column_name }} ~ '^\d{1,2}/\d{1,2}/\d{4}$'
        AND CAST(SPLIT_PART({{ column_name }}, '/', 1) AS INTEGER) <= 12
        THEN TO_DATE({{ column_name }}, 'MM/DD/YYYY')

    -- Try YYYY-MM-DD format (ISO format)
    WHEN {{ column_name }} ~ '^\d{4}-\d{1,2}-\d{1,2}$'
        THEN TO_DATE({{ column_name }}, 'YYYY-MM-DD')

    -- Return NULL for unparseable dates instead of failing
    ELSE NULL
END
{% endmacro %}

{% macro convert_german_number_case(column_name) %}
CASE
    WHEN {{ column_name }} IS NULL THEN NULL
    -- If the value is already a valid number
    WHEN {{ column_name }} ~ '^-?\d+\.?\d*$'
        THEN {{ column_name }}::DOUBLE PRECISION
    -- If contains both dot and comma (German notation)
    WHEN POSITION('.' IN {{ column_name }}) > 0 AND POSITION(',' IN {{ column_name }}) > 0
        THEN REPLACE(REPLACE(TRIM({{ column_name }}), '.', ''), ',', '.')::DOUBLE PRECISION
    -- If only contains comma, treat as decimal point
    WHEN POSITION(',' IN {{ column_name }}) > 0
        THEN REPLACE(TRIM({{ column_name }}), ',', '.')::DOUBLE PRECISION
    -- If only contains dots, likely thousands separator
    WHEN POSITION('.' IN {{ column_name }}) > 0
        THEN REPLACE(TRIM({{ column_name }}), '.', '')::DOUBLE PRECISION
    ELSE NULL
END
{% endmacro %}
