#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
ExcludeLevelFilter.py


"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-30 21:33:57"
###############################################################################

import logging
# from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


# from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
# from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

from MikesToolsLibrary.MyLogging.CustomFormatter import FormatMode



# =================================================================
class ExcludeLevelFilter(logging.Filter):
    """
    A logging filter to exclude specific logging levels.
    This filter can be used to prevent certain log levels from being processed by the logger.

    Example usage:
        logger = logging.getLogger(__name__)
        exclude_filter = ExcludeLevelFilter()
        logger.addFilter(exclude_filter)

        # To exclude a specific level, use:
        exclude_filter.addFilterLevel(logging.DEBUG)

        # To remove the exclusion, use:
        exclude_filter.removeFilterLevel(logging.DEBUG)

        # To exclude multiple levels, you can use:
        exclude_filter.addFilterLevel(logging.DEBUG)
        exclude_filter.addFilterLevel(logging.INFO)
        exclude_filter.addFilterLevel(logging.WARNING)
        exclude_filter.addFilterLevel(logging.ERROR)
        exclude_filter.addFilterLevel(logging.CRITICAL)


    """
    Filters = set()

    # -----------------------------------------------------------------
    def __init__(self, mode: FormatMode = None, name: str = ""):

        super().__init__(name)

        # Disallow ALL here
        if mode == FormatMode.ALL:
            raise ValueError("ExcludeLevelFilter cannot be instantiated with FormatMode.ALL")
        self.mode = mode

    # -----------------------------------------------------------------
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filters out log records based on the excluded levels.
        :param record: The log record to check.
        :return: True if the record should be logged, False otherwise.
        """
        if (None, record.levelno) in ExcludeLevelFilter.Filters:
                return False
                if self.mode and (self.mode, record.levelno) in ExcludeLevelFilter.Filters:
                    return False
                if (FormatMode.ALL, record.levelno) in ExcludeLevelFilter.Filters:
                    return False
                return True



    # -----------------------------------------------------------------
    @classmethod
    def showFiltersByMode(cls):
        """Return a dict of excluded levels grouped by FormatMode."""
        grouped = {}
        for mode, level in cls.Filters:
            grouped.setdefault(mode, []).append(level)
        return grouped
    
    # -----------------------------------------------------------------
    @classmethod
    def addFilterLevel(self, level: int, mode: FormatMode = None) -> None:
        """
        Adds a logging level to the exclusion list.
        :param level: The logging level to exclude.
        """
        self.Filters.add((mode,level))

    # -----------------------------------------------------------------
    @classmethod
    def removeFilterLevel(self, level: int, mode: FormatMode = None) -> None:
        """
        Removes a logging level from the exclusion list.
        :param level: The logging level to include again.
        """
        self.Filters.discard((mode,level))

    # -----------------------------------------------------------------
    @classmethod
    def turnOffLevelRange(self, start:int, end:int, mode: FormatMode = None) -> None:
        for i in range(start, end):
            self.addFilterLevel( i, mode)
            
    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange( self, start:int, end:int, mode: FormatMode = None) -> None:
        for i in range(start, end):
            self.removeFilterLevel(i, mode)
            
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
