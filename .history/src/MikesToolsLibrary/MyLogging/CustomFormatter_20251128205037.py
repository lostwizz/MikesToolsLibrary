#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 20:50:37"
###############################################################################


import logging


class CustomFormatter(logging.Formatter):

    def __init__():
        super().__init__()
        # Custom initialization code can go here

    def format(self, record):
        
        # Example: simple custom formatting
        msg = super().format(record)
        return f"[Custom] {msg}"


