#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import dbfget

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

#if sys.argv[-1] == "test":
#    os.system("python test_dbfget.py")
#    sys.exit()

required = []

setup(
    name='dbfget',
    version=dbfget.__version__,
    description='easily fetch data from dbf files',
    long_description=open('README.rst').read(),
    author=dbfget.__author__,
    email=dbfget.__email__,
    url=dbfget.__url__,
    packages=[
        'dbfget',
    ],
    py_modules=[
    ],
    # install_requires=required,  # Unknown option in Python 3
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
    ),
)
