dbfread - Read DBF Files with Python
====================================

DBF is a file format used by databases such dBase, Visual FoxPro, and
FoxBase+. This library reads DBF files and returns the data as native
Python data types for further processing. It is primarily intended for
batch jobs and one-off scripts.

.. code-block:: python

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

In older versions where dictionaries are not ordered you will instead get a
``collections.OrderedDict``:

.. code-block:: python

    >>> for record in DBF('people.dbf'):
    ...     print(record)
    OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
    OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])

By default records are streamed directly from the file.  If you have
enough memory you can instead load them into a list. This allows for
random access:

.. code-block:: python

    >>> table = DBF('people.dbf', load=True)
    >>> print(table.records[1]['NAME'])
    Bob
    >>> print(table.records[0]['NAME'])
    Alice

Full documentation at https://dbfread.readthedocs.io/

See docs/changes.rst for a full list of changes in each version.


Main Features
-------------

* tested on Python versions 2.7, 3.6, 3.7, 3.8, 3.9, 3.10, pypy, and pypy3

* simple but flexible API

* data is returned as native Python data types

* records are ordered dictionaries, but can be reconfigured to be of
  any type

* aims to handle all variants of DBF files. (Currently only widely
  tested with Visual FoxPro, but should work well with other
  variants.)

* support for 18 field types. Custom types can be added by subclassing
  ``FieldParser``

* reads ``FPT`` and ``DBT`` memo files, both text and binary data

* handles mixed case file names gracefully on case sensitive file systems

* can retrieve deleted records


Installing
----------

Requires Python 2.7, 3.6, 3.7, 3.8, 3.9, 3.10, pypy, or pypy3.

::

  pip install dbfread

``dbfread`` is a pure Python module and doesn't depend on any packages
outside the standard library.

To build documentation locally::

    python setup.py docs

This requires Sphinx. The resulting files can be found in
``docs/_build/``.


Source code
------------

http://github.com/olemb/dbfread/


API Changes
-----------

``dbfread.open()`` and ``dbfread.read()`` are deprecated as of version
``2.0``, and will be removed in ``2.2``.

The ``DBF`` class is no longer a subclass of ``list``. This makes the
API a lot cleaner and easier to understand, but old code that relied
on this behaviour will be broken. Iteration and record counting works
the same as before. Other list operations can be rewritten using the
``record`` attribute. For example::

    table = dbfread.read('people.dbf')
    print(table[1])

can be rewritten as::

    table = DBF('people.dbf', load=True)
    print(table.records[1])

``open()`` and ``read()`` both return ``DeprecatedDBF``, which is a
subclass of ``DBF`` and ``list`` and thus backward compatible.


License
-------

dbfread is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.


Contact
-------

Ole Martin Bjorndalen - ombdalen@gmail.com
