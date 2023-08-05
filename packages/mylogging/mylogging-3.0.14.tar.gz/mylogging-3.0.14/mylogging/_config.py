"""
This is internal module that has class Config and create and instance config that is imported
in __init__.py, so you will find documentation there...
"""

from __future__ import annotations
from typing import Union, Any
from pathlib import Path
import re
import logging

from typeguard import typechecked
from typing_extensions import Literal

from .logger_module import my_logger
from . import colors


@typechecked
class Config:
    """Do not edit class variables, but created instance config in this module...
    All variables has own docstrings.
    """

    def __init__(self):
        self._OUTPUT = "console"
        self._LEVEL = "WARNING"
        self._AROUND = "auto"
        self._used_around = True
        self._COLORIZE = "auto"
        self._FILTER = "once"
        self._FORMATTER_FILE_STR = "{asctime} {levelname} {filename}:{lineno}{message}"
        self._FORMATTER_CONSOLE_STR = "\n{levelname} from {pathname}:{lineno} {funcName}{message}"
        self._BLACKLIST = []
        self._TO_LIST = None
        self._STREAM = None

        # Next variables are used mostly internally, configure only if you know what are you doing
        self._console_log_or_warn = (
            "log"  # If log, logging module will trigger to stderr, if "warn", warning will be raised
        )
        self._repattern = re.compile(
            r"[\W_]+"
        )  # This is regex that edit logs for filter to be able to use 'once' for example also for tracebacks
        my_logger.init_formatter(self.FORMATTER_FILE_STR, self.FORMATTER_CONSOLE_STR, self.OUTPUT, self.LEVEL)

    @property
    def FILTER(self) -> Literal["ignore", "once", "always", "error"]:
        """
        Define what to do with logs, that repeats.

        Only first 100 symbols of message will be used if using once.

        Do not affect warnings library. Use `warnings.simplefilter("__FILTER__", Warning)` if you need.
        Options: ["ignore", "once", "always", "error"]

        Defaults to: 'once'

        "error" means that application stop on log as on error.
        """
        return self._FILTER

    @FILTER.setter
    def FILTER(self, new: Literal["ignore", "once", "always", "error"]) -> None:
        self._FILTER = new

    @property
    def AROUND(self) -> Literal[True, False, "auto"]:
        """
        True: separate logs with ===== and line breaks for better visibility.

        False: keep message short

        "auto": False if OUTPUT == "file/path", True if OUTPUT == "console"

        Defaults to: "auto"
        """
        return self._AROUND

    @AROUND.setter
    def AROUND(self, new: Literal[True, False, "auto"]) -> None:
        if new == "auto":
            self._used_around = True if self.OUTPUT == "console" else False
        else:
            self._used_around = new
        self._AROUND = new

    @property
    def FORMATTER_FILE_STR(self) -> str:
        """You can edit used formatter if you want. Just go to source of logging.Formatter to see
        all possible options. This is only main string of formatter class (style="{" is used).
        Message itself is formatted in return_str function. This is for formatter if logging to console.

        Defaults to: "{asctime} {levelname} {filename}:{lineno}{message}"

        """
        return self._FORMATTER_FILE_STR

    @FORMATTER_FILE_STR.setter
    def FORMATTER_FILE_STR(self, new: str) -> None:
        self._FORMATTER_FILE_STR = new
        my_logger.FORMATTER_FILE_STR = new
        my_logger.get_handler(),

    @property
    def FORMATTER_CONSOLE_STR(self) -> str:
        """You can edit used formatter if you want. Just go to source of logging.Formatter to see
        all possible options. This is only main string of formatter class (style="{" is used).
        Message itself is formatted in return_str function. This is for formatter if logging to console.

        Defaults to: "\n{levelname}from {pathname}:{lineno} {funcName}{message}"
        """
        return self._FORMATTER_CONSOLE_STR

    @FORMATTER_CONSOLE_STR.setter
    def FORMATTER_CONSOLE_STR(self, new: str):
        self._FORMATTER_CONSOLE_STR = new
        my_logger.FORMATTER_CONSOLE_STR = new
        my_logger.get_handler(),

    @property
    def COLORIZE(self) -> Literal[True, False, "auto"]:
        """Whether colorize results.

        Options: [True, False, 'auto']

        Defaults to: 'auto'

        'auto' means color if to console, not color if to file.
        """
        return self._COLORIZE

    @COLORIZE.setter
    def COLORIZE(self, new: Literal[True, False, "auto"]):
        if new == "auto":
            if self.OUTPUT == "console":
                colors.USE_COLORS = True
            else:
                colors.USE_COLORS = False
        else:
            colors.USE_COLORS = new
        self._COLORIZE = new

    @property
    def OUTPUT(self) -> Union[str, Path, None]:
        """Whether log to file or to console. If None, nor console, nor file will be
        used (STREAM logs to a variable is still possible).

        Options: ["console", pathlib.Path, r"path/to/file", None]

        Defaults to: "console"
        """
        return self._OUTPUT

    @OUTPUT.setter
    def OUTPUT(self, new: Union[str, Path, None]) -> None:
        self._OUTPUT = new
        self.AROUND = self.AROUND  # If auto, change it
        self.COLORIZE = self.COLORIZE  # If auto, change it
        my_logger.OUTPUT = new
        my_logger.get_handler()

    @property
    def STREAM(self) -> Any:
        """Whether save all logs to stream (that stream can be variable).

        Example: io.StringIO()

        Defaults to: None
        """
        return self._STREAM

    @STREAM.setter
    def STREAM(self, new: Any):
        self._STREAM = new
        my_logger.STREAM = new
        my_logger.get_handler()

    @property
    def BLACKLIST(self) -> list[str]:
        """Log messages can be filtered out. Only part of message can be used.
        Numeric letters are removed in message comparison, to be able to filter
        out same errors from different places. Only last 100 messages is kept in memory...

        Example: ["Matrix inversion failed"]

        Defaults to: None"""
        return self._BLACKLIST

    @BLACKLIST.setter
    def BLACKLIST(self, new: Union[None, list[str]]):
        self._BLACKLIST = [self._repattern.sub("", i) for i in new]

    @property
    def TO_LIST(self) -> Union[None, list[str]]:
        """You can store all logs in list and then emit when you want.

        Defaults to: None"""
        return self._TO_LIST

    @TO_LIST.setter
    def TO_LIST(self, new: Union[None, list]):
        self._TO_LIST = new
        my_logger.TO_LIST = new
        my_logger.get_handler()

    @property
    def LEVEL(self) -> Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        """Logs can be filtered out based on log severity.

        Options: ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        Defaults to: "INFO"

        Also WARN and FATAL can be used, but will be converted to WARNING and CRITICAL.
        """
        return self._LEVEL

    @LEVEL.setter
    def LEVEL(self, new: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]):
        new = new.upper()

        if new == "FATAL":
            new = "CRITICAL"

        if new == "WARN":
            new = "WARNING"

        if self.OUTPUT:
            my_logger.logger.setLevel(getattr(logging, new))
        self._LEVEL = new


config = Config()
