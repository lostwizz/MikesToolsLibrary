#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-01 18:16:03"
###############################################################################



# from .LoggerSetup import LoggerSetup
from .CustomFormatter import CustomFormatter,FormatMode
from .CustomLevels import  add_log_level      
# from .log_decorator import log_decorator

__all__ = ["CustomFormatter", "FormatMode", "add_log_level"]