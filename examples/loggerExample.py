#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
loggerExample.py


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
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 22:40:28"
###############################################################################


import sys
import os
import time
import logging

from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.log_decorator import log_decorator
from MikesToolsLibrary.MikesLogging import ( log_decorator, log_decoratorPlain,
)
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


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
    print(f"ExcludeLevelFilter {LoggerSetup.showExcludeLevelFilter() }")

    l = logging._nameToLevel.get("NOTICE")
    print(f"level is {l=}")

    LoggerSetup.turnOffLevel(logging._nameToLevel.get("NOTICE"), LoggingMode.CONSOLE)
    print(f"ExcludeLevelFilter {LoggerSetup.showExcludeLevelFilter() }")

    logger.info(
        "the next line is a Notice but will be filtered out in the console (but not the file log)"
    )
    logger.notice(
        "This is a NOTICE message AFTER 2 - should NOT show on the CONSOLE (but will in the log)"
    )
    LoggerSetup.turnOnLevel(
        logging._nameToLevel.get("NOTICE"), LoggingMode.CONSOLE
    )

    logger.notice("This is a NOTICE mes sage AFTER 3 -  should be back and shown")
    # print( ExcludeLevelFilter.Filters)
    print(f"ExcludeLevelFilter {LoggerSetup.showExcludeLevelFilter() }")

    logger.mark()
    LoggerSetup.turnOffLevel(logging._nameToLevel.get("NOTICE"), LoggingMode.FILE)
    # mylog.LoggerSetup.addLevelExclude(15, LoggingMode.FILE)
    print(f"ExcludeLevelFilter {LoggerSetup.showExcludeLevelFilter() }")

    logger.info(
        "the next line is a Notice but will be filtered out in the FILE (but not CONSOLE)  5"
    )
    logger.notice(
        "This is a NOTICE message AFTER 5 - should NOT show on the FILE (but will NOT CONSOLE) 6 "
    )
    LoggerSetup.turnOnLevel(logging._nameToLevel.get("NOTICE"), LoggingMode.FILE)

    logger.notice("This is a NOTICE mes sage AFTER 6 -  should be back and shown 7")
    # print( ExcludeLevelFilter.Filters)
    print(f"ExcludeLevelFilter {LoggerSetup.showExcludeLevelFilter() }")
    logger.notice("some notice")

    LoggerSetup.turnOffLevel(15, LoggingMode.ALL)
    logger.notice(" some other notice")
    print(f"ExcludeLevelFilter A{LoggerSetup.showExcludeLevelFilter() }")
    logger.notice(" some other notice")

    LoggerSetup.turnOnLevel(15, LoggingMode.CONSOLE)
    print(f"ExcludeLevelFilter B{LoggerSetup.showExcludeLevelFilter() }")
    LoggerSetup.turnOnLevel(15, LoggingMode.FILE)
    print(f"ExcludeLevelFilter C{LoggerSetup.showExcludeLevelFilter() }")

    logger.query("some query")
    LoggerSetup.turnOffLevel(55, LoggingMode.FILE)
    logger.query("some query")
    print(f"ExcludeLevelFilter D{LoggerSetup.showExcludeLevelFilter() }")
    logger.query("some query")

    LoggerSetup.turnOnLevel(55, LoggingMode.ALL)
    logger.query("some query")
    print(f"ExcludeLevelFilter D{LoggerSetup.showExcludeLevelFilter() }")

    LoggerSetup.turnOnLevel(15, LoggingMode.ALL)
    print(f"ExcludeLevelFilter Y{LoggerSetup.showExcludeLevelFilter() }")


    LoggerSetup.turnOffLevel(65 )
    print(f"ExcludeLevelFilter Z{LoggerSetup.showExcludeLevelFilter( ) }")
    print(f"ExcludeLevelFilter Z{LoggerSetup.showExcludeLevelFilter(3 ) }")
    print(f"ExcludeLevelFilter Z{LoggerSetup.showExcludeLevelFilter(LoggingMode.CONSOLE | LoggingMode.FILE ) }")
    LoggerSetup.turnOnLevel(65 )
    print(f"ExcludeLevelFilter Z{LoggerSetup.showExcludeLevelFilter( ) }")
    logger.query("some query")
    logger.notice(" some notice")

    logger.mark()

