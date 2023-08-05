"""Module for custom Logger class - wrapper that is internally used. You can also use it, even if 90% of users will not."""

from __future__ import annotations
from typing import Union, Any
import logging
import warnings
from pathlib import Path

from .colors import colorize
from . import _misc


class MyLogger:
    def __init__(self) -> None:

        self.datefmt = "%Y-%m-%d %H:%M"
        self.logger = logging.getLogger("application")
        self.logger.addFilter(self.ContextFilter())

    def init_formatter(
        self,
        FORMATTER_FILE_STR: str,
        FORMATTER_CONSOLE_STR: str,
        OUTPUT: Union[str, Path, None],
        LEVEL: str,
        STREAM: Any = None,
        TO_LIST: Union[None, list[str]] = None,
    ):
        self.FORMATTER_FILE_STR = FORMATTER_FILE_STR
        self.FORMATTER_CONSOLE_STR = FORMATTER_CONSOLE_STR
        self.OUTPUT = OUTPUT
        self.STREAM = STREAM
        self.LEVEL = LEVEL
        self.TO_LIST = TO_LIST
        self.get_handler()
        self.logger.setLevel(getattr(logging, LEVEL))

    def get_handler(self) -> None:
        """If FORMATTER_FILE_STR, FORMATTER_CONSOLE_STR or OUTPUT change, it need new handler.
        First update new value in Mylogger object, then call this function."""
        while self.logger.handlers:
            self.logger.removeHandler(self.logger.handlers[0])

        if self.STREAM:
            handler = logging.StreamHandler(stream=self.STREAM)
            handler.setFormatter(self.get_formatter(self.FORMATTER_CONSOLE_STR))
            # handler.setLevel(getattr(logging, self.LEVEL))
            self.logger.addHandler(handler)

        if self.OUTPUT == "console":
            handler = logging.StreamHandler()
            handler.setFormatter(self.get_formatter(self.FORMATTER_CONSOLE_STR))
            # handler.setLevel(getattr(logging, self.LEVEL))
            self.logger.addHandler(handler)

        elif self.OUTPUT:
            handler = logging.FileHandler(self.OUTPUT)
            handler.setFormatter(self.get_formatter(self.FORMATTER_FILE_STR))
            # handler.setLevel(getattr(logging, self.LEVEL))
            self.logger.addHandler(handler)

        if isinstance(self.TO_LIST, list):
            handler = self.SaveHandler(self.TO_LIST)
            self.logger.addHandler(handler)

    def get_formatter(self, format_str: str) -> logging.Formatter:
        return logging.Formatter(format_str, datefmt=self.datefmt, style="{",)

    def log_and_warn_from_lists(self, logs_list: list = [], warnings_list: list = []) -> None:
        for record in logs_list:
            for h in self.logger.handlers:
                if isinstance(h, self.SaveHandler):
                    raise RuntimeError("\n\nYou have to close redirect before log from list.\n\n")
                if not _misc.filter_out(record.msg, "WARNING"):
                    h.emit(record)

        for i in warnings_list:
            warnings.showwarning(**i)

    class ContextFilter(logging.Filter):
        def filter(self, record):
            record.funcName = "" if record.funcName == "<module>" else f"in function {record.funcName}"
            record.levelname = colorize(record.levelname, record.levelname)
            return True

    class SaveHandler(logging.Handler):
        def __init__(self, TO_LIST) -> None:
            self.TO_LIST = TO_LIST
            super().__init__()

        def emit(self, record) -> None:
            self.TO_LIST.append(record)


my_logger = MyLogger()
