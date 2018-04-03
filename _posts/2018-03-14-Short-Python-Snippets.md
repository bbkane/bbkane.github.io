---
layout: default
title: Short Python Snippets
---

## Enable INFO Level Python Logging

This is fun to set when netmiko isn't doing it's ***ing job and I hate
everything about computers and I seriously consider selling everything, growing
a mustache, and becoming a sheep farmer in New Zealand.

```python
logging.basicConfig(level=logging.DEBUG)
```

## Inline Multiline Strings

This is a quick post on inline multiline strings. I like to use the following style:


```python
from textwarp import dedent


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
