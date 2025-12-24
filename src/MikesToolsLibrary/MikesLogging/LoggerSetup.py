#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
"""
LoggerSetup.py

Unified logger setup for MikesToolsLibrary with:
- Console, file, rotating, timed-rotating handlers
- Custom levels and formatting
- Exclude filters per logging mode
- Transparent module-level logger with optional overrides

Usage in other modules:

Default logger:
    from LoggerSetup import logger
    logger.debug("Debug message")

Custom logger:
    from LoggerSetup import get_logger, LoggingMode
    my_logger = get_logger(
        logfile="D:/Logs/custom.log",
        modes=LoggingMode.CONSOLE | LoggingMode.FILE
    )

    # TODO:
# COMMENT:
# NOTE:
# USEFULL:
# LEARN:
# RECHECK
# INCOMPLETE
# SEE NOTES
# POST
# HACK
# FIXME
# BUG
# [ ] something to do
# [x]  i did sometrhing

"""
__version__ = "0.1.2.00326-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-22 23:00:00"
###############################################################################

import sys
import getpass
import socket
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler
# from logging.handlers import SocketHandler
# from logging.handlers import DatagramHandler
# from logging.handlers import NTEventLogHandler
# from logging.handlers import MemoryHandler, BufferingHandler
# from logging.handlers import HTTPHandler
# from logging.handlers import QueueHandler   #, SimpleQueue
# from logging.handlers import QueueListener

from pathlib import Path

# Custom modules
from .CustomLevels import CustomLevels
from .CustomFormatter import CustomFormatter
from .ExcludeLevelFilter import ExcludeLevelFilter
from .LoggingMode import LoggingMode

