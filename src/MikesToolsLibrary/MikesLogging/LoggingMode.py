#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
LoggingMode.py




"""
__version__ = "0.3.1.00193-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 22:25:03"
###############################################################################
import sys

from enum import Enum, IntFlag, unique, auto

###############################################################################
@unique
class LoggingMode(IntFlag):
    def _generate_next_value_(name, start, count, last_values):
        # Ensure auto() generates powers of two, not sequential integers
        return 1 << count

    CONSOLE = auto()  # 0b0000_0000_0001
    FILE = auto()  # 0b0000_0000_0010
    JSON = auto()  # 0b0000_0000_0100
    SMTP = auto()  # 0b0000__0000_0000_1000
    ROTATINGFN= auto()  # 0b1000_0000_0000
    TIMEDROTATOR = auto()  # 0b0001_0000_0000_0000
    # SYSLOG = auto()   #0b0000_0001_0000
    # HTTP = auto()   #0b0000_0010_0000
    # QUEUE = auto()   #0b0000_0100_0000
    # MEMORY = auto()   #0b0000_1000_0000
    # DATABASE = auto()   #0b0001_0000_0000
    # CLOUD = auto()   #0b0010_0000_0000
    # EXTERNAL = auto()   #0b0100_0000_0000

    ALL = (
        CONSOLE
        | FILE
        | JSON
        | SMTP
        | ROTATINGFN
        | TIMEDROTATOR
        # | SYSLOG
        # | HTTP
        # | QUEUE
        # | MEMORY
        # | DATABASE
        # | CLOUD
        # | EXTERNAL
        )

    # -----------------------------------------------------------------
    def __str__(self):
        return f'LoggingMode: {format(self.value)}'

    # -----------------------------------------------------------------
    def showModes(self):
        for mode in LoggingMode:
            print(f"{mode.name} = {mode.value:_b}")


# -----------------------------------------------------------------
def iter_flags(mask: LoggingMode) -> list[LoggingMode]:
    """Yield individual flags contained in a mask (excluding 0)."""
    return [m for m in LoggingMode if m != 0 and (mask & m) == m]



# -----------------------------------------------------------------
if __name__ == '__main__':
    """
    This is the main function that runs when the script is executed directly.
    It sets up the logger and demonstrates the usage of the CustomFormatter class.
    """
    print("You should not run this file directly, it is a module to be imported.")
    sys.exit(-99)
