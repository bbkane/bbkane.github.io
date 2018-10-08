---
layout: default
title: Short Python Snippets
---

This is just a collection of Python snippits that are too small for their own posts

## Inline Multiline Strings

This is a quick post on inline multiline strings. I like to use the following style:


```python
from textwrap import dedent


def main():
    query = dedent("""
    first line
    second line
    """).strip()

    print(repr(query))

if __name__ == '__main__':
    main()

# 'first line\nsecond line'
```

So it prints it without the preceding and trailing newlines and without the indentation to make it line up with the rest of the function

## Pretty-printing JSON

```python
json.dump(obj, sys.stdout, indent=2, sort_keys=True)
```

or

```python
print(json.dumps(obj, indent=2, sort_keys=True))
```

I kind of prefer the first version, even if it involves an extra `sys` import because it's easy to change the dump to a file (though it's not much harder to add the `file` argument to `print` either...).

```python
with open('file.json', 'w') as fp:
    json.dump(obj, fp, indent=2, sort_keys=True)
```

## Argparse template

This code is for shorter one file scripts that need command line arguments with
the [argparse](https://docs.python.org/3/library/argparse.html) library.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

import argparse
import sys

__doc__ = """
<description>
Examples:
    `{prog}`
Help:
Please see Benjamin Kane for help.
Code at <repo>
""".format(prog=sys.argv[0])


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # TODO: add some args
    return parser.parse_args(*args, **kwargs)


def main():
    args = parse_args()
    ... # do work


if __name__ == "__main__":
    main()
```