###############################################################################
class LoggerSetup:
    """Unified logger setup class."""

    _logger = None  # singleton logger

    def __init__(
        self,
        name: str = "MikesToolsLibrary",
        level: int = logging.DEBUG,
        logfile: str = "./logs/MikesToolsLibrary.log",
        modes: LoggingMode = LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR,
        maxBytes: int = 100_000_000,
        backupCount: int = 25,
        interval: int = 1,
        when: str = "midnight",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handlers_by_mode = {}

        if not self.logger.handlers:
            handlers = {
                LoggingMode.CONSOLE: lambda: self._setup_console(level),
                LoggingMode.FILE: lambda: self._setup_file(level, logfile),
                LoggingMode.SMTP: lambda: self._setup_smtp(name),
                LoggingMode.ROTATINGFN: lambda: self._setup_rotating(level, logfile, maxBytes, backupCount),
                LoggingMode.TIMEDROTATOR: lambda: self._setup_timed_rotating(level, logfile, when, interval, backupCount),
            }
                # LoggingMode.MEMORY: lambda: None,
                # LoggingMode.SYSLOG: lambda: None,
                # LoggingMode.HTTP: lambda: None,
                # LoggingMode.QUEUE: lambda: None,
                # LoggingMode.DATABASE: lambda: None,
                # LoggingMode.CLOUD: lambda: None,
                # LoggingMode.EXTERNAL: lambda: None,
            for mode_flag, setup_fn in handlers.items():
                if modes & mode_flag:
                    handler = setup_fn()
                    self.logger.addHandler(handler)
                    self.handlers_by_mode[mode_flag] = handler

        # Add custom levels
        self.add_special_levels(self.logger)

        # Set singleton if not set
        if LoggerSetup._logger is None:
            LoggerSetup._logger = self.logger

    # -------------------- Handlers -------------------- #
    def _setup_console(self, level):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%H:%M:%S",
                fmtMode=LoggingMode.CONSOLE,
            )
        )
        ch.addFilter(ExcludeLevelFilter(LoggingMode.CONSOLE))
        return ch

    def _setup_file(self, level, logfile):
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )
        fh.addFilter(ExcludeLevelFilter(LoggingMode.FILE))
        return fh

    def _setup_rotating(self, level, logfile, maxBytes, backupCount):
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)15s|%(filename)16s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )
        fh.addFilter(ExcludeLevelFilter(LoggingMode.ROTATINGFN))
        return fh

    def _setup_timed_rotating(self, level, logfile, when, interval, backupCount):
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        fh = TimedRotatingFileHandler(logfile, when=when, interval=interval, backupCount=backupCount, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(
            CustomFormatter(
                fmt="%(asctime)s|%(ip)s|%(user_id)s|%(filename)s|%(lineno)4s|%(funcName)s|%(levelname)8s| %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                fmtMode=LoggingMode.FILE,
            )
        )
        fh.addFilter(ExcludeLevelFilter(LoggingMode.ROTATINGFN))
        return fh

    def _setup_smtp(self, name):
        mail_handler = SMTPHandler(
            mailhost=("mail.merrett.ca", 587),
            fromaddr="public@merrett.ca",
            toaddrs=["public@merrett.ca"],
            subject=f"Application Error - {name}",
            credentials=("public@merrett.ca", "2]soaDOv;E;9"),
            secure=(),
        )
        mail_handler.addFilter(ExcludeLevelFilter(LoggingMode.SMTP))
        mail_handler.setLevel(999)
        return mail_handler

    # -------------------- Utilities -------------------- #
    @classmethod
    def add_special_levels(cls, logger):
        CustomLevels.addMyCustomLevels(logger)

    @classmethod
    def get_logger(cls, name="MikesToolsLibrary", level=logging.DEBUG):
        if cls._logger is None:
            LoggerSetup(name=name, level=level)
        return cls._logger

    @classmethod
    def includeUserNameAndIP(cls, overrideName=None, overrideIP=None):
        if cls._logger is None:
            cls._logger = LoggerSetup().logger  # lazy init
        username = overrideName if overrideName else getpass.getuser()
        local_ip = overrideIP if overrideIP else socket.gethostbyname(socket.gethostname())
        cls._logger.info(
            f"☠Setting Username: '{username}' and IP: '{local_ip}'",
            extra={"user_id": username, "ip": local_ip, "special": True}
        )

    # -------------------- Force Rollover -------------------- #
    @classmethod
    def force_rollover(cls, mode: LoggingMode = LoggingMode.ALL):
        if cls._logger is None:
            cls._logger = LoggerSetup().logger
        for flag, handler in getattr(cls._logger, "handlers", {}).items():
            if mode & flag and hasattr(handler, "doRollover"):
                handler.doRollover()

    # -------------------- Non-standard levels -------------------- #
    @classmethod
    def show_all_levels(cls, logger):
        """Show all defined logging levels."""
        CustomLevels.show_all_levels(logger)

 # -----------------------------------------------------------------
    @classmethod
    def showColorSampler(cls) -> None:
        """show all the possible color combinations"""
        CustomLevels.show_possible_colors()

    # -----------------------------------------------------------------
    @classmethod
    # def addLevelExclude(self, level_to_exclude: int, mode: LoggingMode = LoggingMode.ALL) -> None:
    def turnOffLevel(
        cls, level_to_exclude: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOffLevel(level_to_exclude, mode)

    # -----------------------------------------------------------------
    @classmethod
    # def removeLevelExclude(self, level_to_remove: int, mode: LoggingMode = LoggingMode.ALL) -> None:
    def turnOnLevel(
        cls, level_to_remove: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOnLevel(level_to_remove, mode)

    # -----------------------------------------------------------------
    @classmethod
    def showExcludeLevelFilter(cls, mode: LoggingMode = LoggingMode.ALL) -> set:
        # print (f"++++{ExcludeLevelFilter.Filters=}")
        # return ExcludeLevelFilter.Filters
        return ExcludeLevelFilter.showFiltersByMode(mode)

   # -----------------------------------------------------------------
    @classmethod
    def turnOffRange(
        cls, start: int, end: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOffLevelRange(start, end, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnLevelRange(
        cls, start: int, end: int, mode: LoggingMode = LoggingMode.ALL
    ) -> None:
        ExcludeLevelFilter.turnOnLevelRange(start, end, mode)

    # -------------------- Specific ranges -------------------- #
    @classmethod
    def turnOffNonStandardLevels(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(11, 19, mode)
        ExcludeLevelFilter.turnOffLevelRange(21, 29, mode)
        ExcludeLevelFilter.turnOffLevelRange(31, 39, mode)
        ExcludeLevelFilter.turnOffLevelRange(41, 49, mode)
        ExcludeLevelFilter.turnOffLevelRange(51, 59, mode)
        ExcludeLevelFilter.turnOffLevelRange(60, 1000, mode)


   # -----------------------------------------------------------------
    @classmethod
    def turnOnNonStandardLevels(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(11, 19, mode)
        ExcludeLevelFilter.turnOnLevelRange(21, 29, mode)
        ExcludeLevelFilter.turnOnLevelRange(31, 39, mode)
        ExcludeLevelFilter.turnOnLevelRange(41, 49, mode)
        ExcludeLevelFilter.turnOnLevelRange(51, 59, mode)
        ExcludeLevelFilter.turnOnLevelRange(60, 1000, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn200s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff200s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(200, 299, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn300s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(300, 399, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff300s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(300, 399, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn400s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff400s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(400, 499, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn500s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff500s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(500, 599, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOn600s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOff600s(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(600, 699, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOnDATA(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOnLevelRange(700, 799, mode)

    # -----------------------------------------------------------------
    @classmethod
    def turnOffDATA(cls, mode: LoggingMode = LoggingMode.ALL) -> None:
        ExcludeLevelFilter.turnOffLevelRange(700, 799, mode)

    # -----------------------------------------------------------------

###############################################################################
# Module-level default logger
logger = LoggerSetup().logger

###############################################################################
# Flexible helper
def get_logger(name="MikesToolsLibrary", level=logging.DEBUG, logfile=None, modes=None) -> logging.Logger:
    logfile = logfile or "./logs/MikesToolsLibrary.log"
    modes = modes or (LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR)
    if LoggerSetup._logger and logfile == "./logs/MikesToolsLibrary.log" and modes == (LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR):
        return LoggerSetup._logger
    return LoggerSetup(name=name, level=level, logfile=logfile, modes=modes).logger
