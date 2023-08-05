"""
This module is internal module for mylogging library. It's not supposed to be used by user.
"""

from __future__ import annotations
from typing import Callable, Any, Union, Callable
import warnings
from pathlib import Path
import logging
from dataclasses import dataclass

from typing_extensions import Literal

from ._config import config
from . import colors
from .logger_module import my_logger


printed_info = set()
user_filters = []
original_formatwarning = warnings.formatwarning
level_str_to_int = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


logging_functions = {
    "DEBUG": my_logger.logger.debug,
    "INFO": my_logger.logger.info,
    "WARNING": my_logger.logger.warning,
    "ERROR": my_logger.logger.error,
    "CRITICAL": my_logger.logger.critical,
}


class CustomWarning(UserWarning):
    pass


def filter_out(message: str, level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]) -> bool:
    """Based on configuration pass or deny log based on filter and level.

    Args:
        message (str): Used message. Necessari for 'once' filter.
        level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]): Used level.

    Returns:
        bool: True if message should not be passed (has lover level or already been and filter is 'once').
    """
    # All logging can be turned off
    if config.FILTER == "ignore":
        return True

    # Check if sufficient level

    if level_str_to_int[level] < level_str_to_int[config.LEVEL]:
        return True

    message = config._repattern.sub("", message)[:150]

    # Filters
    if config.FILTER == "once":
        if message in printed_info:
            return True
        else:

            printed_info.add(message)

    for i in config.BLACKLIST:
        if i in message:
            return True

    return False


def log_warn(message: str, level: str, showwarning_details: bool = True, stack_level: int = 3) -> None:
    """If OUTPUT is configured, it will log message into defined path. If OUTPUT == "console" is configured, it will
    log or warn.

    Args:
        message (str): Any string content of warning.
        level (str): 'INFO' or something else, generated automatically from __init__ module.
        showwarning_details (bool, optional): Whether to override warnings details display.
            After warning, default one will be again used. Defaults to True.
        stack_level (int, optional): How many calls to log from error. Defaults to 3.
    """

    if config.FILTER == "error":
        raise RuntimeError(message)

    if config._console_log_or_warn == "log":
        try:
            # From version 3.8
            logging_functions[level](message, stacklevel=stack_level)
        except TypeError:
            logging_functions[level](message)

    else:
        warnings.formatwarning = formatwarning_detailed if showwarning_details else formatwarning_stripped

        CustomWarning.__name__ = level
        CustomWarning.level = level

        warnings.warn(message, stacklevel=stack_level, category=CustomWarning)

        warnings.formatwarning = original_formatwarning


class StringObject(str):
    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self) -> str:
        return f"{self.message}"


def objectize_str(message: str) -> StringObject:
    """Make a class from a string to be able to apply escape characters and colors if raise.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """

    return StringObject(message)


def formatwarning_detailed(message, category, filename, lineno, *args, **kwargs):
    """Function that can override warnings printed info."""
    return (
        f"\n\n{colors.colorize(category.__name__, level=category.level)}from {filename}:{lineno} {message}\n"
    )


def formatwarning_stripped(message, *args, **kwargs):
    """Function that can override warnings printed info."""
    return f"{message}\n"


@dataclass
class RedirectedLogsAndWarnings:

    logs: list[logging.LogRecord]
    warnings: list[dict[str, Any]]
    showwarning_backup: Callable
    OUTPUT_backup: Union[str, Path, None]
    STREAM_backup: Any

    def close_redirect(self):
        warnings.showwarning = self.showwarning_backup
        config.OUTPUT = self.OUTPUT_backup
        config.STREAM = self.STREAM_backup
        config.TO_LIST = None


def redirect_logs_and_warnings_to_lists(
    used_logs: list[logging.LogRecord], used_warnings: list
) -> RedirectedLogsAndWarnings:
    """For example if using many processes with multiprocessing, it may be beneficial to log from one place.
    It's possible to log to variables (logs as well as warnings), pass it to the main process and then log it
    with workings filter etc.

    To log stored logs and warnings, use

    Args:
        used_logs (list): List where logs will be stored
        used_warnings (list): List where warnings will be stored

    Returns:
        RedirectedLogsAndWarnings: Object, where you can reset redirect. Logs and warnings you already have
        from inserted parameters.
    """
    showwarning_backup = warnings.showwarning
    OUTPUT_backup = config.OUTPUT
    STREAM_backup = config.STREAM

    def custom_warn(message, category, filename, lineno, file=None, line=None):
        used_warnings.append(
            {
                "message": message,
                "category": category,
                "filename": filename,
                "lineno": lineno,
                "file": file,
                "line": line,
            }
        )

    warnings.showwarning = custom_warn
    config.OUTPUT = None
    config.STREAM = None
    config.TO_LIST = used_logs

    return RedirectedLogsAndWarnings(
        logs=used_logs,
        warnings=used_warnings,
        showwarning_backup=showwarning_backup,
        OUTPUT_backup=OUTPUT_backup,
        STREAM_backup=STREAM_backup,
    )


def filter_warnings(level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING") -> Callable:
    """If filter (once) in warnings from 3rd party libraries don't work, this implements own filter.

    Args:
        level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], optional): Used level in filter. Defaults to "WARNING".

    Returns:
        Callable: Original warning function. Reset original warning settings with `reset_warnings_filter()`
        and value returned from this function.

    Note:
        Default warnings function is overwritten, you should revert default finally with `reset_warnings_filter`
    """

    backup = warnings.showwarning

    def custom_warn(message, category, filename, lineno, file=None, line=None):
        custom_message = f"In {filename} - {str(category)}: {str(message)}"
        if not filter_out(custom_message, level):
            backup(message, category, filename, lineno, file=file, line=line)

    warnings.showwarning = custom_warn

    return backup


def reset_warnings_filter(backup: Callable) -> None:
    """Reset custom warnings filter.

    Args:
        backup (Callable): Function returned from `filter_warnings`.
    """
    warnings.showwarning = backup
