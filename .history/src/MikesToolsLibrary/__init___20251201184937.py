#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MikesToolsLibrary
-----------------
A collection of tools for advanced logging, formatting, and custom levels.




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-01 18:49:37"
###############################################################################


# import MikesToolsLibrary.MyLogging as mylog


# from .LoggerSetup import LoggerSetup
# from .CustomFormatter import CustomFormatter,FormatMode
# from .CustomLevels import CustomLevels, add_log_level
# from .log_decorator import log_decorator


from .MyLogging import CustomFormatter, FormatMode


__all__ = ["CustomFormatter", "FormatMode", "add_log_level\]