# -------------------
def displayExcludeLevel2():
    logger.mark1()
    # LoggerSetup.turnOffNonStandardLevels(LoggingMode.ALL)
    LoggerSetup.turnOffNonStandardLevels()
    
    print ( logging._nameToLevel.get("MARK1"))
    
    LoggerSetup.show_all_levels(logger)
    LoggerSetup.turnOnLevel( logging._nameToLevel.get("MARK1"))
    logger.mark1()
    
    LoggerSetup.turnOn200s()
    LoggerSetup.show_all_levels(logger)
    LoggerSetup.turnOnLevel( logging._nameToLevel.get("MARK2"))
    logger.mark2()
    
    LoggerSetup.turnOffNonStandardLevels()
    LoggerSetup.turnOn300s()
    LoggerSetup.show_all_levels(logger)
    LoggerSetup.turnOnLevel( logging._nameToLevel.get("MARK3"))
    logger.mark3()
    
    LoggerSetup.turnOffNonStandardLevels()
    LoggerSetup.turnOn600s()
    LoggerSetup.show_all_levels(logger)
    LoggerSetup.turnOnLevel( logging._nameToLevel.get("MARK4"))
    logger.mark4()

    LoggerSetup.turnOnNonStandardLevels()
    LoggerSetup.show_all_levels(logger)
    LoggerSetup.turnOnLevel( logging._nameToLevel.get("MARK5"))
    logger.mark5()


    
# -------------------
def checkLoggerLevel():

    logger.setLevel(1)
    logger.debug("This debug message will be filtered out")
    # Exclude DEBUG logs from console/file
    # setup.add_filter(logging.DEBUG)

    logger.tracez("zzzzzzzzzzzzzzzz")


# -------------------
def showLevelInfo():
    LoggerSetup.show_all_levels(logger)
    # mylog.LoggerSetup.showColorSampler()


# -------------------
@log_decorator
def freddy(a, b, c):
    print(a)
    print(f"{b}")
    print(f"{c=}")
    return a + b


# @log_decoratorPlain
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

    logger.tracet(LoggingMode)

    # print ( isinstance(LoggingMode, Enum))
    logger.traceq(LoggingMode.CONSOLE)

    try:
        d = 2 / 0
    except Exception:
        # logger.error("Something failed", exc_info=False)
        logger.error("Something failed", exc_info=True)
        # logger.error("Something failed")
        logger.exception("Something Failed again")


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

    
    logger.blue("a message", extra={"user_id": "123", "ip": "192.168.1.1"})
    logger.warning("bye")

# -------------------
def checkRotatinglogs(setup, mode):
    setup.force_rollover(mode)
    logger.tracea( "this should be the online line in the log file")
    time.sleep(60)
    logger.tracea( "this should be the online line in the log file")
    showLevelInfo()
    logger.traceb( "this should be the online line in the log file")




# -------------------
# -------------------



# -------------------
def main():
    global logger

    LogSetup = LoggerSetup(
        "MikesToolsLibrary",
        level=logging.DEBUG,
        logfile=".\logs\MikesToolsLibrary.log",
        modes=LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR #| LoggingMode.ROTATINGFN,  # | LoggingMode.SMTP,
    )

    logger = LogSetup.get_logger()

    checkCustomLevels()
    showLevelInfo()
    checkDecorator()
    checkLoggerLevel()
    checkTypesOutput()
    checkMultipleArgs()
    displayExcludeLevel()
    displayExcludeLevel2()
    # checkSMTP()

    checkRotatinglogs(LogSetup, LoggingMode.TIMEDROTATOR)
    checkRotatinglogs(LogSetup, LoggingMode.ROTATINGFN)


    LoggingMode.CONSOLE.showModes()

if __name__ == "__main__":
    main()
