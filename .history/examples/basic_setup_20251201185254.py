#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-01 18:52:54"
###############################################################################


import sys
import os


# from MikesToolsLibrary.MyLogging.ExcludeLevelFilter import ExcludeLevelFilter

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
import logging

# from MikesToolsLibrary.MyLogging import log_decorator
# import MikesToolsLibrary.MyLogging as mylog
# from MikesToolsLibrary.MyLogging.CustomFormatter import CustomFormatter, FormatMode
# from MikesToolsLibrary.MyLogging.log_decorator import log_decorator, log_decoratorPlain

# from MikesToolsLibrary.MyLogging import CustomFormatter

# from MikesToolsLibrary.MyLogging import CustomFormatter, FormatMode, log_decorator
from MikesToolsLibrary.MyLogging import (
    LoggerSetup,
    CustomFormatter,
    FormatMode,
    log_decorator,
    # log_decoratorPlain,
)
from MikesToolsLibrary.MyLogging.LoggerSetup import LoggerSetup



# import pprint


# Initialize unified logger
# logger = mylog.LoggerSetup(
#     "MikesToolsLibrary", level=logging.DEBUG, logfile=f"MikesToolsLibrary.log"
# ).get_logger()

logger = LoggerSetup("MikesToolsLibrary", level=logging.DEBUG, logfile="MikesToolsLibrary.log").get_logger()



# -------------------
def checkCustomLevels():
    # print("v")
    # for h in logger.handlers:
    #     if isinstance(h.formatter, CustomFormatter):
    #         print (f" Handler Formatter==>{h.formatter=} Handler type: {type(h).__name__}")
    # print ("^")
    logger.info("Process complete ✓ — all good 🚀")

    LoggerSetup.add_level("NOTICE", 15, "\x1b[1;35;40m", "‼")
    LoggerSetup.add_special_levels(logger)

    # Log messages
    logger.blkonyk("blkonyk message here")
    logger.debug("Debugging details")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error occurred")
    logger.critical("Critical issue")
    logger.notice("This is a NOTICE message-a")
    logger.notice("This is a NOTICE message-b")


# -------------------
def displayExcludeLevel():
    logger.notice("This is a NOTICE message 1")
    # print( ExcludeLevelFilter.Filters)
    print(f"ExcludeLevelFilter {mylog.LoggerSetup.showExcludeLevelFilter() }")

    l = logging._nameToLevel.get("NOTICE")
    print(f"level is {l=}")

    mylog.LoggerSetup.addLevelExclude(
        logging._nameToLevel.get("NOTICE"), FormatMode.CONSOLE
    )
    print(f"ExcludeLevelFilter {mylog.LoggerSetup.showExcludeLevelFilter() }")

    logger.info(
        "the next line is a Notice but will be filtered out in the console (but not the file log)"
    )
    logger.notice(
        "This is a NOTICE message AFTER 2 - should NOT show on the CONSOLE (but will in the log)"
    )
    mylog.LoggerSetup.removeLevelExclude(
        logging._nameToLevel.get("NOTICE"), FormatMode.CONSOLE
    )

    logger.notice("This is a NOTICE mes sage AFTER 3 -  should be back and shown")
    # print( ExcludeLevelFilter.Filters)
    print(f"ExcludeLevelFilter {mylog.LoggerSetup.showExcludeLevelFilter() }")

    logger.mark()
    mylog.LoggerSetup.addLevelExclude(
        logging._nameToLevel.get("NOTICE"), FormatMode.FILE
    )
    # mylog.LoggerSetup.addLevelExclude(15, FormatMode.FILE)
    print(f"ExcludeLevelFilter {mylog.LoggerSetup.showExcludeLevelFilter() }")

    logger.info(
        "the next line is a Notice but will be filtered out in the FILE (but not CONSOLE)  5"
    )
    logger.notice(
        "This is a NOTICE message AFTER 5 - should NOT show on the FILE (but will NOT CONSOLE) 6 "
    )
    mylog.LoggerSetup.removeLevelExclude(
        logging._nameToLevel.get("NOTICE"), FormatMode.FILE
    )

    logger.notice("This is a NOTICE mes sage AFTER 6 -  should be back and shown 7")
    # print( ExcludeLevelFilter.Filters)
    print(f"ExcludeLevelFilter {mylog.LoggerSetup.showExcludeLevelFilter() }")

    logger.mark()


# -------------------
def checkLoggerLevel():

    logger.setLevel(1)
    logger.debug("This debug message will be filtered out")
    # Exclude DEBUG logs from console/file
    # setup.add_filter(logging.DEBUG)

    logger.tracez("zzzzzzzzzzzzzzzz")


# -------------------
def showLevelInfo():
    mylog.LoggerSetup.show_all_levels(logger)
    # mylog.LoggerSetup.showColorSampler()


# -------------------
@log_decorator
def freddy(a, b, c):
    print(a)
    print(f"{b}")
    print(f"{c=}")
    return a + b


@log_decoratorPlain
def freddy2(a, b, c):
    print(a)
    print(f"{b}")
    print(f"{c=}")
    return a + b


def checkDecorator():
    x = freddy("sam was here ", "tom is gone", 777)
    y = freddy2("sam was herexxx ", "tom is gonexxxxxxxx", 87778)


# -------------------
def checkTypesOutput():

    print("VVVVVVVVVVVVVVVVVVVVVVVVVVVV")
    for name, logger in logging.Logger.manager.loggerDict.items():
        print(name, logger)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    print(logger.getEffectiveLevel())

    alist = [
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
        "e",
    ]
    logger.traceb(alist)

    adict = {"a": 1, "b": 2, "c": 3, "d": 4}
    logger.tracec(adict)

    stuff = ["spam", "eggs", "lumberjack", "knights", "ni"]
    logger.traced(stuff)

    tup = (
        "spam",
        (
            "eggs",
            ("lumberjack", ("knights", ("ni", ("dead", ("parrot", ("fresh fruit",)))))),
        ),
    )

    logger.tracee(tup)

    # pprint.pp( tup, indent=4, width=40)

    logger.tracep("tony is being hit", stuff)

    logger.tracet(FormatMode)

    # print ( isinstance(FormatMode, Enum))
    logger.traceq(FormatMode.CONSOLE)

    try:
        d = 2 / 0
    except Exception:
        # logger.error("Something failed", exc_info=False)
        logger.error("Something failed", exc_info=True)
        # logger.error("Something failed")


# -------------------
def checkSMTP():
    logger.smtp("This is some sort of email!!")
    logger.smtp("This is some sort of email!!", [1, 2, 3, 4, 5, 6], {"a": 1, "b": 2})


# -------------------
def checkMultipleArgs():
    logger.warning("hi")
    logger.info("This is some sort of message with args", "a", "b", "c", "d", "e", "f")
    logger.tracea(
        "This is some sort of mmessage with args", "a", "b", "c", "d", "e", "f"
    )
    logger.rocket("some message", "and some arg", "and another arg")

    logger.check("check msg", [1, 2, 3, 4, 5, 6], {"a": 1, "b": 2})
    logger.warning("bye")


# -------------------
# -------------------
# -------------------
# -------------------

def main():
    checkCustomLevels()
    showLevelInfo()
    checkDecorator()
    checkLoggerLevel()
    checkTypesOutput()
    checkMultipleArgs()
    displayExcludeLevel()
    # checkSMTP()

if __name__ == "__main__":
    main()
