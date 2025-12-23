#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
encryptionExample.py




"""
__version__ = "0.1.2.00213-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-18 21:27:02"
###############################################################################

import os


from MikesToolsLibrary.MikesEncryption import MikesEncryption

from MikesToolsLibrary.MikesSettings import MikesSettings

import logging
from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode


# -----------------------------------------------------------------
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

    encryptor = MikesEncryption()

    root = encryptor.giveRoot()
    print(f"Root  is: '{root}'")

    logger.info(f"Reading settings from INI file" + root + "GlobalImportantStuff.ini" + "...")
    global GlobalINI
    GlobalINI = MikesSettings(root + "GlobalImportantStuff.ini", "GlobalImportantStuff")
    print(f"GlobalINI settings: {GlobalINI}")

    fn = MikesSettings.findConfigFile()   # look for "config.ini" in current or parent dirs
    logger.info(f"Reading settings from INI file {fn=}...")
    global mySettings
    mySettings = MikesSettings(fn, "MikesToolsLibrary")
    print(f"My settings: {mySettings}")

    rCount = mySettings.getRunCounter()

    p = r"\\vm-gis-prd1\gis_manager\Data\Projects\ProjectA"
    root = encryptor.giveRoot(p)
    print(f"Root of '{p}' is: '{root}'")


# -----------------------------------------------------------------
if __name__ == '__main__':
    main()
