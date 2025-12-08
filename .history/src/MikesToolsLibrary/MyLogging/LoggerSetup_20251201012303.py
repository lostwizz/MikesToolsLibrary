#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py


"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-01 01:23:03"
###############################################################################

import sys
import logging
from logging.handlers import SMTPHandler

from MikesToolsLibrary.MyLogging.log_decorator import log_decorator
from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter, FormatMode
from MikesToolsLibrary.MyLogging.ExcludeLevelFilter import ExcludeLevelFilter


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
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Avoid duplicate handlers if re-instantiated
        if not self.logger.handlers:
            ######
            # Console handler
            ch = self.setupConsoleHandler(level)
            self.logger.addHandler(ch)

            ######
            # File handler
            fh = self.setupFileHandler(level, logfile)
            self.logger.addHandler(fh)

            ######
            # SMTP handler
            mh = self.setupSMTPHandler(name)
            self.logger.addHandler(mh)

            ######
            # json handler
            jh = self.setupJSONHandler(logfile)
            self.logger.addHandler(jh)
            
                    # logging.setLoggerClass(AppendArgsLogger)

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

        mail_handler.setLevel(999)

        return mail_handler

    # -----------------------------------------------------------------
    def setupJSONHandler(self, level, logfile):
        fh = logging.FileHandler("JSON" + logfile, encoding="utf-8")
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
    def addLevelExclude(self, level_to_exclude: int, mode: FormatMode = None) -> None:
        ExcludeLevelFilter.addFilterLevel(level_to_exclude, mode)

    # -----------------------------------------------------------------
    @classmethod
    def removeLevelExclude(self, level_to_remove: int, mode: FormatMode = None) -> None:
        ExcludeLevelFilter.removeFilterLevel(level_to_remove, mode)

    # -----------------------------------------------------------------
    @classmethod
    def showExcludeLevelFilter(self, mode: FormatMode = None) -> set:
        # print (f"++++{ExcludeLevelFilter.Filters=}")
        # return ExcludeLevelFilter.Filters
        return ExcludeLevelFilter.showFiltersByMode()

    # -----------------------------------------------------------------
