---
layout: default
title: Inline Multiline Python Strings
---

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
