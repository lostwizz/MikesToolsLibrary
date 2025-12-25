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
__version__ = "0.0.3.00354-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-24 21:43:21"
###############################################################################



# from MikesToolsLibrary.MikesSettings import MikesSettings

# import logging


from MikesToolsLibrary.MikesLogging import get_logger
from MikesToolsLibrary.MikesSettings import MikesSettings
from MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier import (
    load_version_file,
    save_version_file,
    update_tree,
    apply_bumps,
    apply_set_values,
)
logger = get_logger(__name__)
logger.rocket("Logger Loaded - and it checks out",   extra={ "special": True})


from MikesToolsLibrary.MikesVersionModifier.MikesVersionModifier import update_version_suffix


def dry_run_version_update(directory, new_suffix=None, bump=None, set_values=None, logger=None):
    """
    Perform a dry-run version update: load, modify, and simulate updating files without saving.
    """
    version = load_version_file("version.toml", logger=logger)

    if set_values:
        apply_set_values(version, set_values)

    if bump:
        apply_bumps(version, bump)

    if new_suffix:
        version.suffix = new_suffix

    logger.info(f"Dry-run: New version would be: {version.as_string()}")

    # Simulate updating tree without saving version file or modifying files
    changed_files = update_tree(directory, version, dry_run=True, logger=logger)
    logger.info(f"Dry-run: Would update {len(changed_files)} files (but none were changed)")


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
    new_suffix = "dev"

    # Dry-run example
    logger.info("Performing dry-run version update...")
    dry_run_version_update(
        directory,
        new_suffix=new_suffix,
        set_values={"major": 0, "minor": 0, "patch": 3, "build": r, "suffix": "-postdev"},
        logger=logger
    )

    # Actual update (commented out for safety)
    # update_version_suffix(
    #     directory,
    #     new_suffix=new_suffix,
    #     set_values={"major": 0, "minor": 0, "patch": 3, "build": r, "suffix": "-postdev"},
    #     logger=logger
    # )

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