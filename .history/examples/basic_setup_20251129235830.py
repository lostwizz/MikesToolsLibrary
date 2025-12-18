#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-11-29 23:58:30"
###############################################################################


import sys
import os

from MikesToolsLibrary.MyLogging import log_decorator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import logging
import MikesToolsLibrary.MyLogging as mylog
from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter, FormatMode
from MikesToolsLibrary.MyLogging.log_decorator import log_decorator,log_decoratorPlain

# import pprint

@log_decorator
def freddy( a, b,c):
    print (a)
    print(f"{b}")
    print (f"{c=}")
    return a+ b 

@log_decoratorPlain
def freddy2( a, b,c):
    print (a)
    print(f"{b}")
    print (f"{c=}")
    return a+ b 

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
logger.blkonyk("blkonyk message here")
logger.debug("Debugging details")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical issue")
logger.notice("This is a NOTICE message")

logger.setLevel(0)
logger.debug("This debug message will be filtered out")
# Exclude DEBUG logs from console/file
# setup.add_filter(logging.DEBUG)

logger.tracez("zzzzzzzzzzzzzzzz")

#mylog.LoggerSetup.show_all_levels(logger, False)
# mylog.LoggerSetup.show_all_levels(logger, True)


x = freddy("sam was here ", "tom is gone", 777)
y = freddy2("sam was herexxx ", "tom is gonexxxxxxxx", 87778)



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

# print ( isinstance(FormatMode, Enum))
logger.traceq(FormatMode.CONSOLE)

try:
    d= 2/0
except Exception:
    # logger.error("Something failed", exc_info=False)
    logger.error("Something failed", exc_info=True)
    # logger.error("Something failed")