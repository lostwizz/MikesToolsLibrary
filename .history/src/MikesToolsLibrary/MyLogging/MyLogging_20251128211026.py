#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MyLogging.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 21:10:26"
###############################################################################

import logging
import sys
from .CustomFormatter import CustomFormatter
from .CustomLevels import CustomLevels
from .ExcludeLevelFilter import ExcludeLevelFilter

class LoggerSetup:


    # -----------------------------------------------------------------
    def __init__(self, name: str = "MikesToolsLibrary", level: int = logging.DEBUG, logfile: str = "app.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(CustomFormatter("%(name)s | %(levelname)s | %(message)s"))
            self.logger.addHandler(console_handler)

            # File handler
            file_handler = logging.FileHandler(logfile, encoding="utf-8")
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    # -----------------------------------------------------------------
    def get_logger(self) -> logging.Logger:
        return self.logger