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

All text fields and memos (except binary ones) will be returned as
unicode strings.

dbfread will try to detect the character encoding (code page) used in
the file by looking at the ``language_driver`` byte. If this fails it
reverts to ASCII.

You can override this by passing ``encoding='my-encoding'``.

The encoding is available in the ``encoding`` attribute.


Memo Files
----------

If there is at least one memo field in the file dbfread will look for
the corresponding memo file. If ``people.dbf`` had a memo field, the
memo file would be ``people.fpt``. (This is the extension used by
Visual FoxPro. More extensions, like ``.dbt``, will be added as they
are implemented.)

Since the Windows file system is case preserving, the file names may
end up mixed case. For example, in our database we have this::

    Endreg.dbf ENDREG.fpt

This creates problems in Linux, where file names are case
sensitive. dbfread gets around this by ignoring case in file
names. You can turn this off by passing ``ignorecase=False``.

If the memo file is missing you will get a ``MissingMemoFile``
exception. You can still get the rest of the data out by passing
``ignore_missing_memofile=True``. All memo field values will now be
returned as ``None``, as would be the case if there was no memo.


Record Factories
----------------

If you don't want records returned as dictionaries or ordered
dictionaries you can make your own record types with the
``recfactory`` argument.

A record factory is a function that takes a list of ``(name, value)``
pairs and returns a record. The first record in ``people.dbf`` will be
passed to the factory as:

... code-block:: python

    [('NAME', 'Alice'), ('BIRTHDATE': datetime.date(1987, 3, 1)]

You can do whatever you like with this data. Here's a very naive
implementation of CSV:

... code-block:: python

    from dbfread import DBF
    
    def get_values(items):
       return [str(value) for (name, value) in items]
    
    table = DBF('people.dbf', recfactory=get_values)
    print(';'.join(table.field_names))
    for record in table:
        print(';'.join(record))

(You will find this in ``examples/csv_export.py``.)

This is just an example. It doesn't escape values in the data, so you
should use the standard library module ``csv`` instead.


Custom Field Types
------------------




