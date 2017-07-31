---
layout: default
title: Easiest way to turn a Jinja2 template into an HTML file
---

The [docs](http://jinja.pocoo.org/docs/2.9/api/#basics) talk about using the environment or whatever, but for my use case, I usually prefer the FileSystemLoader:

```python
import jinja2 as j2

# need a templates folder to look into (or change it to '.')
env = j2.Environment(loader=j2.FileSystemLoader('./templates'),
                     autoescape=j2.select_autoescape(['html', 'xml']))
template = env.get_template('t1.jinja2')
print(template.render(the='variables', go='here'))
```
