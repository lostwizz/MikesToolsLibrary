#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 01:04:52"
###############################################################################

import logging
import MikesToolsLibrary.MyLogging as mylog
from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

import os
import sys

# if sys.platform.startswith("win"):
#     os.system("")

#mylog.tests("sam is gone")
# mylog.LoggerSetup.test("sam is gone")


# Initialize unified logger
logger = mylog.LoggerSetup("example", level=logging.DEBUG, logfile=f"{__name__}.log").get_logger()

mylog.LoggerSetup.add_level("NOTICE", 15, "\x1b[1;35;40m" )

mylog.LoggerSetup.add_special_levels()

# Log messages
logger.debug("Debugging details")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical issue")
logger.notice("This is a NOTICE message")

logger.setLevel(1)
# Exclude DEBUG logs from console/file
# setup.add_filter(logging.DEBUG)
logger.debug("This debug message will be filtered out")

logger.tracez("zzzzzzzzzzzzzzzz")
logger.blkonyk

mylog.LoggerSetup.show_all_levels()