API Changes
===========

``dbfread.open()`` and ``dbfread.read()`` are deprecated as of version
``1.2``, and will be removed in ``1.4``.

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

``open()`` and ``read()`` both ``DeprecatedDBF``, which is a subclass
of ``DBF`` and ``list`` and thus backward compatible.
