---
layout: default
title: Logging in Python
---

The [logging](https://docs.python.org/3/library/logging.html) module is rather
confusing, so I use it with code similar to the following.

Logging is fun to add when netmiko isn't doing it's ***ing job and I hate
everything about computers and I seriously consider selling everything, growing
a mustache, and becoming a sheep farmer in New Zealand.

NOTE (2018-07-31): I haven't tested quite all of this logging section rewrite.

### Top level code

This is the code driving the program - `main.py` for me usually.

This sets the format for all loggers and turns on debug output for just the
loggers we care about.

```python
# filename: main.py

# create a module level logger for main
logger = logging.getLogger(__name__)

def main():

    # make sure this directory path exists
    logname = datetime.datetime.now().strftime('data/%Y-%m-%d.%H.%M.%S.log')
    # I want to log all loggers to stderr and this file
    # This isn't needed if you just want to log to stderr
    handlers = [
        logging.StreamHandler(),
        logging.FileHandler(logname),
    ]

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s -- %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        # level=logging.DEBUG,  # only if you want all logging possible from everywhere
        handlers=handlers
    )

    # Selectively set levels for just some modules so I'm not overwhelmed by logging
    # See `logging.Logger.manager.loggerDict` for a list of all loggers
    logger.setLevel(logging.DEBUG)
    logging.getLogger('dns_providers').setLevel(logging.DEBUG)


    ... # do actual work, and be content that it will be logged appropriately
```

### Non top level code

In each file, make a new module level logger at the top (note: we did this for main too above)

```python
# filename: mymodule.py

# create a logger for module mymodule
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
