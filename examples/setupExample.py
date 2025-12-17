#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
setupExample.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-16 22:11:09"
###############################################################################

import os

from MikesToolsLibrary.MikesSettings import MikesSettings

import logging
from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode

# -----------------------------------------------------------------
def check_first_read():
    if os.path.exists("../config.ini"):
        fn = "../config.ini"
    else:
        fn = "config.ini"

    logger.info(f"Reading settings from INI file {fn=}...")

    global mySettings
    global GlobalINI
    mySettings = MikesSettings(fn, "MikesToolsLibrary")
    logger.yellow(f"Using settings file: {mySettings.giveINIfile()}")
    logger.traceo(mySettings)

    GlobalINI = MikesSettings( r"D:\GlobalImportantStuff.ini", "GlobalImportantStuff")
    logger.cyan(f"Using global settings file: {GlobalINI.giveINIfile()}")
    logger.tracev(GlobalINI )

    # print("My Settings:")
    # logger.tracet("hi")


    # print(mySettings.dump())
    # print("\nGlobal INI Settings:")
    # print(GlobalINI.getAllSettingsDict())


# -----------------------------------------------------------------
def show_rgister_save_later():
    logger.traceo("Demonstrating register_save_later...")

    mySettings.registerToSaveList("Section1", "KeyA", "ValueA", "Str")
    mySettings.registerToSaveList("Section1", "KeyB", "ValueB", "Str")
    mySettings.registerToSaveList("Section2", "KeyC", "ValueC", "Str")

    logger.tracel("Current settings after register_save_later calls:")
    logger.tracel(mySettings)


# -----------------------------------------------------------------
def check_runcounter():

    app=  mySettings.curApp
    logger.tracez(f"Checking run counter for app: {app}")
    
    count = mySettings.getInt( app, "RunCounters",  0)
    count += 1
    mySettings.setInt( app, "RunCounters", count)
    logger.tracea(f"This program has been run {count} times.")

    r = mySettings.getRunCounter()
    logger.tracew( f"Run counter value from getRunCounter(): {r}" )

    logger.tracek( mySettings )


# -----------------------------------------------------------------
def main():

    LogSetup = LoggerSetup(
        "MikesToolsLibrary",
        level=logging.DEBUG,
        logfile=".\logs\MikesToolsLibrary.log",
        modes=LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR #| LoggingMode.ROTATINGFN,  # | LoggingMode.SMTP,
    )

    global logger
    logger = LogSetup.get_logger()

    logger.info("Checking Process complete ✓ — all good 🚀")

    check_first_read()
    show_rgister_save_later()
    check_runcounter()


# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------
if __name__ == "__main__":
    main()