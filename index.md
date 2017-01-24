---
layout: default
title: Ben's Corner
---

## [Posts]({{ site.baseurl }}{% link post_index.md %})

{% for post in site.posts limit: 5 %}
### [{{ post.title }}]({{ post.url }}) {{ post.date | date: "%Y-%m-%d"}}
{{ post.excerpt | strip_html | truncatewords: 50 }}
{% endfor %}


## APIDOCS

{% assign items = site.apidocs | sort: 'order' %}
{% for post in items limit: 5 %}
### [{{ post.title }}]({{ post.url }}) {{ post.date | date: "%Y-%m-%d"}}
{{ post.excerpt | strip_html | truncatewords: 50 }}
{% endfor %}
