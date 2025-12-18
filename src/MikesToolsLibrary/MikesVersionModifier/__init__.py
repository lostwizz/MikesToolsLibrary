#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MikesSettings package
---------
Custom logging utilities: formatters, levels, and setup helpers.




"""
__version__ = "0.0.1.140-release"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 22:01:22"
###############################################################################

# from .MikesVersionModifier import MikesVersionModifier


from .MikesVersionModifier import update_version_suffix


__all__ = [
    "update_version_suffix",
]
