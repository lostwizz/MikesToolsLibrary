#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
__init__.py

MikesSettings package
---------
Custom logging utilities: formatters, levels, and setup helpers.




"""
__version__ = "0.3.5.0-143-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-17 22:06:07"
###############################################################################


# version_utils.py
import pathlib
import sys

try:
    # Python 3.11+ has tomllib in the stdlib
    import tomllib
except ImportError:
    import tomli as tomllib  # fallback for older versions

def get_version() -> str:
    """
    Reads the version string from pyproject.toml.
    Returns it as a string, e.g. "1.2.3".
    """
    pyproject_path = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    # Works with PEP 621 standard metadata
    return data["project"]["version"]
