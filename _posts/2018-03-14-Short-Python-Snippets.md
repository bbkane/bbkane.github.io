---
layout: default
title: Short Python Snippets
---

This is just a collection of Python snippits that are too small for their own posts

## Working with Python logging

The logging module is rather confusing, but I think this suffices for basic usage.

Logging is fun to set when netmiko isn't doing it's ***ing job and I hate
everything about computers and I seriously consider selling everything, growing
a mustache, and becoming a sheep farmer in New Zealand.

NOTE (2018-07-31): I haven't tested quite all of this logging section rewrite.

### Top level code

This is the code driving the program - `main.py` for me usually.

This sets the format for all loggers and turns on debug output for just the
loggers we care about.

```python
logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s -- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Selectively set levels for just my module so I'm not overwhelmed by logging
logging.getLogger('mymodule').setLevel(logging.DEBUG)
```

### Non top level code

In each file, make a new module level logger at the top:

```python
# file: mymodule.py

logger = logging.getLogger(__name__)
```

When you actually want to log something, use one of the following:

```python
logger.debug(msg)
logger.info(msg)
logger.warning(msg)
logger.error(msg)
logger.critical(msg)
```

Oddly, these methods don't take `print` style variable arguments. They have their own odd C-style format arguments, but it's probably easier just to use a single f-string.

If you need stack trace, add the `stack_info=True` argument.

Example:

```python
# this logs the message and the call stack
logger.info(f'{thing.value}, {random_var}', stack_info=True)
```

If logging in an an exception handler, use
[`logger.exception(msg)`](https://docs.python.org/3/library/logging.html#logging.Logger.exception). It automatically logs at ERROR level and adds exception trace info for you.

```python
try:
    foo(arg)
except MyError as e:
    # the exception stuff will be logged after the message
    logger.exception(f'arg: {arg}')
    raise
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
