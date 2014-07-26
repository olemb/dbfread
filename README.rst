dbfread - Python library for reading data from DBF files
========================================================

Requires Python 3.2 or 2.7.

License: MIT

Latest version of the source code: http://github.com/olemb/dbfread/


Example
-------

::

    >>> import dbfread
    >>> for record in dbfread.open('people.dbf'):
    ...     print(record)
    ... 
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

If you have enough memory you can load the whole table into a list::

    >>> import dbfread
    >>> people = dbfread.read('people.dbf')
    >>> people[1]
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Both functions return a ``Table`` object. If records are loaded it
also behaves like a list of records. (It's a subclass of ``list``.)
See below for attributes and methods.

Using the `dataset <http://dataset.readthedocs.org/en/latest/>`_
package it's easy to move your data into a more modern database::

    import dataset
    import dbfread

    db = dataset.connect('sqlite:///:memory:')

    table = db['people']
    for record in dbfread.open('people.dbf', lowernames=True):
        table.insert(record)

    print(table.find_one(name='Alice'))

(Pass ``recfactory=collections.OrderedDict`` to ``open()`` if you want
to preserve field order.)


Installing
----------

::

  pip install dbfread

    

Status
------

The library has been used to read FoxPro files with a wide range of
data types, but is not widely tested with other DBF formats. It should
still work for most files.

Foxpro memo files (``.FPT``) are fully supported. The alternative
``.DBT`` memo files will be supported if I find any examples to test
with.

I intend for dbfread to be able to read any DBF file. If you have a
file it can't read, or you find a bug, I'd love to hear from you.


Supported Field Types
---------------------

=  ==========  ========================================================
:  Field type   Converted to
=  ==========  ========================================================
0  flags       int
C  text        unicode string
D  date        datetime.date or None
F  float       float or None
I  integer     int or None
L  logical     True, False or None
M  memo        unicode string (memo), byte string (picture or object)
               or None
N  numeric     int, float or None
T  time        datetime.datetime
=  ==========  ========================================================


Options for open() and read()
-----------------------------

load=True
  Load all records into memory. The ``Table`` object will behave as a
  list of records, and the ``deleted`` attribute will be a list of
  deleted records. This defaults to ``False`` for ``open()`` and
  ``True`` for ``read()``.

encoding='latin1'
  By default, dbfread will try to guess the character encoding from
  the language_driver byte. If this fails it uses "latin1". You can
  override this with the ``encoding`` argument.

lowernames=True
  Field names in DBF files are usually in
  uppercase. This converts them to lowercase.

recfactory=OrderedDict
  Takes any function that will be used to produce new records. The
  function should take a list of ``(name, value)`` tuples.

ignorecase=False
  The default is to ignore case in filenames.

parserclass=MyFieldParser
  You can add new field types by subclassing
  ``dbfread.field_parser.FieldParser``. See ``examples/parserclass.py``.

  (Please let me know if you have new field types that should be
  supported out of the box.)

raw=True
  Returns all data values as bytestrings. This can be used for
  debugging or for doing your own decoding.

All list methods are also available when records are loaded.


Table Attributes
----------------

deleted
  Deleted records. If records are in memory this is a list of records,
  if not it is a ``RecordIterator`` object. In any case you can
  iterate over it and call ``len()`` on it.

loaded
  ``True`` if records are loaded into memory.

name
  Name of the table. This is the lowercased stem of the filename, for
  example the file ``/home/me/SHOES.dbf`` will have the name
  ``shoes``.

date
  Date when the file was last written to (as ``datetime.datetime``).

field_names
  A list of field names in the order they appear in the file. This can
  for example be used to produce the header line in a CSV file.

encoding
  Character encoding used in the file. This is determined by the
  ``language_driver`` byte in the header, and can be overriden with the
  ``encoding`` keyword argument.

ignorecase, lowernames, recfactory, parserclass, raw
  These correspond to the keyword arguments below.

filename
  File name of the DBF file.

memofilename
  File name of the memo file, or ``None`` if there is no memo file.

header
  The file header. Example::

      DBFHeader(dbversion=48, year=12, month=7, day=11, numrecords=555,
      headerlen=2408, recordlen=632, reserved1=0, incomplete_transaction=0,
      encryption_flag=0, free_record_thread=0, reserved2=0, reserved3=0,
      mdx_flag=3, language_driver=3, reserved4=0)

fields
  A list of field headers from the file. Example::

      [DBFField(name=u'NAME', type=u'C', address=1, length=25, decimal_count=0,
      reserved1=0, workarea_id=0, reserved2=0, reserved3=0, set_fields_flag=0,
      reserved4='\x00\x00\x00\x00\x00\x00\x00', index_field_flag=0),
      ... etc. ...]


Methods
-------

load()
   Load records into memory.

unload()
   Unload records from memory.

__len__()
   Return number of records in the file. If records are not
   loaded this will scan the file to count records.

__iter__()
   Iterate through records.



dbf2sqlite
----------

(This does not require the `dataset
<http://dataset.readthedocs.org/en/latest/>`_ package.)

A tool is included in the ``examples`` directory to convert DBF into
sqlite, for example::

    dbf2sqlite -o example.sqlite table1.dbf table2.dbf

This will create one table for each DBF file. You can also omit the
``-o example.sqlite`` option to have the SQL printed directly to
stdout.

If you get character encoding errors you can pass ``--encoding`` to
override the encoding, for example::

   dbf2sqlite --encoding=latin1 ...


Contact
-------

Ole Martin Bjorndalen - ombdalen@gmail.com
