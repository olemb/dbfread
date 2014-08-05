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

If you have enough memory you can load the records into a list by
passing ``load=True`` or calling the ``load()`` method. This allows
for random access::

    >>> table = DBF('people.dbf', load=True)
    >>> table.records[0]
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}

Iteration and ``len(table)`` work the same way with loaded and
unloaded tables. Deleted records are available in the ``deleted``
attribute and behave just like normal records.

``dbfread`` will detect most commonly used character encodings. If you
get decording errors you can use the keyword argument ``encoding`` to
override the detected encoding.

Full documentation at http://dbfread.readthedocs.org/


Main Features
-------------

* dirt simple API.

* written for Python 3. (Also works in 2.7.)

* iterate over records directly from file or keep them in a list.

* full support for all 9 commonly used field types. New types can
  be added by subclassing ``FieldParser``.

* DBF class with many options and attributes.

* full support for ``.FPT`` memo files.

* handles mixed case file names gracefully by ignoring case.

* reads deleted records separately.


Status
------

Various incarnations of the library has been used since 2001 to read
Visual FoxPro files with a wide range of data types. It is not widely
tested with other DBF formats but should still work for most files.

I intend for dbfread to be able to read any DBF file. If you have a
file it can't read, or you find a bug, I'd love to hear from you.


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
