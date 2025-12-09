#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
ExcludeLevelFilter.py


"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-08 21:04:25"
###############################################################################

import logging
from collections import defaultdict


# from MikesToolsLibrary.MyLogging.log_decorator import log_decorator


# from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
# from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

from MikesToolsLibrary.MikesLogging.CustomFormatter import FormatMode

# -----------------------------------------------------------------
def iter_flags(mask: FormatMode) -> list[FormatMode]:
    """Yield individual flags contained in a mask (excluding 0)."""
    return [m for m in FormatMode if m != 0 and (mask & m) == m]


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
    def __init__(self, mode: FormatMode = None, name: str = ""):
        super().__init__(name)

        if mode == FormatMode.ALL:
            raise ValueError("ExcludeLevelFilter cannot be instantiated with FormatMode.ALL")
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
    def showFiltersByMode(cls, fMode: FormatMode =FormatMode.ALL ):

        """
        Display exclusions with human-friendly keys.
        - Never stores under 'ALL'; compute ALL as union of all flags for display.
        - If fMode is a combination, aggregate those flags.
        """
        def key_name(k):
            return k.name if isinstance(k, FormatMode) else str(k)

        # Build per-flag dict (exclude empty for clarity if desired)
        per_flag = {
            key_name(flag): sorted(list(levels))
            for flag, levels in cls.Filters.items()
            if flag is not None
        }
        global_levels = sorted(list(cls.Filters.get(None, set())))

        if fMode == FormatMode.ALL:
            sets_to_union = [cls.Filters[f] for f in cls.Filters if f is not None]
            union = sorted(list(set().union(*sets_to_union))) if sets_to_union else []
            result = dict(per_flag)

            if global_levels:
                result["GLOBAL"] = global_levels

            result["ALL"] = union
            return result

        else:
            # Aggregate only requested flags
            requested = [f for f in FormatMode if f != 0 and (fMode & f) == f]
            agg = sorted(list(set().union(*(cls.Filters.get(f, set()) for f in requested)))) if requested else []
            return {
                " | ".join(f.name for f in requested) if requested else fMode.name: agg
            }





    # -----------------------------------------------------------------
    @classmethod
    # def addFilterLevel(self, level: int, mode: FormatMode = None) -> None:
    def turnOffLevel(cls, level: int, mode: FormatMode = FormatMode.ALL) -> None:
        """
        Adds a logging level to the exclusion list.
        :param level: The logging level to exclude.
        """
        # self.Filters.add((mode,level))
        # self.Filters[mode].add(level)
        if mode is None:
            cls.Filters[None].add(level)
            return
        for flag in iter_flags(mode):
            cls.Filters[flag].add(level)



    # -----------------------------------------------------------------
    @classmethod
    # def removeFilterLevel(self, level: int, mode: FormatMode = None) -> None:
    def turnOnLevel(cls, level: int, mode: FormatMode = FormatMode.ALL) -> None:
        """
        Removes a logging level from the exclusion list.
        :param level: The logging level to include again.
        """
        # self.Filters.discard((mode,level))
        # self.Filters[mode].discard(level)
        if mode is None:
            cls.Filters[None].discard(level)
            return
        for flag in iter_flags(mode):
            cls.Filters[flag].discard(level)


    # -----------------------------------------------------------------
    @classmethod
    def turnOffLevelRange(self, start:int, end:int, mode: FormatMode = FormatMode.ALL) -> None:
        for i in range(start, end):
            self.turnOffLevel( i, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange( self, start:int, end:int, mode: FormatMode = FormatMode.ALL) -> None:
        for i in range(start, end):
            self.turnOnLevel(i, mode)

    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
