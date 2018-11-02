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
import typing as t

__author__ = "Benjamin Kane"
__version__ = "0.1.0"
__doc__ = f"""
<description>
Examples:
    `{sys.argv[0]}`
Help:
Please see Benjamin Kane for help.
Code at <repo>
"""


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


def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # TODO: add app args here

    # logging options
    parser.add_argument(
        '--log_dir',
        default='logs',
        help='defaults to "logs"'
    )
    parser.add_argument(
        '--log_level',
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
        default='INFO',
        help='Set code-specified loggers to this. Defaults to INFO'
    )
    parser.add_argument(
        '--global_log_level',
        default=None,
        help='Set all loggers to this. Defaults to None'
    )

    parsed_args = parser.parse_args(*args, **kwargs)
    return parsed_args


def main():
    args = parse_args()

    setup_global_logging(
        log_dir=args.log_dir,
        log_level=args.log_level,
        global_log_level=args.global_log_level,
    )

    # ...do actual work, and be content that it will be logged appropriately
    logger.debug("I'm too loggy for my tree")
    logger.info("I'm too loggy for my tree")
    logger.warning("I'm too loggy for my tree")
    logger.error("I'm too loggy for my tree")
    logger.critical("I'm too loggy for my tree")


if __name__ == "__main__":
    main()
```
