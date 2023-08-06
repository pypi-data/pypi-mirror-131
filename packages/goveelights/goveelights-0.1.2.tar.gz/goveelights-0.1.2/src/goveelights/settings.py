"""
goveelights.logging

This module contains
"""

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,

    "formatters": {
        "brief": {
            "class": "logging.Formatter",
            "datefmt": "%I:%M:%S",
            "format": "%(levelname)s - %(name)s - %(message)s"
        },
        "verbose": {
            "class": "logging.Formatter",
            "datefmt": "%I:%M:%S",
            "format": "%(levelname)s - [%(process)d] - %(threadName)s - %(name)s - %(module)s:%(funcName)s - %(lineno)d: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "brief",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "level": "INFO",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "verbose",
            "filename": "/tmp/file_handler.log",
            "mode": "a",
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "goveelights.hub": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
        "goveelights.color": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
        "goveelights.device": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
        "goveelights.client": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    # "root": {
    #     "handlers": ["console"],
    #     "level": "DEBUG"
    # }
}
