# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.0.6'

from .dbf import Table

open = Table

def read(filename, load=True, **kwargs):
    """Read a DBF file and return a list of records.

    Returns a Table object which is also a list of records.
    This is an alias for open(filename, load=True).
    """
    return open(filename, load=load, **kwargs)
