---
layout: default
title: Ben's Corner
---

{% for post in site.posts %}
### [{{ post.title }}]({{ post.url }}) {{ post.date | date: "%Y-%m-%d"}} | {{ post.content | number_of_words }} words

{{ post.excerpt | strip_html | truncatewords: 50 }}

{% endfor %}
