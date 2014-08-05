dbfread - Read DBF files with Python
====================================

DBF is a file format used by databases such as dBase, Visual FoxPro,
FoxBase+ and Clipper. dbfread makes it easy to get data out of these
files.

If you also need to write DBF files check out Ethan Furman's `dbf
<https://pypi.python.org/pypi/dbf/0.95.012>`_ package.


Example
-------

To read records from a DBF file::

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

By default the ``DBF`` object will stream records directly from the
file.  If you have enough memory you can load the records into a
list. This allows for random access::

    >>> table = DBF('people.dbf')
    >>> table.records[1]
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Full documentation at http://dbfread.readthedocs.org/


Main Features
-------------

* written for Python 3 (but also works in 2.7).

* records are returned as dictionaries with native Python data
  types. Can also use ordered dictionaries and custom record types.

* aims to handle all variants of DBF files. (Currently only widely
  tested with Visual FoxPro, but all other files have worked so far.)

* reads all 9 commonly used field types. New types can be added by
  subclassing ``FieldParser``.

* reads ``.FPT`` memo files with both text and binary memos (and soon
  ``.DBT`` files).

* handles mixed case file names gracefully on case sensitive file systems.

* can retrieve deleted records.


Installing
----------

Requires Python 3.2 or 2.7.

::

  pip install dbfread

``dbfread`` is a pure Python module, so doesn't depend on any packages
outside the standard library.

To build documentation locally::

    python setup.py docs

This requires Sphinx. The resulting files can be found in
``docs/_build/``.


Source code
------------

Latest stable release: http://github.com/olemb/dbfread/

Development version: http://github.com/olemb/dbfread/tree/develop/


License
-------

dbfread is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.


Contact
-------

Ole Martin Bjorndalen - ombdalen@gmail.com
