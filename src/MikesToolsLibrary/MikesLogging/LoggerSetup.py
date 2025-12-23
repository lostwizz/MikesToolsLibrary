#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py


to use this -- add it to the path
set PYTHONPATH=D:\_Python_Projects\MikesToolsLibrary\src;%PYTHONPATH%

# TODO:
# COMMENT:
# NOTE:
# USEFULL:
# LEARN:
# RECHECK
# INCOMPLETE
# SEE NOTES
# POST
# HACK
# FIXME
# BUG
# [ ] something to do
# [x]  i did sometrhing


"""
__version__ = "0.1.2.00213-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-16 19:35:14"
###############################################################################

from encodings.punycode import T
import sys
import json
import socket
import getpass

import logging
from logging.handlers import SMTPHandler

# from logging.handlers import NullHandler, StreamHandler, FileHandler
# from logging.handlers import WatchedFileHandler
from logging.handlers import BaseRotatingHandler, RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

# from logging.handlers import SocketHandler
# from logging.handlers import DatagramHandler
# from logging.handlers import NTEventLogHandler
# from logging.handlers import MemoryHandler, BufferingHandler
# from logging.handlers import HTTPHandler
# from logging.handlers import QueueHandler   #, SimpleQueue
# from logging.handlers import QueueListener

from .log_decorator import log_decorator
from .CustomLevels import CustomLevels
from .CustomFormatter import CustomFormatter
from .ExcludeLevelFilter import ExcludeLevelFilter
from .LoggingMode import LoggingMode


###############################################################################
###############################################################################
class LoggerSetup:
    """
    Unified logger setup:
    - Console handler with CustomFormatter (color, pretty-print)
    - File handler with plain text logs
    - Support for custom levels via add_custom_level
    - Optional filters (exclude certain levels)
    """

    _logger = None

    # -----------------------------------------------------------------
    def __init__(
        self,
        name: str = "MikesToolsLibrary",
        level: int = logging.DEBUG,
        logfile: str = "app.log",
        modes: LoggingMode = LoggingMode.CONSOLE | LoggingMode.ROTATINGFN,
        maxBytes=100_000_000,
        backupCount=100,
        interval=1,
        when="midnight",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handlers_by_mode = {}

        # Avoid duplicate handlers if re-instantiated
        if not self.logger.handlers:

            # INCOMPLETE
            handlers = {
                LoggingMode.CONSOLE: lambda: self.setupConsoleHandler(level),
                LoggingMode.FILE: lambda: self.setupFileHandler(level, logfile),
                LoggingMode.SMTP: lambda: self.setupSMTPHandler(name),
                LoggingMode.JSON: lambda: self.setupJSONHandler(level, logfile),
                LoggingMode.ROTATINGFN: lambda: self.setupRotationFileHandler(
                    level, logfile=logfile, maxBytes=maxBytes, backupCount=backupCount
                ),
                LoggingMode.TIMEDROTATOR: lambda: self.setupTimedRotationFileHandler(
                    level,
                    logfile,
                    interval=interval,
                    when=when,
                    backupCount=backupCount,
                ),
                # LoggingMode.MEMORY: lambda: None,
                # LoggingMode.SYSLOG: lambda: None,
                # LoggingMode.HTTP: lambda: None,
                # LoggingMode.QUEUE: lambda: None,
                # LoggingMode.DATABASE: lambda: None,
                # LoggingMode.CLOUD: lambda: None,
                # LoggingMode.EXTERNAL: lambda: None,
            }

            for mode, setup in handlers.items():
                if modes & mode:
                    handler = setup()
                    self.logger.addHandler(handler)
                    self.handlers_by_mode[mode] = handler

        self.add_special_levels(self.logger)


        
    # -----------------------------------------------------------------
    def get_logger(self):
        return self.logger

    # -----------------------------------------------------------------
    def setupConsoleHandler(self, level):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%H:%M:%S",
                fmtMode=LoggingMode.CONSOLE,
            )
        )
        ch.addFilter(ExcludeLevelFilter(LoggingMode.CONSOLE))
        return ch

    # -----------------------------------------------------------------
    def setupFileHandler(self, level, logfile):
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(LoggingMode.FILE))
        return fh

    # -----------------------------------------------------------------
    def setupJSONHandler(self, level, logfile):
        fh = logging.FileHandler("JSON" + logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.JSON,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(LoggingMode.JSON))
        return fh

    # -----------------------------------------------------------------
    def setupSMTPHandler(self, name):

        mail_handler = SMTPHandler(
            mailhost=("mail.merrett.ca", 587),
            fromaddr="public@merrett.ca",
            toaddrs=["public@merrett.ca"],
            subject="Application Error - " + name,
            credentials=("public@merrett.ca", "2]soaDOv;E;9"),
            secure=(),
        )

        # mail_handler = SMTPHandler(
        #     mailhost=("localhost", 1025),
        #     fromaddr="test@example.com",
        #     toaddrs=["admin@example.com"],
        #     subject="Test Log Email - " + name
        # )

        mail_handler.addFilter(ExcludeLevelFilter(LoggingMode.SMTP))
        mail_handler.setLevel(999)

        return mail_handler

    # ---------------------------------------------------------------
    def setupRotationFileHandler(
        self, level, logfile, maxBytes=100_000_000, backupCount=25
    ):
        fh = RotatingFileHandler(
            filename=logfile,
            encoding="utf-8",
            maxBytes=maxBytes,
            backupCount=backupCount,
        )
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)15s|%(filename)16s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(LoggingMode.ROTATINGFN))
        return fh

    # -----------------------------------------------------------------
    def setupTimedRotationFileHandler(
        self, level, logfile, when="d", interval=7, backupCount=25
    ):
        fh = TimedRotatingFileHandler(
            filename=logfile,
            encoding="utf-8",
            interval=interval,
            backupCount=backupCount,
            when=when,
        )
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(LoggingMode.ROTATINGFN))
        return fh

    # -----------------------------------------------------------------
    def force_rollover(self, mode: LoggingMode = LoggingMode.ALL):
        """Force rollover for handlers matching the given mode."""
        for flag, handler in self.handlers_by_mode.items():
            if mode & flag and hasattr(handler, "doRollover"):
                handler.doRollover()

    # -----------------------------------------------------------------
    @staticmethod
    def reset_state():
        # Clear custom filters
        ExcludeLevelFilter.Filters.clear()
        # Remove custom levels
        for level_name in list(logging._nameToLevel.keys()):
            if level_name not in logging._levelToName.values():
                logging._nameToLevel.pop(level_name, None)
        # Clear loggerDict
        logging.Logger.manager.loggerDict.clear()

    # -----------------------------------------------------------------
    @classmethod
    def includeUserNameAndIP(cls, overrideName=None, overrideIP=None):

        username = overrideName if overrideName else getpass.getuser()

        if overrideIP:
            local_ip = overrideIP
        else:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

        # print(f"setting to: {username=} {local_ip=}")
        cls._logger.pirate(f"☠Setting Username: '{username}' and IP: '{local_ip}'",extra={"user_id": username, "ip": local_ip, "special":True})

    # -----------------------------------------------------------------
    @classmethod
    def add_special_levels(cls, logger):
        """Add the predefined custom log levels by delegating to CustomLevels."""
        CustomLevels.addMyCustomLevels(logger)

    # -----------------------------------------------------------------
    @classmethod
    def add_level(
        cls, level_name: str, level_num: int, colorFmt: str = None, specialChar=""
    ):
        """
        Add a custom logging level.
        :param level_name: Name of the logging level.
        :param level_num: Numeric value of the logging level.
        :param method_name: Optional method name for logger.
        """

        CustomLevels.add(level_name, level_num, colorFmt, specialChar)

    # -----------------------------------------------------------------
    @classmethod
    def get_logger(cls, name="MikesToolsLibrary", level=logging.DEBUG):
        if cls._logger is None:
            logger = logging.getLogger(name)
            logger.setLevel(level)

            if not logger.handlers:  # prevent duplicate handlers
                ch = logging.StreamHandler()
                ch.setLevel(level)
                formatter = logging.Formatter(
                    "%(asctime)s|%(filename)s|%(lineno)4d|%(funcName)s|%(levelname)8s| %(message)s"
                )
                ch.setFormatter(formatter)
                logger.addHandler(ch)

            cls._logger = logger
        return cls._logger

    # -----------------------------------------------------------------
    def add_custom_level(self, level_name, level_num, method_name=None):
        """Add a custom level via the CustomLevels helper class."""
        return CustomLevels.add(level_name, level_num, method_name)

    # -----------------------------------------------------------------
    @classmethod
    def show_all_levels(cls, logger):
        """Show all defined logging levels."""
        CustomLevels.show_all_levels(logger)

    # -----------------------------------------------------------------
    @classmethod
    def showColorSampler(cls) -> None:
        """show all the possible color combinations"""
        CustomLevels.show_possible_colors()

    # -----------------------------------------------------------------
    @classmethod
    # def addLevelExclude(self, level_to_exclude: int, mode: LoggingMode = LoggingMode.ALL) -> None:
    def turnOffLevel(
        cls, level_to_exclude: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOffLevel(level_to_exclude, mode)

    # -----------------------------------------------------------------
    @classmethod
    # def removeLevelExclude(self, level_to_remove: int, mode: LoggingMode = LoggingMode.ALL) -> None:
    def turnOnLevel(
        cls, level_to_remove: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOnLevel(level_to_remove, mode)

    # -----------------------------------------------------------------
    @classmethod
    def showExcludeLevelFilter(cls, mode: LoggingMode = LoggingMode.ALL) -> set:
        # print (f"++++{ExcludeLevelFilter.Filters=}")
        # return ExcludeLevelFilter.Filters
        return ExcludeLevelFilter.showFiltersByMode(mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffRange(
        cls, start: int, end: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOffLevelRange(start, end, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange(
        cls, start: int, end: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOnLevelRange(start, end, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffNonStandardLevels(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(11, 19, mode)
        ExcludeLevelFilter.turnOffLevelRange(21, 29, mode)
        ExcludeLevelFilter.turnOffLevelRange(31, 39, mode)
        ExcludeLevelFilter.turnOffLevelRange(41, 49, mode)
        ExcludeLevelFilter.turnOffLevelRange(51, 59, mode)
        ExcludeLevelFilter.turnOffLevelRange(60, 1000, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnNonStandardLevels(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(11, 19, mode)
        ExcludeLevelFilter.turnOnLevelRange(21, 29, mode)
        ExcludeLevelFilter.turnOnLevelRange(31, 39, mode)
        ExcludeLevelFilter.turnOnLevelRange(41, 49, mode)
        ExcludeLevelFilter.turnOnLevelRange(51, 59, mode)
        ExcludeLevelFilter.turnOnLevelRange(60, 1000, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn200s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff200s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn300s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(300, 399, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff300s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(300, 399, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn400s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff400s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn500s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff500s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn600s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff600s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnDATA(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(700, 799, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffDATA(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(700, 799, mode)

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------


# -----------------------------------------------------------------
if __name__ == "__main__":
    """
    This is the main function that runs when the script is executed directly.
    It sets up the logger and demonstrates the usage of the CustomFormatter class.
    """
    print("You should not run this file directly, it is a module to be imported.")
    sys.exit(-99)
