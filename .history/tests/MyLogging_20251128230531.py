#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
Simple compatibility script used by tests to validate behavior expected by
`tests/test_MyLogging.py`.

The test expects that importing this file prints "mike was here" and that the
`get_logger` function prints "mike was here 2" and returns a logging.Logger
instance with the requested name.
"""
__version__ = "0.0.0.0001"

import logging

# Print a message at import time so tests can capture it
print("mike was here")

# The test injects a `Logger` name in the runpy globals when it runs this file
# which allows the annotation `-> Logger` to work in that environment.
def get_logger(FileName: str) -> "Logger":
    logger = logging.getLogger(FileName)
    print("mike was here 2")
    return logger
