.. dbfread documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dbfread - Read DBF files with Python
====================================

DBF is a file format used by databases such as dBase, Visual FoxPro,
FoxBase+ and Clipper. dbfread makes it easy to get data out of these
files.

.. code-block:: python

    >>> import dbfread
    >>> for record in dbfread.open('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)} 
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

If you also need to write DBF files check out Ethan Furman's `dbf
<https://pypi.python.org/pypi/dbf/0.95.012>`_ package.


Source code
-----------

Latest stable release: http://github.com/olemb/dbfread/

Latest development version: http://github.com/olemb/dbfread/tree/develop/


Contents
------------

.. toctree::
   :maxdepth: 2

   installing
   about_dbf
   lib
   license
   authors
   acknowledgements


Indices and tables
==================

* :ref:`genindex`

* :ref:`modindex`

* :ref:`search`
