#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MyLogging.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 20:46:27"
###############################################################################


import logging

print ("mike was here")

# src/MikesToolsLibrary/MyLogging/MyLogging.py
import logging

class MyLogging:
    def __init__(self, name: str = "default"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(name)s | %(levelname)s | %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger