#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-30 19:40:34"
###############################################################################

import sys
import logging

from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels

# from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter, FormatMode
from MikesToolsLibrary.MyLogging.ExcludeLevelFilter import ExcludeLevelFilter




# from .CustomFormatter import CustomFormatter
# from .CustomLevels import CustomLevels

from .ExcludeLevelFilter import ExcludeLevelFilter


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

            exclude_filter = ExcludeLevelFilter()
            
            ######
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(
                CustomFormatter(
                    fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                    datefmt="%H:%M:%S",
                    fmtMode=FormatMode.CONSOLE,
                )
            )  # short, colored
            ch.addFilter(exclude_filter)
            self.logger.addHandler(ch)

            ######
            # File handler
            fh = logging.FileHandler(logfile, encoding="utf-8")
            fh.setLevel(level)
            fh.setFormatter(
                CustomFormatter(
                    fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    fmtMode=FormatMode.FILE,
                )
            )  # more detail, timestamps
            fh.addFilter(exclude_filter)
            self.logger.addHandler(fh)

    # -----------------------------------------------------------------
    @classmethod
    def add_special_levels(self, logger):
        """Add the predefined custom log levels by delegating to CustomLevels."""
        CustomLevels.addMyCustomLevels(logger)

    # -----------------------------------------------------------------
    @classmethod
    def add_level(cls, level_name: str, level_num: int, colorFmt: str = None, specialChar=""):
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
    def add_filter(self, level_to_exclude: int):
        """
        Add a filter to exclude a specific level from console/file output.
        """
        for handler in self.logger.handlers:
            handler.addFilter(ExcludeLevelFilter(level_to_exclude))

    # -----------------------------------------------------------------
    @classmethod
    def show_all_levels(self, logger):
        """Show all defined logging levels."""
        CustomLevels.show_all_levels(logger)
        
    # -----------------------------------------------------------------
    @classmethod
    def showColorSampler(self, logger) -> None:        
        """show all the possible color combinations"""
        CustomLevels.show_possible_colors()
        
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
