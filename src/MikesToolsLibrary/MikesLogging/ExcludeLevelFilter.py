#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
ExcludeLevelFilter.py


"""
__version__ = "0.0.0.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 22:26:04"
###############################################################################
import sys
import logging
from collections import defaultdict

from .LoggingMode import LoggingMode, iter_flags


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
    _instance = None # class-level singleton reference
    #Filters = set()
    Filters = defaultdict(set)

    # -----------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # -----------------------------------------------------------------
    def __init__(self, mode: LoggingMode = None, name: str = ""):
        super().__init__(name)

        if mode == LoggingMode.ALL:
            raise ValueError("ExcludeLevelFilter cannot be instantiated with LoggingMode.ALL")
        self.mode = mode

    # -----------------------------------------------------------------
    def filter(self, record: logging.LogRecord) -> bool:
        """Return False if excluded for any intersecting flag or globally."""
        # Global exclusions
        if record.levelno in ExcludeLevelFilter.Filters[None]:
            return False
        # No specific mode: only global applies
        if not self.mode:
            return True
        # Check any constituent flag of this filter’s mode
        for flag in iter_flags(self.mode):
            if record.levelno in ExcludeLevelFilter.Filters[flag]:
                return False
        return True

    # -----------------------------------------------------------------
    @classmethod
    def showFiltersByMode(cls, fMode: LoggingMode =LoggingMode.ALL ):

        """
        Display exclusions with human-friendly keys.
        - Never stores under 'ALL'; compute ALL as union of all flags for display.
        - If fMode is a combination, aggregate those flags.
        """
        def key_name(k):
            return k.name if isinstance(k, LoggingMode) else str(k)

        # Build per-flag dict (exclude empty for clarity if desired)
        per_flag = {
            key_name(flag): sorted(list(levels))
            for flag, levels in cls.Filters.items()
            if flag is not None
        }
        global_levels = sorted(list(cls.Filters.get(None, set())))

        if fMode == LoggingMode.ALL:
            sets_to_union = [cls.Filters[f] for f in cls.Filters if f is not None]
            union = sorted(list(set().union(*sets_to_union))) if sets_to_union else []
            result = dict(per_flag)

            if global_levels:
                result["GLOBAL"] = global_levels

            result["ALL"] = union
            return result

        else:
            # Aggregate only requested flags
            requested = [f for f in LoggingMode if f != 0 and (fMode & f) == f]
            agg = sorted(list(set().union(*(cls.Filters.get(f, set()) for f in requested)))) if requested else []
            return {
                " | ".join(f.name for f in requested) if requested else fMode.name: agg
            }





    # -----------------------------------------------------------------
    @classmethod
    # def addFilterLevel(self, level: int, mode: LoggingMode = None) -> None:
    def turnOffLevel(cls, level: int, mode: LoggingMode = LoggingMode.ALL) -> None:
        if mode is None:
            cls.Filters[None].add(level)
            return
        for flag in iter_flags(mode):
            cls.Filters[flag].add(level)

    # -----------------------------------------------------------------
    @classmethod
    # def removeFilterLevel(self, level: int, mode: LoggingMode = None) -> None:
    def turnOnLevel(cls, level: int, mode: LoggingMode = LoggingMode.ALL) -> None:
        if mode is None:
            cls.Filters[None].discard(level)
            return
        for flag in iter_flags(mode):
            cls.Filters[flag].discard(level)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffLevelRange(self, start:int, end:int, mode: LoggingMode = LoggingMode.ALL) -> None:
        for i in range(start, end):
            self.turnOffLevel( i, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange( self, start:int, end:int, mode: LoggingMode = LoggingMode.ALL) -> None:
        for i in range(start, end):
            self.turnOnLevel(i, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnEverything(self, mode:LoggingMode = LoggingMode.ALL) -> None:
        for i in range( 1, 1000):
            self.turnOnLevel(i, mode)
            
    # -----------------------------------------------------------------
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
