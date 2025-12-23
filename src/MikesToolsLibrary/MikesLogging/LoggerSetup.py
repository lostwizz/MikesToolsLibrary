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
__version__ = "0.1.2.00231-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-22 21:10:41"
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

# Import your custom modules
from .CustomLevels import CustomLevels
from .CustomFormatter import CustomFormatter
from .ExcludeLevelFilter import ExcludeLevelFilter
from .LoggingMode import LoggingMode



# from .log_decorator import log_decorator
###############################################################################
class LoggerSetup:
    """
    Unified logger setup with optional modes:
    - Console
    - File
    - Timed rotation
    - Rotating file
    - SMTP
    """

    _logger = None

    # -----------------------------------------------------------------
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

        # Avoid duplicate handlers if re-instantiated
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

    # -------------------- Handlers -------------------- #
    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
    def force_rollover(self, mode: LoggingMode = LoggingMode.ALL):
        """Force rollover for handlers matching the given mode."""
        for flag, handler in self.handlers_by_mode.items():
            if mode & flag and hasattr(handler, "doRollover"):
                handler.doRollover()

    # -----------------------------------------------------------------
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
    # -----------------------------------------------------------------
    @classmethod
    def add_special_levels(cls, logger):
        CustomLevels.addMyCustomLevels(logger)

    # -----------------------------------------------------------------
    @classmethod
    def includeUserNameAndIP(cls, overrideName=None, overrideIP=None):
        if cls._logger is None:
            # Create default logger if not already created
            cls._logger = LoggerSetup().logger

        username = overrideName if overrideName else getpass.getuser()
        local_ip = overrideIP if overrideIP else socket.gethostbyname(socket.gethostname())
        cls._logger.info(
            f"☠Setting Username: '{username}' and IP: '{local_ip}'",
            extra={"user_id": username, "ip": local_ip, "special": True}
        )


    # -----------------------------------------------------------------
    @classmethod
    def reset_state(cls):
        ExcludeLevelFilter.Filters.clear()
        logging.Logger.manager.loggerDict.clear()
        for level_name in list(logging._nameToLevel.keys()):
            if level_name not in logging._levelToName.values():
                logging._nameToLevel.pop(level_name, None)

   # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
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
logger = LoggerSetup(
    name="MikesToolsLibrary",
    level=logging.DEBUG,
    logfile="./logs/MikesToolsLibrary.log",
    modes=LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR
).logger


###############################################################################
# Flexible helper to create custom loggers
def get_logger(
    name: str = "MikesToolsLibrary",
    level: int = logging.DEBUG,
    logfile: str = None,
    modes: LoggingMode = None,
) -> logging.Logger:
    """
    Returns a configured logger.
    - Override logfile, level, or modes if desired.
    - If module-level logger exists and defaults are used, returns it.
    """
    logfile = logfile or "./logs/MikesToolsLibrary.log"
    modes = modes or (LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR)

    if LoggerSetup._logger and logfile == "./logs/MikesToolsLibrary.log" and modes == (LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR):
        return LoggerSetup._logger

    return LoggerSetup(
        name=name,
        level=level,
        logfile=logfile,
        modes=modes
    ).get_logger()
