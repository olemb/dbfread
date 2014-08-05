API Changes
===========

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
