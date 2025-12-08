#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 21:22:24"
###############################################################################


import logging
import pprint
from pprint import pformat
import json
from enum import Enum
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator




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

    # SPECIAL_CHARACTERS = {}
    SPECIAL_CHARACTERS = {
            logging.CRITICAL: "‼",
            logging.ERROR: "✖",
            logging.WARNING: "⚠",
            logging.INFO: "ℹ",
            logging.DEBUG: "…"
        }




    # -----------------------------------------------------------------
    def __init__(self, fmt: str = None, datefmt: str = None, fmtMode= FormatMode.CONSOLE):
        # Call the parent constructor with format strings
        super().__init__(fmt or self.DEFAULT_FORMAT, datefmt or self.DEFAULT_DATEFMT)
        self.fmtMode = fmtMode

    # -----------------------------------------------------------------
    def format(self, record):
        # You can customize formatting here if needed
    
            # Pretty-print BEFORE calling super().format()
        if isinstance(record.msg, (set, list, tuple)):
            record.msg = pformat(record.msg, indent=4, width=40, depth=5,
                                compact=False, underscore_numbers=True)
        elif isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg, indent=4, ensure_ascii=False)
        elif isinstance(record.msg, Enum):
            record.msg = f"{record.msg.__class__.__name__}.{record.msg.name} ({record.msg.value})"

        # if record.args:
        #     record.args = tuple(
        #         pformat(a, indent=4, width=40) if isinstance(a, (set, list, tuple, dict))
        #         else (f"{a.__class__.__name__}.{a.name} ({a.value})" if isinstance(a, Enum) else a)
        #         for a in record.args
        #     )

        # Now call the base formatter
        msg = super().format(record)

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
