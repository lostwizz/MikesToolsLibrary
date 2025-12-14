#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomFormatter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 22:59:03"
###############################################################################


import sys
import logging
import pprint
from pprint import pformat
import json
from enum import Enum, IntFlag, unique, auto

import traceback
from .log_decorator import log_decorator
from .LoggingMode import LoggingMode


sys.stdout.reconfigure(encoding="utf-8")


###############################################################################
###############################################################################
class CustomFormatter(logging.Formatter):
    DEFAULT_TEXT_MSG = "~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~"

    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m",
    }
    RESET = "\033[0m"
    SPECIAL_CHARACTERS = {
        logging.CRITICAL: "🔴☠🔴",
        logging.ERROR: "❌❌ ",
        logging.WARNING: "⚠ ",
        logging.INFO: "ℹ ",
        logging.DEBUG: "……",
    }
    # """
    # 25: "🔍",   # TRACE custom level
    # 26: "📊",   # DATA custom level
    # 27: "✔",   # SUCCESS custom level
    # 28: "🛠",   # CONFIG custom level
    # 29: "🔒",   # SECURITY custom level
    # """

    IP=""
    uName=""

    # -----------------------------------------------------------------
    def __init__(self, fmt=None, datefmt=None, fmtMode=LoggingMode.CONSOLE, style="%"):
        super().__init__(
            fmt or "%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)7s| %(message)s",
            datefmt or "%Y-%m-%d %H:%M:%S",
            style=style,
        )
        self.fmtMode = fmtMode
        self.style = style

    # -----------------------------------------------------------------
    # def _has_placeholders(self, msg: str) -> bool:
    #     if self.style == "%":
    #         return (
    #             "%" in msg
    #         )  # simple heuristic; enough for deciding to let logging interpolate
    #     elif self.style == "{":
    #         return "{" in msg and "}" in msg
    #     elif self.style == "$":
    #         return "$" in msg
    #     return False

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
        elif isinstance(record.msg, Enum):
            record.msg = self._pp(record.msg)

        # if not record.msg or record.msg == CustomFormatter.DEFAULT_TEXT_MSG:
        #     if CustomFormatter.MARKER_LOW <= record.levelno <= CustomFormatter.MARKER_HIGH:
        #         record.msg = f"{record.levelno - 300:1d}{CustomFormatter.DEFAULT_TEXT_MSG}"

        # If args exist but message has no placeholders, fold pretty-printed args into the message
        original_args = record.args
        try:
            if (
                original_args
                and isinstance(record.msg, str)
                # and not self._has_placeholders(record.msg)
            ):

                # print ( f"{original_args=}")
                if len(original_args) == 1:
                    appended = self._pp(original_args[0])
                else:
                    # appended = pformat(
                    #     tuple(self._pp(a) for a in original_args), indent=2, width=100
                    # )
                    sep = "\n"
                    appended = sep.join(str(self._pp(a)) for a in original_args)
                    record.msg = f"{record.msg}{sep}{appended}"
                    record.args = ()  # prevent logging from doing msg % args

            if not hasattr(record, "user_id"):
                record.user_id = self.uName
            else:
                if not self.uName:
                    self.uName = record.user_id
                    
            if not hasattr(record, "ip"):
                record.ip = "-"

            # Build base message
            msg = super().format(record)

            # limit the file name to FILENAME_SIZE length
            FILENAME_SIZE = 15
            record.filename = record.filename.replace(".py", "")
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

            # INCOMPLETE
            # Style per mode
            match self.fmtMode:
                case LoggingMode.FILE | LoggingMode.ROTATINGFN | LoggingMode.TIMEDROTATOR:
                    color = ""
                    special = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                    end = ""
                case LoggingMode.CONSOLE:
                    color = self.COLORS.get(record.levelno, self.RESET)
                    special = self.SPECIAL_CHARACTERS.get(record.levelno, "")
                    end = self.RESET
                case LoggingMode.SMTP:
                    color = ""
                    end = ""
                    special = ""
                case LoggingMode.JSON:
                    log_obj = {
                        "time": self.formatTime(record, self.datefmt),
                        "level": record.levelname,
                        "filename": record.filename,
                        "funcName": record.funcName,
                        "lineno": record.lineno,
                        "message": record.getMessage(),
                    }
                    return json.dumps(log_obj, ensure_ascii=False)

                case _:
                    pass

            # return f"{special}{color}{msg}{end}{special}"
            return f"{color}{msg}{end}{special}"
        finally:
            # Restore args to avoid side effects across handlers/formatters
            record.args = original_args

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

# -----------------------------------------------------------------
if __name__ == '__main__':
    """
    This is the main function that runs when the script is executed directly.
    It sets up the logger and demonstrates the usage of the CustomFormatter class.
    """
    print("You should not run this file directly, it is a module to be imported.")
    sys.exit(-99)
