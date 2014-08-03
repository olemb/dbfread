# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.0.6'

from .dbf import Table
from .dbf import Table as open  # Alias.
from . import dbf as _dbf

def read(filename, load=True, **kwargs):
    """Read a DBF file and return a list of records.

    Returns a OldStyleTable object which is also a list of records.

    This function is deprecated. Please use open(load=True) instead.
    """
    from warnings import warn
    warn("read() is deprecated. Please use dbfread.open(filename, load=True)")

    return _dbf.OldStyleTable(filename, load=load, **kwargs)
