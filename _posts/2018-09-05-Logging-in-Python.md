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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import logging

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def setup_global_logging(
    log_dir: str = "logs",
    loggers=[logging.getLogger("__main__"), logging.getLogger(__package__)],
    level=logging.INFO,
    global_level=None,
    stream_level=logging.INFO,
):
    """Set up basic logging to stderr and a log directory

    loggers: defaults to this module's logger and this module's package's logger
    level: level to log your code (as defined by `loggers` parameter). Defaults to logging.INFO
    global_level: change levels on logging not included in `loggers` (including 3rd party libaries). It defaults to logging.ERROR.
    stream_level: change level of stderr logging specifically (so it can ignore more verbose logging going to a file)

    See `logging.Logger.manager.loggerDict` for a list of all loggers
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logname = log_dir / datetime.datetime.now().strftime("%Y-%m-%d.%H.%M.%S.log")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_level)

    logging.basicConfig(
        format="# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s\n",
        level=global_level,
        handlers=(stream_handler, logging.FileHandler(logname)),
    )

    if loggers is not None:
        for l in loggers:
            if l is not logging.getLogger():
                l.setLevel(level)


def main():
    setup_global_logging(level=logging.DEBUG)

    # ...do actual work, and be content that it will be logged appropriately
    logger.debug("I'm too loggy for my tree")
    logger.info("I'm too loggy for my tree")
    logger.warning("I'm too loggy for my tree")
    logger.error("I'm too loggy for my tree")
    logger.critical("I'm too loggy for my tree")


if __name__ == "__main__":
    main()
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

# Logging Function Calls

Sometimes when debugging, it can be helpful to log all calls, arguments, and results of a function. I have a little decorator to do this. Just decorate the function at definition, and all of that will be logged. This function was inspired by David Beazley's talk [The Fun of Reinvention](https://youtu.be/5nXmq1PsoJ0). As a side note, David Beazley is a mad genius and this talk is a brilliant testament to that.

```python
from inspect import signature
from functools import wraps


def log_calls(logger, message='', sep=' '):
    """Decorator to log calls with an optional message

    @log_calls(logger, 'wtf?')
    def f(a, b):
        ...
    """

    if message:
        message = message + sep

    def wrap(func):
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):

            bound = sig.bind(*args, **kwargs)

            argstr = [f'{arg}={value!r}' for arg, value in
                      bound.arguments.items()]
            argstr = ', '.join(argstr)

            ret = func(*args, **kwargs)

            logger.debug(f'{message}{func.__name__}({argstr}) -> {ret!r}')
            return ret
        return wrapper
    return wrap
```

# Formatting [requests](http://docs.python-requests.org/en/master/) calls

I love the `requests` library, but oddly, it doesn't offer a nice way to print most parts of requests and responses. See my [pocket_backup](https://github.com/bbkane/Random-Scripts/blob/master/pocket_backup.py) for a decent set of functions to deal with this. I need to turn my experiences with `requests` into their own blog post...

# Opening the log

This alias automatically opens the last log.

```bash
alias view_last_log='vim -R -c "set syn=config" $(ls -t logs/*log | head -n1)'
```
