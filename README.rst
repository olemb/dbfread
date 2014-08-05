dbfread - Read DBF Files with Python
====================================
 
DBF is a file format used by databases such dBase, Visual FoxPro, and
FoxBase+. This library reads DBF files and returns the data as native
Python data types for further processing. It is primarily intended for
batch jobs and one-off scripts.

If you need to write DBF files check out `dbfpy
<https://pypi.python.org/pypi/dbfpy/>`_


Example
-------

To read records from a DBF file::

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
    OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])

By default the ``DBF`` object will stream records directly from the
file.  If you have enough memory you can load the records into a
list instead. This allows for random access::

    >>> table = DBF('people.dbf', load=True)
    >>> print(table.records[1]['NAME'])
    Bob
    >>> print(table.records[0]['NAME'])
    Alice

Full documentation at http://dbfread.readthedocs.org/


Main Features
-------------

* written for Python 3, but also works in 2.7

* simple but flexible API

* data is returned as native Python data types

* records are ordered dictionaries, but can be recofigured to be of
  any type

* aims to handle all variants of DBF files. (Currently only widely
  tested with Visual FoxPro, but should work well with other
  variants.)

* support for 9 widely used field types with more to come. Custom
  types can be added by subclassing ``FieldParser``

* reads ``.FPT`` memo files with both text and binary memos (and soon
  ``.DBT`` files)

* handles mixed case file names gracefully on case sensitive file systems

* can retrieve deleted records


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


API Changes
-----------

The ``dbfread.open()`` and ``dbfread.read()`` functions are deprecated
as of version ``1.2``, and ``DBF()`` is used instead. They will be
removed in ``1.4``.

Also, the ``DBF`` class is no longer a subclass of ``list``. This
makes the API a lot cleaner and easier to understand, but old code
that relied on this behaviour will be broken. Iteration and record
counting works the same as before. Other list operations can be
rewritten using the ``record`` attribute. For example::

    table = dbfread.read('people.dbf')
    print(table[1])

can be rewritten as::

    table = DBF('people.dbf', load=True)
    print(table.records[1])

``open()`` and ``read()`` return the old style class
``DeprecatedDBF``, which is a subclass of ``DBF`` and ``list`` and
thus backward compatible.


License
-------

dbfread is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.


Contact
-------

Ole Martin Bjorndalen - ombdalen@gmail.com
