+++
title = "Printing Objects in Flask"
date = 2018-01-22
updated = 2018-01-22
aliases = [ "2018/01/22/Printing-Objects-in-Flask.html" ]
+++

Recently I needed to painlessly enumerate a (simple) Python object's properties
in HTML to make a web page. I was creating different types of objects and I just
wanted an easy way to print them. This post is how to do that in Flask.

## What is a "(simple) Python object"

What I'm calling a simple Python object is an instance of a class or namedtuple
that only has primitive types (I only needed to test for `int`s, `str`s), or
primitive collections of primitive types (`list`s or `dict`s of `int`s, `str`s)
as properties. Take the following class for example.

```python
class SimplePythonObject:
    def __init__(self, a: int, b_list=None):
        self.a = a
        self.b_list = b_list or ['b1', 'b2']

my_spo = SimplePythonObject(1)
```

For the purposes of this post, it's a simple Python object because it's
properties are `a` of type `int` and `b_list` of type `List[str]`. Of course,
because of Python's dynamic typing, actually guaranteeing this might be more
trouble than it's worth, but I can guarantee it for my code at least.

## Getting the properties of a class instance

I'm going to use the
[`vars`](https://docs.python.org/3/library/functions.html#vars) function to get
all the properties as a `dict`. Unfortunately, this function won't work for
`namedtuples` (they use `<name>._asdict()`) so I'm going to use a small wrapper
function that will work for both simple classes and namedtuples.

```python
def todict(obj):
    """Convert both objects and namedtuples to dicts"""
    if hasattr(obj, '_asdict'):
        return obj._asdict()
    return vars(obj)
```

How to use this in Jinja? I could turn my simple classes into dicts before
passing them to `render_template` like so:

```python
    ...
    my_spo = SimplePythonObject(1)
    return render_template(todict(my_spo), ...)
```

But that's annoying and I'd rather do it on the template side, so I told Jinja2
about it:

```python
# Give Jinja the ability to turn things into dicts
# This will let us print objects easily
# https://stackoverflow.com/a/7226047/2958070
app.jinja_env.globals.update(todict=todict)
```

Now I don't have to babysit my `render_template` function:

```python
    ...
    my_spo = SimplePythonObject(1)
    return render_template(my_spo, ...)
```

## Rendering the object

Now it's fairly easy to define a macro in Jinja2 to print the object:

```html
{% raw %}
<!-- This needs todict(obj) to turn both classes and namedtuples into dicts -->
<!-- not recursive- I don't think I need recursion for my simple objects -->
{% macro render_object(obj) %}
  {% for key, value in todict(obj).items() %}
    <h3> {{ key }} </h3>
    <ul>
    {% if value is mapping %}
      {% for child_key, child_value in value.items() %}
        <li> {{ child_key }} : {{ child_value }}</li>
      {% endfor %}
    {% elif value is iterable and value is not string %}
      {% for child_value in value %}
        <li>{{ child_value }}</li>
      {% endfor %}
    {% else %}
      <li>{{ value }}</li>
    {% endif %}
    </ul>
  {% endfor %}
{% endmacro %}
{% endraw %}
```

I put this macro in a helper file: `templates/_macros.html`, and then reference
it everywhere else:

```html
{% raw %}
{% from "_macros.html" import render_object %}
<h2>My Simple Object</h2>
{{ render_object(my_spo) }}
{% endraw %}
```

Which produces the following HTML:

```html
    <h3> a </h3>
    <ul>

      <li>1</li>

    </ul>

    <h3> b_list </h3>
    <ul>


        <li>b1</li>

        <li>b2</li>


    </ul>
```

This is a sorta-ugly and brittle way to print objects, but it'll work until I
get some good output and it's saved me some time.
