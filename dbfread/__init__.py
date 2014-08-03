"""
Read DBF files with Python.

The only function you need is:

    dbfread.open(filename, **kwargs)

which is an alias for:

    dbfread.DBF(filename, **kwargs)
"""
__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'http://nerdly.info/ole/'
__license__ = 'MIT'
__version__ = '1.1.1'

print(__doc__)

from .dbf import DBF
from .dbf import DBF as open  # Alias.
from .deprecated_dbf import DeprecatedDBF as read

# Prevent splat import.
__all__ = []

