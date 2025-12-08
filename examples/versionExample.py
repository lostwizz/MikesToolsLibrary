#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
versionExample.py




"""
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-07 19:51:47"
###############################################################################

import tomllib  # Python 3.11+
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data["project"]["version"])

