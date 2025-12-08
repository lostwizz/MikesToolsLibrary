#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggerSetup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 22:16:09"
###############################################################################
import logging
import sys

from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter


# from .CustomFormatter import CustomFormatter
# from .CustomLevels import CustomLevels

from .ExcludeLevelFilter import ExcludeLevelFilter


class LoggerSetup:
    """
    Unified logger setup:
    - Console handler with CustomFormatter (color, pretty-print)
    - File handler with plain text logs
    - Support for custom levels via add_custom_level
    - Optional filters (exclude certain levels)
    """

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
            # Console handler
            # console_handler = logging.StreamHandler(sys.stdout)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            # console_handler.setFormatter(CustomFormatter("%(name)s | %(levelname)s | %(message)s"))
            # console_formatter = logging.Formatter(
            #     CustomFormatter.DEFAULT_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"
            # )

            console_formatter = CustomFormatter(CustomFormatter.DEFAULT_FORMAT, datefmt="%H:%M:%S")
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            ######
            # File handler
            file_handler = logging.FileHandler(logfile, encoding="utf-8")
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                CustomFormatter.DEFAULT_FILE_FORMAT,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

        
        setupLogger


    # -----------------------------------------------------------------
    def get_logger(self) -> logging.Logger:
        return self.logger

    # -----------------------------------------------------------------
    def add_custom_level(level_name, level_num, method_name=None):
        return CustomLevels.add_log_level(level_name, level_num, method_name)


    # -----------------------------------------------------------------
    def add_filter(self, level_to_exclude: int):
        """
        Add a filter to exclude a specific level from console/file output.
        """
        for handler in self.logger.handlers:
            handler.addFilter(ExcludeLevelFilter(level_to_exclude))
