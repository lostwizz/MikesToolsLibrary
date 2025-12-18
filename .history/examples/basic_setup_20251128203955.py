#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
basic_setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 20:39:55"
###############################################################################

import src.MyLogging as MyLogging

MyLogging.setup_logging()


import MikesToolsLibrary.MyLogging as mylog

mylog.MyLogging.some_function()