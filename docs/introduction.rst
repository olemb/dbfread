.. highlight:: python

Introduction
============

This is a short introduction to the API. If you want to follow along
you can find ``people.dbf`` in ``examples/files/``.


Opening a DBF File
------------------

::

    >>> from dbfread import DBF
    >>> table = DBF('people.dbf')

This returns a ``DBF`` object. You can now iterate over records::

    >>> for record in table:
    ...     print(record)
    OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
    OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])

and count records::

    >>> len(table)
    2

Deleted records are available in ``deleted``::

    >>> for record in table.deleted:
    ...     print(record)
    OrderedDict([('NAME', 'Deleted Guy'), ('BIRTHDATE', datetime.date(1979, 12, 22))])

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
``load=True``. This allows for random access::

    >>> table = DBF('people.dbf', load=True)
    >>> print(table.records[1]['NAME'])
    Bob
    >>> print(table.records[0]['NAME'])
    Alice

Deleted records are also loaded into a list in ``table.deleted``.

Alternatively, you can load the records later by calling
``table.load()``. This is useful when you want to look at the header
before you commit to loading anything. For example, you can make a
function which returns a list of tables in a directory and load only
the ones you need.

If you just want a list of records and you don't care about the other
table attributes you can do::

    >>> records = list(DBF('people.dbf'))

You can unload records again with ``table.unload()``.

If the table is not loaded, the ``records`` and ``deleted`` attributes
return ``RecordIterator`` objects.

Loading or iterating over records will open the DBF and memo file once
for each iteration. This means the ``DBF`` object doesn't hold any
files open, only the ``RecordIterator`` object does.


Character Encodings
-------------------

All text fields and memos (except binary ones) will be returned as
unicode strings.

dbfread will try to detect the character encoding (code page) used in
the file by looking at the ``language_driver`` byte. If this fails it
reverts to ASCII. You can override this by passing
``encoding='my-encoding'``. The encoding is available in the
``encoding`` attribute.


Memo Files
----------

If there is at least one memo field in the file dbfread will look for
the corresponding memo file. For ``buildings.dbf`` this would be
``buildings.fpt`` (for Visual FoxPro) or ``buildings.dbt`` (for other
databases).

Since the Windows file system is case preserving, the file names may
end up mixed case. For example, you could have::

    Buildings.dbf BUILDINGS.DBT

This creates problems in Linux, where file names are case
sensitive. dbfread gets around this by ignoring case in file
names. You can turn this off by passing ``ignorecase=False``.

If the memo file is missing you will get a ``MissingMemoFile``
exception. If you still want the rest of the data you can pass
``ignore_missing_memofile=True``. All memo field values will now be
returned as ``None``, as would be the case if there was no memo.

dbfread has full support for Visual FoxPro (``.FPT``) and dBase III
(``.DBT``) memo files. It reads dBase IV (also ``.DBT``) memo files,
but only if they use the default block size of 512 bytes. (This will
be fixed if I can find more files to study.)


Record Factories
----------------

If you don't want records returned as ``collections.OrderedDict`` you
can use the ``recfactory`` argument to provide your own record
factory.

A record factory is a function that takes a list of ``(name, value)``
pairs and returns a record.  You can do whatever you like with this
data. Here's a function that creates a record object with fields as
attributes::

    class Record(object):
        def __init__(self, items):
            for (name, value) in items:
                setattr(self, name, value)

    for record in DBF('people.dbf', recfactory=Record, lowernames=True):
        print(record.name, record.birthdate)

If you pass ``recfactory=None`` you will get the original ``(name,
value)`` list. (This is a shortcut for ``recfactory=lambda items:
items``.)


Custom Field Types
------------------

If the included message types are not enough you can add your own by
subclassing ``FieldParser``. As a silly example, here how you can read
text (``C``) fields in reverse::

    from dbfread import DBF, FieldParser

    class MyFieldParser(FieldParser):
        def parseC(self, field, data):
            # Return strings reversed.
            return data.rstrip(' 0').decode()[::-1]

    for record in DBF('files/people.dbf', parserclass=MyFieldParser):
        print(record['NAME'])

and here's how you can return invalid values as ``InvalidValue``
instead of raising ``ValueError``::

    from dbfread import DBF, FieldParser, InvalidValue

    class MyFieldParser(FieldParser):
        def parse(self, field, data):
            try:
                return FieldParser.parse(self, field, data)
            except ValueError:
                return InvalidValue(data)

    table = DBF('invalid_value.dbf', parserclass=MyFieldParser):
    for i, record in enumerate(table):
        for name, value in record.items():
            if isinstance(value, InvalidValue):
                print('records[{}][{!r}] == {!r}'.format(i, name, value))

This will print::

    records[0][u'BIRTHDATE'] == InvalidValue(b'NotAYear')
