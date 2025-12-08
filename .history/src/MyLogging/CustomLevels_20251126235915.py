#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
CustomLevels.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-26 23:59:15"
###############################################################################

class CustomLevels:
    """Defines custom logging levels."""

    # Define custom logging levels
    VERBOSE = 15
    NOTICE = 25
    ALERT = 45

    @staticmethod
    def add_custom_levels_to_logging(logging_module):
        """Adds custom levels to the logging module."""
        logging_module.addLevelName(CustomLevels.VERBOSE, "VERBOSE")
        logging_module.addLevelName(CustomLevels.NOTICE, "NOTICE")
        logging_module.addLevelName(CustomLevels.ALERT, "ALERT")

        def verbose(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.VERBOSE):
                self._log(CustomLevels.VERBOSE, message, args, **kws)

        def notice(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.NOTICE):
                self._log(CustomLevels.NOTICE, message, args, **kws)

        def alert(self, message, *args, **kws):
            if self.isEnabledFor(CustomLevels.ALERT):
                self._log(CustomLevels.ALERT, message, args, **kws)

        logging_module.Logger.verbose = verbose
        logging_module.Logger.notice = notice
        logging_module.Logger.alert = alert


