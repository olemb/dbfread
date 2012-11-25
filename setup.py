# -*- coding: utf-8 -*-

import os
import sys
import dbfread

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

#if sys.argv[-1] == "test":
#    os.system("python test_dbfread.py")
#    sys.exit()

required = []

setup(
    name='dbfread',
    version=dbfread.__version__,
    description='read data from dbf files',
    long_description=open('README.rst').read(),
    author=dbfread.__author__,
    email=dbfread.__email__,
    url=dbfread.__url__,
    packages=[
        'dbfread',
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
