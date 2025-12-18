#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-11-26 23:31:33"
###############################################################################


from setuptools import setup, find_packages



setup(
    name='Mikes Tools Library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Mike Merrett',
    description='A simple math utility library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/my_library',
)