{% macro postgres__drop_relation(relation) -%}
  {% call statement('drop_relation', auto_begin=False) -%}
    DROP {{ relation.type }} IF EXISTS {{ relation }} CASCADE
  {%- endcall %}
{%- endmacro %}
