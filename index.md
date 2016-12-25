---
layout: default
title: Recent Blog Posts
---

{% for post in site.posts %}
[{{ post.title }}]({{ post.url }}) {{ post.date | date: "%Y-%m-%d"}}

{{ post.excerpt | strip_html | truncatewords: 50 }}

{% endfor %}
