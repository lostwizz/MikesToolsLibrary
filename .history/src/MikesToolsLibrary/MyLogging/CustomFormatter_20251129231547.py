#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 23:15:47"
###############################################################################


import logging
import pprint
from pprint import pformat
import json
from enum import Enum
import traceback
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


import sys
sys.stdout.reconfigure(encoding="utf-8")

###############################################################################
###############################################################################
class FormatMode(Enum):
    CONSOLE = 1
    FILE = 2
    JSON = 3


###############################################################################
###############################################################################
class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m",
    }
    RESET = "\033[0m"
    SPECIAL_CHARACTERS = {
        logging.CRITICAL: "🔴☠🔴☠🔴",
        logging.ERROR: "❌❌❌❌ ",
        logging.WARNING: "⚠ ",
        logging.INFO: "ℹ ",
        logging.DEBUG: "……",
    }

    # -----------------------------------------------------------------
    def __init__(self, fmt=None, datefmt=None, fmtMode=FormatMode.CONSOLE, style="%"):
        super().__init__(fmt or "%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)7s| %(message)s",
                            datefmt or "%Y-%m-%d %H:%M:%S",
                            style=style)
        self.fmtMode = fmtMode
        self.style = style

    # -----------------------------------------------------------------
    def _has_placeholders(self, msg: str) -> bool:
        if self.style == "%":
            return "%" in msg  # simple heuristic; enough for deciding to let logging interpolate
        elif self.style == "{":
            return "{" in msg and "}" in msg
        elif self.style == "$":
            return "$" in msg
        return False

    # -----------------------------------------------------------------
    def _pp(self, obj):
        if isinstance(obj, dict):
            try:
                return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)
            except TypeError:
                return pformat(obj, indent=2, width=100, compact=False)
        if isinstance(obj, (list, tuple, set)):
            return pformat(obj, indent=2, width=100, compact=False)
        if isinstance(obj, Enum):
            return f"{obj.__class__.__name__}.{obj.name} ({obj.value})"
        return obj

    # -----------------------------------------------------------------
    def format(self, record):
        # Pretty-print msg if it's a complex object
        if isinstance(record.msg, (set, list, tuple)):
            record.msg = self._pp(record.msg)
        elif isinstance(record.msg, dict):
            record.msg = self._pp(record.msg)
        # elif isinstance(record.msg, Enum):
        elif isinstance(record.msg, 'enum.EnumType'):
            record.msg = self._pp(record.msg)

        # If args exist but message has no placeholders, fold pretty-printed args into the message
        original_args = record.args
        try:
            if original_args and isinstance(record.msg, str) and not self._has_placeholders(record.msg):
                if len(original_args) == 1:
                    appended = self._pp(original_args[0])
                else:
                    appended = pformat(tuple(self._pp(a) for a in original_args), indent=2, width=100)
                record.msg = f"{record.msg} {appended}"
                record.args = ()  # prevent logging from doing msg % args


            # Build base message
            msg = super().format(record)

            # limit the file name to FILENAME_SIZE length
            FILENAME_SIZE = 15
            record.filename = record.filename.replace('.py','')
            if len(record.filename) > FILENAME_SIZE:
                record.filename = record.filename[:FILENAME_SIZE]
            else:
                record.filename = record.filename.rjust(FILENAME_SIZE)

            # Limit funcName to the first 15 characters
            FUNCNAME_SIZE = 18  
            if len(record.funcName) > FUNCNAME_SIZE:
                record.funcName = record.funcName[:FUNCNAME_SIZE]
            else:
                record.funcName = record.funcName.rjust(FUNCNAME_SIZE)

            ## handle exceptions and traceback
            record.message = record.getMessage()
            if record.exc_info:
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)

            # Style per mode
            match self.fmtMode: 
                case FormatMode.FILE:
                    color = ""
                    special = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                    end = ""
                case FormatMode.CONSOLE:
                    color = self.COLORS.get(record.levelno, self.RESET)
                    special = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                    end = self.RESET
                case FormatMode.JSON:
                    color = ""
                    special = ""
                    end = ""
                case _:
                    pass

            return f"{special}{color}{msg}{end}{special}"
        finally:
            # Restore args to avoid side effects across handlers/formatters
            record.args = original_args

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
