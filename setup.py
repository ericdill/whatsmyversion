#!/usr/bin/env python

import setuptools
from distutils.core import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import theversion

setup(
    name='theversion',
    version=theversion.__version__,
    author='Eric Dill',
    description="Making versioning easy",
    long_description=read('README.rst'),
    pymodules=['theversion'],
    url='http://github.com/ericdill/theversion',
    license='GPL-3',
)
