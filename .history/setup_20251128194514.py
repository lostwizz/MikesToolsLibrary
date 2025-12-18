#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
r"""
setup.py




"""
__version__ = "0.0.0.0036.115-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-11-28 19:45:14"
###############################################################################


from setuptools import setup, find_packages



setup(
    name='Mikes_Tools_Library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Mike Merrett',
    author_email='public@merrett.ca',
    description='Mikes Tools Library - A collection of useful Python tools and utilities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/my_library',
 python_requires='>=3.6'
)