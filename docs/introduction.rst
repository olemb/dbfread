Introduction
============

If you want to follow along you can find ``people.dbf`` in
``examples/files/``.


Opening a DBF File
------------------

... code-block:: python

    >>> from dbfread import DBF
    >>> table = DBF('people.dbf')

This returns a ``DBF`` object. You can now iterate over records::

... code-block:: python

    >>> for record in table:
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

... code-block:: python

and count records::

... code-block:: python

    >>> len(table)
    2

Deleted records are available in ``deleted``:

... code-block:: python

    >>> for record in table.deleted:
    ...     print(record)
    {'NAME': 'Deleted Guy', 'BIRTHDATE': datetime.date(1979, 12, 22)}
    >>> len(table.deleted)
    1

You can also use the ``with`` statement::

    with DBF('people.dbf') as table:
        ...

The DBF object doesn't keep any files open, so this is provided merely
as a convenience.


Streaming or Loading Records
----------------------------

By default records are streamed directly off disk, which means only
one record is in memory at a time.

If have enough memory, you can load the records into a list by passing
``load=True''. This allows for random access:

... code-block:: python

    >>> table = DBF('people.dbf', load=True)
    >>> table.records[1]
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Deleted records are also loaded into a list in ``table.deleted``.

Alternatively, you can load the records later by calling
``table.load()``. This is useful when you want to look at the header
before you commit to loading anything. For example, you can make a
function which returns a list of tables in a directory and load only
the ones you need.

If you just want a list of records and you don't care about the other
table attributes you can do::

... code-block:: python

    >>> records = list(DBF('people.dbf'))

You can unload records again with ``table.unload()``.

If the table is not loaded, the ``records`` and ``deleted`` attributes
return ``RecordIterator`` objects.

Loading or iterating over records will open the DBF and memo file once
for each iteration. This means the ``DBF`` object doesn't hold any
files open, only the ``RecordIterator`` object does.


Ordered Records
---------------

By default dbread returns records as dictionaries, whose keys are not
ordered. This can create problems when generating output such as
CSV. You can get around this by passing ``ordered=True``. This will
return records as ordered dictionaries which means you can iterate
over the keys in the order they are found in the file.

Here's an example of a simple CSV exporter:

.. code-block:: python

    import csv
    import dbfread

    with dbfread.open('files/people.dbf',
                      ordered=True, lowernames=True) as people:
        writer = csv.writer(sys.stdout, delimiter=';',
                      quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(people.field_names)
        for record in people:
             writer.writerow(record.values())

(This example can be found in ``examples/ordered.py``.)


Character Encodings
-------------------


Memo Files
----------


Record Factories
----------------


Custom Field Types
------------------




