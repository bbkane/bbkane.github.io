+++
title = "On Errors in Repeated Functions"
date = 2016-12-16
updated = 2021-02-08
aliases = [ "2016/12/16/On-Errors-in-Repeated-Functions.html" ]
+++

Recently I found myself parsing several similar XML files in Python. The XML
had a deeply nested structure I wanted to get stuff out of, which means using
Python's [`xml.etree.ElementTree`'s](https://docs.python.org/3/library/xml.etree.elementtree.html) `find` and `findall` methods:

```python
for entry in root.find('this').find('this2').findall('entry'):
    first_thing = entry.text
    for next_entry in entry.find('this3').findall('next_entry'):
        thing_i_want = next_entry.find('thing_i_want').text
        other_thing = next_entry.find('junk').find('other_thing').text
```

With this bit of code, I want to grab a list of the text in a XML tree. It's
readable, succinct, and does no error handling. Each of those `find` calls can
return `None` if their element isn't found, and because I want to parse
multiple files I can't have that. Fortunately, for the most part, I want to
handle the errors in only two ways: assign `None` to the specific thing or quit
the whole parse and try again with the next one (whether that's at the file
level or at the XML branch level). The other problem is how to repeat this
error handling non-awkwardly.

One way to do handle the errors is with a `try/except` block:

```python
for entry in root.find('this').find('this2').findall('entry'):
    try:
            first_thing = entry.text
            for next_entry in entry.find('this3').findall('next_entry'):
                thing_i_want = next_entry.find('thing_i_want').text
                other_thing = next_entry.find('junk').find('other_thing').text
    except AttributeError:
        first_thing = None
        thing_i_want = None
        other_thing = None
        # or `continue` if the rest of the info isn't worth processing on error
```

The problem with this construct in this situation is that it's not granular
enough. I'd like to get the `first_thing` if possible and assign `None` to the
others if I can't get them. I could you multiple `try/except` blocks, but it
quickly becomes very unreadable.

Another way of doing it is to test everything before we find it:

```python
this = root.find('this')
if this is not None:
    this2 = this.find('this2')
    if this2 is not None:
        # iteration over None just skips the loop, so no need to check here
        for entry in this2.findall('entry')
            ...
```

The problems with this is obvious. Look at that nesting! I'd be halfway across
the screen before I got anything done! However, this pattern can be abstracted
into a function.

```python
def find_or_none(node, taglist):
    for tag in taglist:
        node = node.find(tag)
        if node is None:
            return node
    return node
```

This compressed error handling could also be implemented using exceptions. With
this punted error handling, the code becomes:

```python
this2 = find_or_none(root, ['this', 'this2'])
if this2 is not None:
    for entry  in this2.findall('entry')
        first_thing = entry.text
        next_entries = entry.find('this3')
        if next_entries is not None:
            for ...
```

This works, but there's one way I think it can be improved. Instead of checking
if something `is not None`, check if it `is None` and `break`, `continue`, or
`return` the heck away from the error.

With this change, I get fairly clean error handling:

```python
this2 = find_or_none(root, 'this', 'this2')
if this2 is None:
    return None
for entry in this2.findall('entry'):
    first_thing = entry.text
    this3 = entry.find('this3')
    if this3 is None:
        continue  # or `break` or `return` if that's appropriate
    for next_entry in this3.findall('next_entry'):
        thing_i_want = next_entry.find('thing_i_want')
        if thing_i_want is not None:
            thing_i_want = thing_i_want.text
        other_thing = find_or_none(next_entry, ['junk', 'other_thing'])
        if other_thing is not None:
            other_thing = other_thing.text
```

It's not pretty, but it works. Other techniques in other languages for this
kind of thing are C#'s [null-conditional
operator](https://msdn.microsoft.com/en-us/library/dn986595(v=vs.140).aspx) and
Functional Programming's [monadic error
handling](http://softwareengineering.stackexchange.com/questions/150837/maybe-monad-vs-exceptions).
There's also an excellent
[video](https://www.youtube.com/watch?v=E8I19uA-wGY&index=4&list=PLNVusuQqAKq4-2-a04SxI7Ss0B3w_Je8s&t=3222s)
including a functional approach to this this (and other) problems.
Rust also has a [monadic approach](http://www.codethatgrows.com/lessons-learned-from-rust-the-result-monad/) to error handling.
After I read/watch this stuff again, I'll probably be ashamed of this post, but until then, it's up :)

Update: I still find this useful for some things, but XML handling is best handled by XSLT! Use XSLT!
