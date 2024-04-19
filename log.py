import functools
import inspect
import logging
import os
import sys

from loguru import logger


class __InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def __setup_loger():
    debug_mode = os.getenv('DEBUG_MODE').lower() == 'true'
    if debug_mode:
        level = 'DEBUG'
    else:
        level = 'INFO'
    logger.remove()
    logger.add(sys.stdout, level=level)
    logger.add("logs/log.log",
               level='INFO',
               retention="1 week",
               enqueue=True,
               )

    logging.getLogger('aiogram').setLevel(level)
    logging.getLogger('aiogram').addHandler(__InterceptHandler())

    logger.info('Logger is successfully configured')


def log_this(*, entry=True, exit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = await func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
