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
import typing as t

__author__ = "Benjamin Kane"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)

LogLevel = t.Union[int, str]


def setup_global_logging(
        log_dir: str = 'logs',
        loggers: t.Iterable[LogLevel] = [logger, logging.getLogger(__package__)],
        log_level: LogLevel = logging.INFO,
        global_log_level: t.Optional[LogLevel] = None):
    """Set up basic logging to stderr and a log directory

    Use global_log_level to change levels on ALL logging
    loggers defaults to this module's logger and this module's package's logger
    See `logging.Logger.manager.loggerDict` for a list of all loggers
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logname = log_dir / datetime.now().strftime('%Y-%m-%d.%H.%M.%S.log')

    logging.basicConfig(
        format='# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s',
        level=global_log_level,
        handlers=(logging.StreamHandler(), logging.FileHandler(logname),)
    )

    if loggers is not None:
        for l in loggers:
            if l is not None:
                l.setLevel(log_level)

def main():
    setup_global_logging(log_level=logging.DEBUG)

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

# Opening the log

This alias automatically opens the last log.

```bash
alias view_last_log='vim -R -c "set syn=config" $(ls -t logs/*log | head -n1)'
```
