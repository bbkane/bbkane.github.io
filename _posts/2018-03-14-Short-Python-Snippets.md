---
layout: default
title: Short Python Snippets
---

This is just a collection of Python snippits that are too small for their own
posts. All code is for Python 3.

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

import argparse
import sys

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
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
    # do real work


if __name__ == "__main__":
    main()
```

## Zipping Files

The `shutil.make_archive` function is a bit hard to use. Here's my notes on it and some code to erase partially zipped files on exceptions. This function works well with `pathlib.Path`.

```python
try:
    # how params work:
    # change into root_dir
    # creating base_name.zip and adding base_dir to it
    # NOTE: not threadsafe! https://bugs.python.org/issue30511
    shutil.make_archive(
        base_name=base_name,
        format='zip',
        root_dir=root_dir,
        base_dir=base_dir.name,
        dry_run=False,
        logger=logger
    )
# KeyboardInterrupt doesn't inherit from Exception
except (Exception, KeyboardInterrupt):
    logger.exception(f'Exception! Deleting {dest_path_zip}')
    dest_path_zip.unlink()
    raise
```

## Creating Context Managers

Add the following two methods to create a context manager for a class:

This is useful when working with resources.

```python
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean()
```
