#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py


to use this -- add it to the path
set PYTHONPATH=D:\_Python_Projects\MikesToolsLibrary\src;%PYTHONPATH%


"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-08 00:32:30"
###############################################################################

import sys
import json
import logging
from logging.handlers import SMTPHandler

from MikesToolsLibrary.MikesLogging.log_decorator import log_decorator
from MikesToolsLibrary.MikesLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MikesLogging.CustomFormatter import CustomFormatter, FormatMode
from MikesToolsLibrary.MikesLogging.ExcludeLevelFilter import ExcludeLevelFilter


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
        modes: FormatMode = FormatMode.CONSOLE | FormatMode.FILE,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid duplicate handlers if re-instantiated
        if not self.logger.handlers:

            handlers = {
                FormatMode.CONSOLE: lambda: self.setupConsoleHandler(level),
                FormatMode.FILE: lambda: self.setupFileHandler(level, logfile),
                FormatMode.SMTP: lambda: self.setupSMTPHandler(name),
                FormatMode.JSON: lambda: self.setupJSONHandler(level, logfile),
                # FormatMode.MEMORY: lambda: None,
                # FormatMode.SYSLOG: lambda: None,
                # FormatMode.HTTP: lambda: None,
                # FormatMode.QUEUE: lambda: None,
                # FormatMode.DATABASE: lambda: None,
                # FormatMode.CLOUD: lambda: None,
                # FormatMode.EXTERNAL: lambda: None,
            }

            for mode, setup in handlers.items():
                if modes & mode:
                    self.logger.addHandler(setup())

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
                fmtMode=FormatMode.CONSOLE,
            )
        )
        ch.addFilter(ExcludeLevelFilter(FormatMode.CONSOLE))
        return ch

    # -----------------------------------------------------------------
    def setupFileHandler(self, level, logfile):
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=FormatMode.FILE,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(FormatMode.FILE))
        return fh

    # -----------------------------------------------------------------
    def setupJSONHandler(self, level, logfile):
        fh = logging.FileHandler("JSON" + logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=FormatMode.JSON,
            )
        )  # more detail, timestamps
        fh.addFilter(ExcludeLevelFilter(FormatMode.JSON))
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

        mail_handler.addFilter(ExcludeLevelFilter(FormatMode.SMTP))
        mail_handler.setLevel(999)

        return mail_handler

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
    def add_special_levels(self, logger):
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
    def show_all_levels(self, logger):
        """Show all defined logging levels."""
        CustomLevels.show_all_levels(logger)

    # -----------------------------------------------------------------
    @classmethod
    def showColorSampler(self) -> None:
        """show all the possible color combinations"""
        CustomLevels.show_possible_colors()

    # -----------------------------------------------------------------
    @classmethod
    # def addLevelExclude(self, level_to_exclude: int, mode: FormatMode = FormatMode.ALL) -> None:
    def turnOffLevel(self, level_to_exclude: int, mode: FormatMode = FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevel(level_to_exclude, mode)

    # -----------------------------------------------------------------
    @classmethod
    #def removeLevelExclude(self, level_to_remove: int, mode: FormatMode = FormatMode.ALL) -> None:
    def turnOnLevel(self, level_to_remove: int, mode: FormatMode = FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevel(level_to_remove, mode)

    # -----------------------------------------------------------------
    @classmethod
    def showExcludeLevelFilter(self, mode: FormatMode = FormatMode.ALL) -> set:
        # print (f"++++{ExcludeLevelFilter.Filters=}")
        # return ExcludeLevelFilter.Filters
        return ExcludeLevelFilter.showFiltersByMode(mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffRange( self, start:int, end:int, mode:FormatMode = FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( start, end, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange( self, start:int, end:int, mode: FormatMode = FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(start, end, mode )

    # -----------------------------------------------------------------
    @classmethod
    def turnOffNonStandardLevels(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 11, 19, mode)
        ExcludeLevelFilter.turnOffLevelRange( 21, 29, mode)
        ExcludeLevelFilter.turnOffLevelRange( 31, 39, mode)
        ExcludeLevelFilter.turnOffLevelRange( 41, 49, mode)
        ExcludeLevelFilter.turnOffLevelRange( 51, 59, mode)
        ExcludeLevelFilter.turnOffLevelRange( 60, 1000, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnNonStandardLevels(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 11, 19, mode)
        ExcludeLevelFilter.turnOnLevelRange( 21, 29, mode)
        ExcludeLevelFilter.turnOnLevelRange( 31, 39, mode)
        ExcludeLevelFilter.turnOnLevelRange( 41, 49, mode)
        ExcludeLevelFilter.turnOnLevelRange( 51, 59, mode)
        ExcludeLevelFilter.turnOnLevelRange( 60, 1000, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn200s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff200s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn300s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 300, 399, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff300s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 300, 399, mode)
    # -----------------------------------------------------------------
    @classmethod
    def turnOn400s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff400s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn500s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff500s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn600s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff600s(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnDATA(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange( 700, 799, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffDATA(self, mode: FormatMode= FormatMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange( 700, 799, mode)


    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    # @classmethod
    # def turnOffTrace(mode: FormatMode = None) -> set:

