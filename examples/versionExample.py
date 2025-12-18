#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
versionExample.py

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
__version__ = "0.0.0.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 22:54:33"
###############################################################################



from MikesToolsLibrary.MikesSettings import MikesSettings

import logging
from MikesToolsLibrary.MikesLogging.LoggerSetup import LoggerSetup
from MikesToolsLibrary.MikesLogging.LoggingMode import LoggingMode
from MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier import update_version_suffix
#    MikesToolsLibrary\MikesVersionModifier\MikesVersionModifier.py
#-----------------------------------------------------------------


# try:
#     import tomllib  # Python 3.11+
#     with open("pyproject.toml", "rb") as f:
#         data = tomllib.load(f)
#     print(data["project"]["version"])

# except Exception:
#    print("Something Failed again")

#-----------------------------------------------------------------

def main():
    """
    Main function to update version in all .py files in a directory.
    """
    LogSetup = LoggerSetup(
        "MikesToolsLibrary",
        level=logging.DEBUG,
        logfile=".\logs\MikesToolsLibrary.log",
        modes=LoggingMode.CONSOLE | LoggingMode.TIMEDROTATOR #| LoggingMode.ROTATINGFN,  # | LoggingMode.SMTP,
    )

    global logger
    logger = LogSetup.get_logger()

    fn = MikesSettings.findConfigFile()   # look for "config.ini" in current or parent dirs
    logger.info(f"Reading settings from INI file {fn=}...")
    mySettings = MikesSettings(fn,'MikesToolsLibrary')

    r = mySettings.getRunCounter()
    logger.traceu( f"Run counter value from getRunCounter(): {r}" )


    # Example usage:
    # directory = "path/to/your/code"
    directory = "D:\_Python_Projects\MikesToolsLibrary"
    new_suffix = f"{r}-release"



    update_version_suffix(directory, new_suffix, logger)

#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

#-----------------------------------------------------------------
if __name__ == "__main__":
    main()