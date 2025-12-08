#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 20:48:58"
###############################################################################


import logging
import pprint
import json
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

        if isinstance(msg, (set, list, tuple)):
            msg = pprint.pformat(msg, indent=4, width=40)
            
        elif isinstance(record.msg, dict):
            # JSON style for dicts
            msg = json.dumps(record.msg, indent=2, ensure_ascii=False)

        elif isinstance(record.msg, Enum):
            msg = f"{record.msg.__class__.__name__}.{record.msg.name} ({record.msg.value})"


        print ( f"+++>")


        # 
        match self.fmtMode:
            case FormatMode.FILE:
                color =""
                specialChar = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                endChar =""
            case FormatMode.CONSOLE:
                color = self.COLORS.get(record.levelno, self.RESET)
                specialChar = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                endChar = self.RESET
            case _:
                pass

        return f"{specialChar}{color}{msg}{endChar}{specialChar}"
