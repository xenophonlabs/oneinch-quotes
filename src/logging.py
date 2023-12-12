"""
Custom logging config and useful aliases for logging.
Copied from https://github.com/curveresearch/curvesim/blob/main/curvesim/logging.py.
"""

__all__ = ["get_logger"]

import datetime
import logging
import logging.config
import os
from typing import Dict, List

# -- convenient parameters to adjust for debugging -- #
DEFAULT_LEVEL = "info"
USE_LOG_FILE = True
# --------------------------------------------------- #

LEVELS = {
    "critical": logging.CRITICAL,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
if USE_LOG_FILE:
    os.makedirs(LOG_DIR, exist_ok=True)

__dt_string = datetime.datetime.now().strftime("%Y%m%d")
LOG_FILEPATH = os.path.join(LOG_DIR, __dt_string + ".log")

LOGGING_FORMAT = "[%(levelname)s][%(asctime)s][%(name)s]: %(message)s"
MULTIPROCESS_LOGGING_FORMAT = (
    "[%(levelname)s][%(asctime)s][%(name)s]-%(process)d: %(message)s"
)


# FIXME: need a function to update the config after module initialization
HANDLERS = ["console", "file"] if USE_LOG_FILE else ["console"]

CUSTOM_LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": MULTIPROCESS_LOGGING_FORMAT, "datefmt": "%H:%M:%S"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 10 * 1024 * 1024,
            "mode": "a",
            "backupCount": 10,
            "filename": LOG_FILEPATH,
            "formatter": "standard",
            "delay": True,
        },
    },
    "loggers": {
        "": {
            "handlers": HANDLERS,
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# 3rd party loggers that we want to largely ignore
silenced_loggers: List[str] = [
    "matplotlib",
    "asyncio",
    "rlp",
    "parso",
    "web3",
    "urllib3",
]
configured_loggers: Dict[str, dict] = CUSTOM_LOGGING_CONFIG["loggers"]
for name in silenced_loggers:
    configured_loggers[name] = {
        "handlers": HANDLERS,
        "level": "WARNING",
        "propagate": False,
    }

logging.config.dictConfig(CUSTOM_LOGGING_CONFIG)


def get_logger(logger_name: str, level: str | int = DEFAULT_LEVEL) -> logging.Logger:
    """
    Ensures logging config is loaded and allows us
    to make various customizations.
    """
    logger = logging.getLogger(logger_name)
    if isinstance(level, str):
        level = LEVELS[level.strip().lower()]
    logger.setLevel(level)

    return logger
