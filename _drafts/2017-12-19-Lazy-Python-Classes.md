---
layout: default
title: Lazy Python Classes
---

TODO: make this more cohesive
- good Introduction, summary 
- add dataclasses

Before you program in Python for too long, you start to work with classes. In
most day to day programming, a class is just a container for similarly named
variables ( very similar to a `struct` in C ). Here's an example `Song` class:


    class SongCLass

        def __init__(self, title: str, length: int):
            self.title = title
            self.length = length

This is a perfectly functional object, even if the `__init__` method seems a little redundant. However if you print it, you something similar to this ugliness:

    s = SongVanilla('mysong', 300)
    print(s)

    # <__main__.SongVanilla object at 0x10be016a0>

The default `__repr__` method for classes is very unhelpful. Let's add one:


    class SongVanilla:

        def __init__(self, title: str, length: int):
            self.title = title
            self.length = length

        def __repr__(self):
            return f'SongVanilla({self.title!r}, {self.length!r})'

This does get us a nice print method:

    s = SongVanilla('mysong', 300)
    print(s)

    # SongVanilla('mysong', 300)

Now the redundancy is even more transparent: All we wanted was a way to group
`title` and `length` and get reasonable ways to access and print instance
variables. With this method, we have to type `title` 4 times just to get that!
And we have to do this with every member variable want to add. Want to add
`author`? Prepare for an early case of arthritis. And this get's even worse if we decide to add any of the comparison functions or other double underscore methods to our class

## NamedTuple

Fortunately, there are better ways to do this. If you *know your data will be
immutable*, Python's standard library comes with `namedtuple` in the
`collections` module that does the right thing.


    from collections import namedtuple

    SongCollectionsNamedTuple = namedtuple('SongCollectionsNamedTuple', ['title', 'length'])

This gives us a printing function that does the expected:

    s = SongCollectionsNamedTuple('mysong', 300)
    print(s)

    # SongCollectionsNamedTuple(title='mysong', length=300)

So namedtuples are a nice solution to this problem assuming your data in the class won't change, but you can't really typehint them, and their odd declaration syntax means adding a docstring looks funny. Fortunately, `typing.NamedTuple` fixes most of these problems:


    from typing import NamedTuple

    class SongTypingNamedTuple(NamedTuple):
        title: str
        length: int

This looks nice, but also gets us a good `__repr__`. The immutability requirement still applies.


    s = SongTypingNamedTuple('mysong', 300)
    print(s)

    # SongTypingNamedTuple(title='mysong', length=300)

In code that supports it, I recommend `typing.NamedTuple` unconditionally over `collections.namedtuple`

## static repr

If you have mutable data, another option is to use Python's metaprogramming abilities to create generic `__repr__` and `__init__` methods for our classes and then call them from each instance via inheritance or function call. I'm only going to focus on the `__repr__` method for this post.

Let's dissect  what happens in `__repr__`.

We need: 
- The name of the class - provided by `type(self).__name__` - and
- The member variables of the class - provided by `vars(self)` as a dictionary

Using these two bits of information, let's build a `generic_repr(instance) -> str` function:


    def generic_repr(instance) -> str:
        name = type(instance).__name__
        vars_list = [f'{key}={value!r}'
                     for key, value in vars(instance).items()]
        vars_str = ', '.join(vars_list)
        return f'{name}({vars_str})'

    s = SongVanilla('mysong', 300)
    print(generic_repr(s))

Unfortunately, this function won't work on the immutable
`collections.namedtuple` or `typing.NamedTuple`. It relies on attributes they
don't have (specifically the `__dict__` attribute for `vars()`). That's not
really a problem, though, because they supply their own `__repr__`s. Now that
we have this function, we can call it from a class's `__repr__` method:

    def __repr__(self):
        return generic_repr(self)

or bake it into a base class and inherit from it:

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

This is basically what `argparse` does in it's private
[`_AttributeHolder`](https://github.com/python/cpython/blob/3.6/Lib/argparse.py#L109)
class.

## Dataclasses
