#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
setupExample.py




"""
__version__ = "0.0.0.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 21:50:42"
###############################################################################

import os

from MikesToolsLibrary.MikesSettings import MikesSettings

import logging
from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode

# -----------------------------------------------------------------
def check_first_read():

    fx = MikesSettings.findConfigFile("bob.ini")
    logger.tracey( f"Found bob.ini at: {fx}" )
    bob = MikesSettings(fx, "BobApp")
    logger.tracey( bob )

    fn = MikesSettings.findConfigFile()   # look for "config.ini" in current or parent dirs
    logger.info(f"Reading settings from INI file {fn=}...")

    global mySettings
    global GlobalINI
    mySettings = MikesSettings(fn, "MikesToolsLibrary")
    logger.yellow(f"Using settings file: {mySettings.giveINIfile()}")
    logger.traceo(mySettings)

    GlobalINI = MikesSettings( r"D:\GlobalImportantStuff.ini", "GlobalImportantStuff")
    logger.cyan(f"Using global settings file: {GlobalINI.giveINIfile()}")
    logger.tracev(GlobalINI )




# -----------------------------------------------------------------
def lamby1():
    return 42
# -----------------------------------------------------------------
def lamby2():
    return "john was here"
# -----------------------------------------------------------------
def lamby3():
    return 47.47
# -----------------------------------------------------------------
def show_rgister_save_later():
    logger.traceo("Demonstrating register_save_later...")

    # lambda: self.root.winfo_width(
    mySettings.registerToSaveList("Section1", "KeyA", lambda: lamby1(), MikesSettings.fldType.Int)
    mySettings.registerToSaveList("Section2", "KeyB", lambda: lamby2(), MikesSettings.fldType.Str)
    mySettings.registerToSaveList("Section3", "KeyC", lambda: lamby3(), MikesSettings.fldType.Float)

    logger.tracel("Current settings after register_save_later calls:")
    logger.tracel(mySettings)

    mySettings.processSaveLater()
    logger.tracem(mySettings)
    
    mySettings.writeConfig()



# -----------------------------------------------------------------
def check_runcounter():

    app=  mySettings.curApp
    logger.tracez(f"Checking run counter for app: {app}")

    #manually get and set run counter
    count = mySettings.getInt( app, "RunCounters",  0)
    count += 1
    mySettings.setInt( app, "RunCounters", count)
    logger.tracea(f"This program has been run {count} times.")

    # use the purpose-built getRunCounter() method  to increment and get the run counter
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