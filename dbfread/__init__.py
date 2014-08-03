# -*- coding: utf-8 -*-

__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.1.1'

from .dbf import DBF
from .dbf import DBF as open  # Alias.
from . import dbf as _dbf

def read(filename, load=True, **kwargs):
    """Read a DBF file and return a DeprecatedDBF object.

    This function is deprecated. Please use open(load=True) instead.
    """
    from warnings import warn
    warn("read() is deprecated. Please use dbfread.open(filename, load=True)")

    return _dbf.DeprecatedDBF(filename, load=load, **kwargs)
