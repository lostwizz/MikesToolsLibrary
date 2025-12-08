#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
ExcludeLevelFilter.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-26 23:28:51"
###############################################################################


# =================================================================
# =================================================================
import logging
import sys


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

    def __init__(self, name=""):
        """
        Initializes the filter with an empty set of levels to exclude.
        :param name: Optional name for the filter.
        """
        super().__init__(name)
        #######self.Filters = set()

    def filter(self, record):
        """
        Filters out log records based on the excluded levels.
        :param record: The log record to check.
        :return: True if the record should be logged, False otherwise.
        """
        return record.levelno not in self.Filters

    def addFilterLevel(self, level):
        """
        Adds a logging level to the exclusion list.
        :param level: The logging level to exclude.
        """
        self.Filters.add(level)

    def removeFilterLevel(self, level):
        """
        Removes a logging level from the exclusion list.
        :param level: The logging level to include again.
        """
        self.Filters.discard(level)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffNonStandardLevels(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, 11, 19)
        ExcludeLevelFilter.turnOffLevelRange(logger, 21, 29)
        ExcludeLevelFilter.turnOffLevelRange(logger, 31, 39)
        ExcludeLevelFilter.turnOffLevelRange(logger, 41, 49)
        ExcludeLevelFilter.turnOffLevelRange(logger, 51, 59)
        ExcludeLevelFilter.turnOffLevelRange(logger, 60, 1000)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffTrace(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.ExcludeLevelFilter.turnOffLevelRange(logger, -100, -199)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnTrace(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOnLevelRange(logger, -100, -199)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffMarkers(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOffLevelRange(logger, -300, -399)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnMarkers(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOnLevelRange(logger, -300, -399)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffTodo(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOffLevelRange(logger, -400, -499)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnTodo(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOnLevelRange(logger, -400, -499)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnAllNonStandardLevels(logger) -> None:
        for handler in logger.handlers:
            ExcludeLevelFilter.turnOnLevelRange(logger, -1, -1000)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffLevelRange(logger, start: int, end: int) -> None:
        for handler in logger.handlers:
            for i in range(start, end):
                for f in handler.filters:  # Access filters directly
                    if isinstance(f, ExcludeLevelFilter):
                        f.addFilterLevel(i)  # Dynamically add levels to exclude

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnLevelRange(logger, start: int, end: int) -> None:
        for handler in logger.handlers:
            for i in range(start, end):
                for f in handler.filters:  # Access filters directly
                    if isinstance(f, ExcludeLevelFilter):
                        f.removeFilterLevel(i)  # Dynamically add levels to include

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffLevel(logger, level: int) -> None:
        for handler in logger.handlers:
            for f in handler.filters:  # Access filters directly
                if isinstance(f, ExcludeLevelFilter):
                    f.addFilterLevel(level)  # Dynamically add levels to exclude

    # -----------------------------------------------------------------
    @staticmethod
    def turnOnLevel(logger, level: int) -> None:
        for handler in logger.handlers:
            for f in handler.filters:  # Access filters directly
                if isinstance(f, ExcludeLevelFilter):
                    f.removeFilterLevel(level)  # Dynamically add levels to include

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff200level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -200, -299)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn200level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -200, -299)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn300level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -300, -399)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff300level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -300, -399)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn400level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -400, -499)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff400level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -400, -499)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn500level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -500, -599)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff500level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -500, -599)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn600level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -600, -699)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff600level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -600, -699)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOn700level(logger) -> None:
        ExcludeLevelFilter.turnOnLevelRange(logger, -700, -799)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOff700level(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -700, -799)

    # -----------------------------------------------------------------
    @staticmethod
    def turnOffDataLevels(logger) -> None:
        ExcludeLevelFilter.turnOffLevelRange(logger, -700, -799)


# -----------------------------------------------------------------
if __name__ == "__main__":
    """
    This is the main function that runs when the script is executed directly.
    It sets up the logger and demonstrates the usage of the CustomFormatter class.
    """
    print("You should not run this file directly, it is a module to be imported.")
    sys.exit(-99)
