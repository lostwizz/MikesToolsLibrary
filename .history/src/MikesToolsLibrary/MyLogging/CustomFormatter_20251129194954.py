#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 19:49:54"
###############################################################################


import logging
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator



from enum import Enum

class FormatMode(Enum):
    CONSOLE = 1
    FILE = 2
    JSON = 3


class CustomFormatter(logging.Formatter):

    # ANSI escape codes for colors
    COLORS = {
        logging.DEBUG: "\033[36m",  # Cyan
        logging.INFO: "\033[32m",  # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_FORMAT = (
        "%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)7s| %(message)s"
    )

    DEFAULT_FILE_FORMAT = (
        "%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)7s| %(message)s"
    )

    SPECIAL_CHARACTERS = {}

    # -----------------------------------------------------------------
    def __init__(self, fmt: str = None, datefmt: str = None, fmtMode= FormatMode.CONSOLE):
        # Call the parent constructor with format strings
        super().__init__(fmt or self.DEFAULT_FORMAT, datefmt or self.DEFAULT_DATEFMT)
        self.fmtMode = fmtMode

    # -----------------------------------------------------------------
    def format(self, record):
        # You can customize formatting here if needed
        msg = super().format(record)
        # Example: add a prefix
        match self.fmtMode:
            case FormatMode.CONSOLE:
                pass
            case forma:
                msg = f"[CustomFormatter] {msg}"
            case _:
                pass
        color = self.COLORS.get(record.levelno, self.RESET)
        # print (f" format==>{color=}")

        specialChar = self.SPECIAL_CHARACTERS.get(record.levelno, "")

        # return f"[Custom] {msg}"
        return f"{specialChar}{color}{msg}{self.RESET}{specialChar}"
