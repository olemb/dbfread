"""
Read DBF files with Python.

Functions:

    table = open(filename, **kwargs)

    # Alternative name for the same function.
    table = DBF(filename, **kwargs)

Example:

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

    >>> table = DBF('people.dbf', load=True)
    >>> table.records[0]
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}

See README.rst for full documentation.

"""
__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.1.1'

from .dbf import DBF
from .deprecated_dbf import open, read
from .exceptions import *
from .field_parser import FieldParser, InvalidValue

# Prevent splat import.
__all__ = []
