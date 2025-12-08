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
__updated__ = "2025-12-01 19:01:02"
###############################################################################



# from .LoggerSetup import LoggerSetup
from .CustomFormatter import CustomFormatter,FormatMode
from .CustomLevels import  CustomLevels
from .log_decorator import log_decorator, log_decoratorPlain

__all__ = ["CustomFormatter", "FormatMode", "add_log_level", "LoggerSetup", "log_decorator", "log_decoratorPlain"]