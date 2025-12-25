#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
version_utils.py


---------
Custom logging utilities: formatters, levels, and setup helpers.




"""
__version__ = "0.1.2.00322-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-24 19:14:37"
###############################################################################


# version_utils.py
import pathlib
import sys

try:
    # Python 3.11+ has tomllib in the stdlib
    import tomllib
except ImportError:
    import toml as tomllib  # fallback for older versions

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
