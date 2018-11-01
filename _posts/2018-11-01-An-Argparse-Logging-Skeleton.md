---
layout: default
title: An Argparse-Logging Skeleton
---

In previous posts, I've posted skeletons for scripts using `argparse` and
scripts using `logging`. This script combines both boilerplate recipes and
should be useful for simple command line apps.

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import logging
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


# create a module level logger for main
logger = logging.getLogger(__name__)


def setup_global_logging(
        log_dir='logs',
        log_level=logging.DEBUG,
        global_log_level=None,
        loggers=(logging.getLogger(__package__ or __name__),)):
    """Set up basic logging

    log_dir: str = log directory name. Will be created if necessary
    log_level: int = level to set passed loggers too
    global_log_level: int = root logger level (propagates to children)
    loggers: Iterable[Logging.logger] = loggers to set to level

    loggers defaults to a tuple of either the package (if in a package), or this module
    TODO: test the package or module idea
    See `logging.Logger.manager.loggerDict` for a list of all loggers
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    logname = log_dir / datetime.now().strftime('%Y-%m-%d.%H.%M.%S.log')

    logging.basicConfig(
        format='# %(asctime)s %(levelname)s %(name)s %(filename)s:%(lineno)s\n%(message)s',
        level=global_log_level,  # Dangerous
        handlers=(
            logging.StreamHandler(),
            logging.FileHandler(logname),
        )
    )

    # Selectively set levels for just some modules so I'm not overwhelmed by logging
    # See `logging.Logger.manager.loggerDict` for a list of all loggers
    if loggers is not None:
        for l in loggers:
            l.setLevel(log_level)


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # TODO: add some real args

    # logging options
    parser.add_argument(
        '--log_dir',
        default='logs',
        help='defaults to "logs"'
    )
    parser.add_argument(
        '--log_level',
        default='INFO',
        help='Set code-specified loggers to this. Defaults to INFO'
    )
    parser.add_argument(
        '--global_log_level',
        default=None,
        help='Set all loggers to this. Defaults to None'
    )

    parsed_args = parser.parse_args(*args, **kwargs)

    # Extra validation
    try:
        parsed_args.log_level = getattr(logging, parsed_args.log_level)
        assert isinstance(parsed_args.log_level, int)
    except AttributeError:
        raise SystemError(f'Incorrect log level: log_level: {parsed_args.log_level!r}')

    try:
        # None is a special value for logging.basicConfig
        if parsed_args.global_log_level is not None:
            parsed_args.global_log_level = getattr(logging, parsed_args.global_log_level)
            assert isinstance(parsed_args.global_log_level, int)
    except AttributeError:
        raise SystemError(f'Incorrect log level: global_log_level: {parsed_args.global_log_level!r}')

    return parsed_args


def main():
    args = parse_args()

    setup_global_logging(
        log_dir=args.log_dir,
        log_level=args.log_level,
        global_log_level=args.global_log_level,
    )

    # ...do actual work, and be content that it will be logged appropriately
    logger.info("I'm too loggy for my tree")


if __name__ == "__main__":
    main()
```
