#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
ExcludeLevelFilter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-30 20:51:08"
###############################################################################

import logging
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


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
    def __init__(self, name: str = ""):
        """
        Initializes the filter with an empty set of levels to exclude.
        :param name: Optional name for the filter.
        """
        super().__init__(name)
        #######self.Filters = set()

    # -----------------------------------------------------------------
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filters out log records based on the excluded levels.
        :param record: The log record to check.
        :return: True if the record should be logged, False otherwise.
        """
        return record.levelno not in self.Filters

    # -----------------------------------------------------------------
    @classmethod
    def addFilterLevel(self, level: int) -> None:
        """
        Adds a logging level to the exclusion list.
        :param level: The logging level to exclude.
        """
        self.Filters.add(level)

    # -----------------------------------------------------------------
    @classmethod
    def removeFilterLevel(self, level: int) -> None:
        """
        Removes a logging level from the exclusion list.
        :param level: The logging level to include again.
        """
        self.Filters.discard(level)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffLevelRange(self, start:int, end:int) -> None:
        for i in range(start, end):
            self.addFilterLevel( i)
            
    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange( self, start:int, end:int) -> None:
        for i in range(start, end):
            self.removeFilterLevel(i)
            
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
