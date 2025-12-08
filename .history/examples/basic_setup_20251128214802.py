#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 21:48:02"
###############################################################################

# from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup

# from .CustomLevels import CustomLevels
import MikesToolsLibrary.MyLogging as mylog



# Initialize unified logger

logger = mylog.LoggerSetup("example", log).get_logger()



mylog.CustomLevels.add_log_level("NOTICE", 15)




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



