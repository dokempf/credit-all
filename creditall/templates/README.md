In alphabetical order:
{% for c in contributors|sort(attribute='name') -%}
* {{ c.name }} ({% for t in c.contributions %}{{ types[t]['description'] }}{{ ", " if not loop.last }}{% endfor %})
{%- endfor %}
