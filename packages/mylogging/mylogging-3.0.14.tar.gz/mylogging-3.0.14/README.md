# mylogging

[![Python versions](https://img.shields.io/pypi/pyversions/mylogging.svg)](https://pypi.python.org/pypi/mylogging/) [![PyPI version](https://badge.fury.io/py/mylogging.svg)](https://badge.fury.io/py/mylogging) [![Downloads](https://pepy.tech/badge/mylogging)](https://pepy.tech/project/mylogging) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mylogging.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mylogging/context:python) [![Documentation Status](https://readthedocs.org/projects/mylogging/badge/?version=latest)](https://mylogging.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mylogging/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mylogging)


My python logging-warning module. It logs to console or to file based on configuration.

1) It's automatically colorized and formatted to be more readable and noticeable (you can immediately see what errors are yours)
2) It's possible to control logs and warnings behaviour (ignore, once, always) as in warnings.
3) It's possible to filter messages by level (INFO, DEBUG, WARNING, ERROR, CRITICAL) as in logging.

Motivation for this project is to be able to have one very simple code base for logging and warning at once
and setup logging at one place, not in every project.

You can use one code for logging apps running on server (developers see what happens on server) and the same
code for printing info and warnings from developed library.

## Links

Official documentation - https://mylogging.readthedocs.io/

Official repo - https://github.com/Malachov/mylogging


## Installation

Python >=3.6 (Python 2 is not supported).

Install just with::

    pip install mylogging


## Output

This is how the results of examples below look like in console.

<p align="center">
<img src="docs/source/_static/logging.png" width="620" alt="Logging output example"/>
</p>

For log file, just open example.log in your IDE.
This is how the results in log file opened in VS Code look like.

<p align="center">
<img src="docs/source/_static/logging_file.png" width="620" alt="Logging output example"/>
</p>

## Examples

Library is made to be as simple as possible, so configuration should be easy (you don't need
to configure anything actually)... Just setup path to log file (will be created if not exists).
If you do not set it up, log to console will be used.
Change FILTER (defaults to once) and LEVEL (defaults to WARNING) if you need.
Then syntax is same as in logging module. Functions debug, info, warn, error and critical are available.

<!--phmdoctest-setup-->
```python
import mylogging

mylogging.config.LEVEL = "WARNING"
mylogging.warn("I am interesting warning.")
```

You can log your errors with traceback, where you set level as input parameter. You can use traceback also with no parameters, traceback type will be used as heading then.

```python
try:
    print(10 / 0)

except ZeroDivisionError:
    mylogging.traceback("Maybe try to use something different than 0.")

mylogging.fatal("This is fatal", caption="You can use captions")
```

Print function omit the details like file name, line etc.

```python
mylogging.print("No details about me.")
```

There are also another functions you can use: `return_str` will return edited string (Color, indent and around signs).
Use case for that is mostly raising your errors. You can see in one second, whether raise is yours or from imported library.

<!--phmdoctest-mark.skip-->
```python
raise ModuleNotFoundError(mylogging.return_str("Try pip install...", caption="Library not installed error"))
```

This is result
<p align="center">
<img src="docs/source/_static/return_str.png" width="620" alt="Logging output example"/>
</p>

Another function is for ignoring specified warnings from imported libraries. Global warnings
settings are edited, so if you use it in some library that other users will use, don't forget to 
reset user settings after end of your call with reset_outer_warnings_filter() or use it in
witch.catch_warnings(): block.

Sometimes only message does not work, then ignore it with class and warning type

```python
ignored_warnings = ["mean of empty slice"]
ignored_warnings_class_type = [
    ("TestError", FutureWarning),
]

mylogging.outer_warnings_filter(ignored_warnings, ignored_warnings_class_type)

mylogging.reset_outer_warnings_filter()
```

If somebody is curious how it looks like on light color theme, here it goes...

<p align="center">
<img src="docs/source/_static/logging_white.png" width="620" alt="Logging output example"/>
</p>

## Config

Some config, that can be configured globally for not having to use in each function call.

Config values has docstrings, so description should be visible in IDE help.

`OUTPUT` - Whether log to file or to console. 'console' or path to file (string or pathlib.Path).
Defaults by "console"

`LEVEL` - Set level of severity that will be printed, e.g. DEBUG, ERROR, CRITICAL. Defaults to 'WARNING'.

`FILTER` - If the same logs, print it always, once or turn all logging off.
Possible values "ignore", "once", "always" or "error". Defaults to "once".

Usually that's everything you will set up. If you need different formatting of output, you can define

`BLACKLIST` - You can filter out some specific messages by content.

`FORMATTER_CONSOLE_STR` or `FORMATTER_FILE_STR` with for example::

    "{asctime} {levelname} " + "{filename}:{lineno}" + "{message}"

Rest options should be OK by default, but it's all up to you of course: You can set up for example

`AROUND` - Whether separate logs with line breaks and ==== or shrink to save space. Defaults to True.

`COLORIZE` - Possible options: [True, False, 'auto']. Colorize is automated. If to console, it is
colorized, if to file, it's not (.log files can be colorized by IDE). Defaults to 'auto'.

`TO_LIST` - You can save all the logs in the list and log it later (use case: used in multiprocessing
processes to be able to use once filter)

`STREAM` - If you want to use a stream (for example io.StringIO)

logger
=======

It's possible to use logger in any other way if you need (though it's usually not necessary), you can find used my_logger in logger_module. There are also used filters and handlers.

multiprocessing
===============

If using in subprocesses, to be able to use filters (just once), it's possible to redirect logs and warnings, send as results as log later in main process

```python
logs_list = []
warnings_list = []

logs_redirect = mylogging.redirect_logs_and_warnings_to_lists(logs_list, warnings_list)

logs_redirect.close_redirect()

mylogging.my_logger.log_and_warn_from_lists(logs_list, warnings_list)
```
