#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 22:34:02"
###############################################################################

import logging
import MikesToolsLibrary.MyLogging as mylog
from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter

import os
import sys

# if sys.platform.startswith("win"):
#     os.system("")


# Initialize unified logger
logger = mylog.LoggerSetup("example", logfile=f"{__name__}.log").get_logger()



mylog.add_level("NOTICE", 15, "\x1b[1;35;40m" )




# Log messages
logger.debug("Debugging details")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical issue")
logger.notice("This is a NOTICE message")

# Exclude DEBUG logs from console/file
# setup.add_filter(logging.DEBUG)
logger.debug("This debug message will be filtered out")



