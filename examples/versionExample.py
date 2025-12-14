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
__version__ = "0.0.0.0036"
__author__ = "Mike Merrett"
__updated__ = "2025-12-13 18:12:44"
###############################################################################

try:
    import tomllib  # Python 3.11+
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    print(data["project"]["version"])

except Exception:
   print("Something Failed again")


