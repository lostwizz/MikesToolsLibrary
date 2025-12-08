#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 21:14:26"
###############################################################################


import logging

class CustomFormatter(logging.Formatter):
    DEFAULT_FORMAT = "%(name)s | %(levelname)s | %(message)s"
    
    DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, fmt: str = None, datefmt: str = None):
        # Call the parent constructor with format strings
        super().__init__(fmt or self.DEFAULT_FORMAT, datefmt or self.DEFAULT_DATEFMT)

    def format(self, record):
        # You can customize formatting here if needed
        msg = super().format(record)
        # Example: add a prefix
        return f"[Custom] {msg}"

