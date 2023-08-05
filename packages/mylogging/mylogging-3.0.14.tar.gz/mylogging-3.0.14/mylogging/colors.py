"""Module for colors. Contain functions for coloring messages by level (yellow, red, grey...)
or function that color python code."""

from __future__ import annotations
from typing import Union

# Lazy imports
# import pygments
# from pygments.lexers.python import PythonTracebackLexer
# from pygments.formatters import TerminalFormatter

USE_COLORS = True

color_palette = {
    "reset": "\x1b[0m",  # "reset"
    # "INFO": "\x1b[38;21m",  # "grey"
    # "DEBUG": "\x1b[38;21m",  # "grey"
    "WARNING": "\x1b[33;21m",  # "yellow"
    "ERROR": "\x1b[31;21m",  # "red"
    "CRITICAL": "\x1b[31;1m",  # "bold_red"
}


def colorize(message: str, level: str = "WARNING", use: Union[bool, None] = None) -> str:
    """Add color to message based on level - usally warnings and errors, to know what is internal error on first sight.
    There is global config.COLORIZE value that can be configured, so it's not necessary to pass as argument.

    Args:
        message (str): Any string you want to color.
        level (str, optional): "INFO" and "DEBUG" not colored, "WARNING": yellow, "ERROR": red
            or "CRITICAL": more red. Defaults to "WARNING".
        use (Union[bool, None], optional): It's possible to turn on and off colors with one config
            variable to keep syntax simple. Defaults to None.

    Returns:
        str: Message in yellow color. Symbols added to string cannot be read in some terminals.
            If config COLORIZE is False, it return original string.

    Example:
        >>> message = "Hello there"
        >>> colored_message = colorize(message, use=True)
        >>> colored_message
        '\\x1b[33;21m Hello there \\x1b[0m'
    """

    if use is None:
        use = USE_COLORS

    if not use or level in ["DEBUG", "INFO"]:
        return message
    else:
        return f"{color_palette[level]} {message} {color_palette['reset']}"


def colorize_traceback(traceback_str: str) -> str:
    """Colorize traceback to be more readable.

    Args:
        traceback_str (str): Get from traceback with traceback.format_exc().

    Returns:
        str: String with added symbols cause that string will be colorized.

    Example:
        >>> import traceback
        ...
        >>> try:
        ...     1/0
        ... except ZeroDivisionError:
        ...     colorize_traceback(traceback.format_exc())
        'Traceback (most recent call last):\\n  File \\x1b[36m"<doctest mylogging.colors.colorize_traceback[1]>"\\x1b[39;49;00m...'
    """
    import pygments
    from pygments.lexers.python import PythonTracebackLexer
    from pygments.formatters import TerminalFormatter

    return pygments.highlight(traceback_str, PythonTracebackLexer(), TerminalFormatter(style="friendly"),)
