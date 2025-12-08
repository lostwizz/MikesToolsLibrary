#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
MyLogging.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 20:44:42"
###############################################################################


import logging

print ("mike was here")

def get_logger(FileName:str) -> logging.Logger:
    logger = logging.getLogger(FileName)


    print ("mike was here 2")

    return logger