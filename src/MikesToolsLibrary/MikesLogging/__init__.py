#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MyLogging
---------
Custom logging utilities: formatters, levels, and setup helpers.




"""
__version__ = "0.1.2.00322-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-24 19:32:02"
###############################################################################


from .log_decorator import log_decorator, log_decoratorPlain
from .LoggerSetup import get_logger

__all__ = [
    "log_decorator",
    "log_decoratorPlain",
    "get_logger",
]


