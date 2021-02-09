+++
title = "Auto-printing Python Classes"
date = 2017-12-19
updated = 2017-12-26
aliases = [ "2017/12/19/Auto-Printing-Python-Classes.html" ]
+++

This article examines different ways to generate `__repr__` functions. But,
just to be clear, here are my recommendations in order:

- Immutable data:
  - [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
    (Python >= 3.5)
  - [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple)
- Mutable data:
  - [`dataclasses.dataclass`](https://www.python.org/dev/peps/pep-0557/)
    (Python >= 3.7 or you don't mind using `pip` to get it)
  - [`argparse._AttributeHolder`](https://github.com/python/cpython/blob/3.6/Lib/argparse.py#L109)
    (Python >= 3.2 and you don't mind using its non-public class)
  - `generic_repr` or `GenericReprBase` (read on for implementation)


Before you program in Python for too long, you start to work with classes. In
most day to day programming, a class is just a container for similarly named
variables ( very similar to a `struct` in C ). Here's an example `Song` class:

```python
class SongVanilla:

    def __init__(self, title: str, length: int): self.title = title
    self.length = length
```

This is a perfectly functional object, even if the `__init__` method seems a
little redundant. However if you print it, you something similar to this
ugliness:

```python
s = SongVanilla('mysong', 300) print(s)

# <__main__.SongVanilla object at 0x10be016a0>
```

The default `__repr__` method for classes is very unhelpful. Let's add one:


```python
class SongVanilla:

    def __init__(self, title: str, length: int): self.title = title
    self.length = length

    def __repr__(self): return f'SongVanilla({self.title!r},
    {self.length!r})'
```

This does get us a nice print method:

```python
s = SongVanilla('mysong', 300) print(s)

# SongVanilla('mysong', 300)
```

Now the redundancy is even more transparent: All we wanted was a way to group
`title` and `length` and get reasonable ways to access and print instance
variables. With this method, we have to type `title` 4 times just to get that!
And we have to do this with every member variable want to add. Want to add
`author`? Prepare for an early case of arthritis. And this gets even worse if
we decide to add any of the comparison functions or other double underscore
methods to our class.

## NamedTuple

Fortunately, there are better ways to do this. If you *know your data will be
immutable*, Python's standard library comes with `namedtuple` in the
`collections` module that does the right thing.


```python
from collections import namedtuple

SongCollectionsNamedTuple = namedtuple('SongCollectionsNamedTuple', ['title', 'length'])
```

This gives us a printing function that does the expected:

```python
s = SongCollectionsNamedTuple('mysong', 300)
print(s)

# SongCollectionsNamedTuple(title='mysong', length=300)
```

So namedtuples are a nice solution to this problem assuming your data in the
class won't change, but you can't really typehint them, and their odd
declaration syntax means adding a docstring looks funny. Fortunately,
`typing.NamedTuple` fixes most of these problems:


```python
from typing import NamedTuple

class SongTypingNamedTuple(NamedTuple):
    title: str
    length: int
```

This looks nice, but also gets us a good `__repr__`. The immutability
requirement still applies.


```python
s = SongTypingNamedTuple('mysong', 300)
print(s)

# SongTypingNamedTuple(title='mysong', length=300)
```

In code that supports it, I recommend `typing.NamedTuple` unconditionally over
`collections.namedtuple`.

## static repr

If you have mutable data, another option is to use Python's metaprogramming
abilities to create generic `__repr__` and `__init__` methods for our classes
and then call them from each instance via inheritance or function call. I'm
only going to focus on the `__repr__` method for this post.

Let's dissect  what happens in `__repr__`.

We need:
- The name of the class - provided by `type(self).__name__` - and
- The member variables of the class - provided by `vars(self)`, which returns
  them in a dictionary.

Using these two bits of information, let's build a `generic_repr(instance) ->
str` function:


```python
def generic_repr(instance) -> str:
    name = type(instance).__name__
    vars_list = [f'{key}={value!r}'
                 for key, value in vars(instance).items()]
    vars_str = ', '.join(vars_list)
    return f'{name}({vars_str})'

s = SongVanilla('mysong', 300)
print(generic_repr(s))

# SongVanilla(title='mysong', length=300)
```

Unfortunately, this function won't work on the immutable
`collections.namedtuple` or `typing.NamedTuple`. It relies on attributes they
don't have (specifically the `__dict__` attribute for `vars()`). That's not
really a problem, though, because they supply their own `__repr__`s. Now that
we have this function, we can call it from a class's `__repr__` method:

```python
def __repr__(self):
    return generic_repr(self)
```

or bake it into a base class and inherit from it:

```python
class GenericReprBase:

    def __repr__(self):
        name = type(self).__name__
        vars_list = [f'{key}={value!r}'
                     for key, value in vars(self).items()]
        vars_str = ', '.join(vars_list)
        return f'{name}({vars_str})'


class SongInheritedRepr(GenericReprBase):

    def __init__(self, title: str, length: int):
        self.title = title
        self.length = length

s = SongInheritedRepr('mysong', 300)
print(s)
# SongInheritedRepr(title='mysong', length=300)
```

This is basically what `argparse` does in it's private
[`_AttributeHolder`](https://github.com/python/cpython/blob/3.6/Lib/argparse.py#L109)
class.

## Dataclasses

In Python 3.7 ( coming mid-2018 ), the `dataclasses` module has been added to
the standard library. Python 3 users can `pip install dataclasses` to use it
right now. Use the `@dataclass` decorator provided by this module to
automatically give your class `__init__`, `__repr__`, and more goodies you can
read about in the [PEP](https://www.python.org/dev/peps/pep-0557/). For mutable
data, this is almost certainly the best option. Here's an example:


```python
from dataclasses import dataclass

@dataclass
class SongDataClass:
    title: str
    length: int

s = SongDataClass('mysong', 300)
print(s)

# SongDataClass(title='mysong', length=300)
```

The only issues I can think of is that, with this option, IDEs can have a hard
time informing you of what arguments they need exactly for the `__init__`
function of the class. Also if you're doing something clever with your classes
(for example, some crazy [SQLAlchemy
operator](https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/sql/operators.py)),
you should probably buckle down and write `__repr__` yourself.

In summary, Python offers many ways to generate printable classes- from adding
`__repr__` manually to every class to standard library solutions to third party
solutions to writing your own generic solution, you shouldn't have to repeat
yourself very often at all
