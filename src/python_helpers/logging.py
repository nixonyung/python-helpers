# (ref.) [How can I include the relative path to a module in a Python logging statement?](https://stackoverflow.com/questions/52582458/how-can-i-include-the-relative-path-to-a-module-in-a-python-logging-statement)
import logging
import logging.config
import os


def relpathname_filter(record: logging.LogRecord):
    cwd = os.getcwd()
    if record.pathname.startswith(cwd):
        record.relpathname = f".{record.pathname[len(cwd) :]}"
    else:
        record.relpathname = record.pathname

    return True


def init_logging(show_debug: bool, enable_rich: bool):
    # (ref.) [LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)
    # (ref.) [How to specify a log handler class with a required argument using dictConfig syntax?](https://stackoverflow.com/questions/54565623/how-to-specify-a-log-handler-class-with-a-required-argument-using-dictconfig-syn)
    if enable_rich:
        from rich.traceback import install as rich_traceback_install

        rich_traceback_install()

        format = "%(message)s  [%(name)s at %(relpathname)s:%(lineno)d]"
        handler_class = "rich.logging.RichHandler"
        # (ref.) [rich.logging](https://rich.readthedocs.io/en/stable/reference/logging.html#logging)
        handler_args = {
            "omit_repeated_times": False,
            "show_path": False,
        }
    else:
        format = "%(asctime)s %(levelname)-8s %(message)s  [%(name)s at %(relpathname)s:%(lineno)d]"
        handler_class = "logging.StreamHandler"
        handler_args = {}

    loggers = {
        "": {  # root logger
            "level": "NOTSET" if show_debug else "INFO",
            "handlers": ["default"],
        },
    }
    # (ref.) [Modern Python logging](https://www.youtube.com/watch?v=9L77QExPmI0)
    # (ref.) [Configuration dictionary schema](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "standard": {
                    "format": format,
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "default": {
                    "()": handler_class,
                    "formatter": "standard",
                    "filters": [relpathname_filter],
                    **handler_args,
                },
            },
            "loggers": loggers,
        }
    )
