#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MyLogging
---------
Custom logging utilities: formatters, levels, and setup helpers.




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 20:42:16"
###############################################################################


# from .LoggerSetup import LoggerSetup
from .CustomFormatter import CustomFormatter
from .CustomLevels import CustomLevels
from .log_decorator import log_decorator, log_decoratorPlain
# from .LoggingMode import LoggingMode

__all__ = [
    "CustomFormatter",
    # "LoggingMode",
    "add_log_level",
    "LoggerSetup",
    "log_decorator",
    "log_decoratorPlain",
]
