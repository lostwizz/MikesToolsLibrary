#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 22:49:34"
###############################################################################


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import logging
import MikesToolsLibrary.MyLogging as mylog
# from MikesToolsLibrary.MyLogging.CustomLevels import CustomLevels
# from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter, FormatMode


import pprint

# Initialize unified logger
logger = mylog.LoggerSetup("MikesToolsLibrary", level=logging.DEBUG, logfile=f"MikesToolsLibrary.log").get_logger()


# print("v")
# for h in logger.handlers:
#     if isinstance(h.formatter, CustomFormatter):
#         print (f" Handler Formatter==>{h.formatter=} Handler type: {type(h).__name__}")
# print ("^")
logger.info("Process complete ✓ — all good 🚀")


mylog.LoggerSetup.add_level("NOTICE", 15, "\x1b[1;35;40m" , "‼")
mylog.LoggerSetup.add_special_levels(logger)

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
logger.blkonyk("blkonyk message here")

#mylog.LoggerSetup.show_all_levels(logger, False)
# mylog.LoggerSetup.show_all_levels(logger, True)


alist = ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc", "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", "e"]
logger.traceb( alist)

adict = { "a":1, "b":2, "c":3, "d":4}
logger.tracec(adict)

stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
logger.traced(stuff)

tup = ('spam', ('eggs', ('lumberjack', ('knights', ('ni', ('dead',
('parrot', ('fresh fruit',))))))))

logger.tracee( tup)

# pprint.pp( tup, indent=4, width=40)

logger.tracep("tony is being hit", stuff)

logger.tracet(FormatMode)

try:
    d= 2/0
except Exception:
    logger.error("Something failed", exc_info=True)