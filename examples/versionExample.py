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
__version__ = "0.1.2.00322-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-24 19:26:57"
###############################################################################



# from MikesToolsLibrary.MikesSettings import MikesSettings

# import logging


from MikesToolsLibrary.MikesLogging import get_logger
from MikesToolsLibrary.MikesSettings import MikesSettings
from MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier import (
    load_version_file,
    save_version_file,
    update_tree,
)
logger = get_logger(__name__)


from MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier import update_version_suffix


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

    # logger = LoggerSetup().get_logger("version_modifier")

    
    fn = MikesSettings.findConfigFile()   # look for "config.ini" in current or parent dirs
    logger.info(f"Reading settings from INI file {fn=}...")
    mySettings = MikesSettings(fn,'MikesToolsLibrary')

    r = mySettings.getRunCounter()
    logger.traceu( f"Run counter value from getRunCounter(): {r}" )


    logger.tracea("hello world")

    # Example usage:
    # directory = "path/to/your/code"
    directory = "D:\_Python_Projects\MikesToolsLibrary"
    new_suffix = f"{r}-dev"



    # MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier ( suffix= 'dev' ,["bump build"])


    # update_version_suffix(directory, new_suffix, logger)

    # update_version_suffix(
    #     directory,
    #     new_suffix=new_suffix,
    #     bump="major",
    #     set_values={"minor":3, "patch":5},
    #     logger=logger
    # )

    update_version_suffix(
        directory,
        # new_suffix = f"{r}-dev"
        new_suffix=new_suffix ,
        set_values={"major":0,"minor":1,"patch":2, "build": r},
        logger=logger
    )

    # update_version_suffix(
    #     "D:/_Python_Projects/MikesToolsLibrary",
    #     new_suffix=new_suffix,
    #     # bump=["minor", "patch"]
    # )

#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

#-----------------------------------------------------------------
if __name__ == "__main__":
    main()