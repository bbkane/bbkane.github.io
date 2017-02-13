---
layout: default
title: Easiest way to turn a Jinja2 template into an HTML file
---

The docs talk about using the environment or whatever, but for my use case, this was all I needed:

```python
with open('./my_template.jinja2') as template_file:
    template = Template(template_file.read())
with open('./output.html', 'w') as htmlfile:
    output = template.render(first_thing=first_thing
                             second_thing=second_thing)
    print(output, file=htmlfile)
```

If I do use the environment approach (for example, to use template inheritance), I use a slightly modified version from the [docs](http://jinja.pocoo.org/docs/2.9/api/#basics):

```python
import jinja2 as j2

# need a templates folder to look into
env = j2.Environment(loader=j2.FileSystemLoader('./templates'),
                     autoescape=j2.select_autoescape(['html', 'xml']))
template = env.get_template('t1.jinja2')
print(template.render(the='variables', go='here'))
```
