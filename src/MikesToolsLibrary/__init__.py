#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MikesToolsLibrary
-----------------
A collection of tools for advanced logging, formatting, and custom levels.




"""
__version__ = "0.1.2.00316-316-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 20:44:55"
###############################################################################


# import MikesToolsLibrary.MyLogging as mylog


# from .LoggerSetup import LoggerSetup
# from .CustomFormatter import CustomFormatter,FormatMode
# from .CustomLevels import CustomLevels, add_log_level
# from .log_decorator import log_decorator


from .MikesLogging import CustomFormatter
# from .MikesLogging.LoggingMode import LoggingMode


__all__ = ["CustomFormatter"]
# __all__ = ["CustomFormatter", "LoggingMode"]
