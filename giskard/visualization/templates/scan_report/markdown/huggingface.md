{% if issues|length == 0 %}
<div class="m-4">
    <div class="p-3 bg-green-100/40 rounded-sm w-full flex align-middle">
        <p class="ml-2 my-1 text-green-50 text-sm">
            We found no issues in your model. Good job!
        </p>
    </div>
</div>
{% endif %}

{% for view in groups -%}

<details>
<summary>👉{{ view.group.name }} issues ({{ view.issues|length }})</summary>

{% for issue in view.issues -%}

| Level | Data slice | Metric | Deviation |
|-------|------------|--------|-----------|
| <span style="color:{% if issue.level.value == "major" %} red {% else %} orange {% endif %} "> {{ issue.level.value }} {% if issue.level.value == "major" %} 🔴 {% else %} 🟡 {% endif %} </span> | {{ issue.slicing_fn if issue.slicing_fn else "—" }} | {% if "metric" in issue.meta %}{{ issue.meta.metric }} = {{ issue.meta.metric_value|format_metric }}{% else %} "—" {% endif %} | {{ issue.meta["deviation"] if "deviation" in issue.meta else "—" }} |

{% if issue.taxonomy %}
<h4 class="font-bold text-sm mt-4">Taxonomy</h4>
{% for tag in issue.taxonomy %}
<span class="inline-block bg-blue-300/25 text-zinc-100 px-2 py-0.5 rounded-sm text-sm mr-1 my-2">
    {{ tag }}
</span>
{% endfor %}
<br />
{% endif %}

<details>
<summary> 🔍✨Examples</summary>
{{ issue.description }}

{% if issue.examples(3)|length %}
{{ issue.examples(issue.meta.num_examples if "num_examples" in issue.meta else 3).to_markdown(
index=not issue.meta.hide_index if "hide_index" in issue.meta
else True)|replace("\\n", "<br>")|safe }}
{% endif %}
</details>

{% endfor %}

</details>
{% endfor -%}
<br />
<!-- line breaker -->

