#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

# import shutil
import sys

# import itertools

from setuptools import setup, find_packages

# from setuptools.command.install import install
# from distutils.dir_util import copy_tree

readme = ""
with open("README.rst") as f:
    readme = f.read()

setup(
    name="wslinklc",
    version="0.0.1",
    description="Python/JavaScript library for communicating over WebSocket, with workarounds to publish messages synchronously, by Luminary. A fork of https://github.com/kitware/wslink",
    long_description=readme,
    author="Kitware, Inc.",
    author_email="yasushi.saito@gmail.com",
    url="https://github.com/yasushi-saito/wslink",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="websocket javascript rpc pubsub",
    packages=find_packages("src", exclude=("tests.*", "tests")),
    package_dir={"": "src"},
    install_requires=["aiohttp"],
)
