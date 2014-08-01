dbfread - Python library for reading data from DBF files
========================================================

DBF is a file format used by databases such dBase, Visual FoxPro,
FoxBase+ and Clipper. dbfread is designed to make it easy to get data
out of these files.

If you also need to write and create DBF files check out `dbfpy
<https://pypi.python.org/pypi/dbfpy/>`_


Example
-------

::

    >>> import dbfread
    >>> for record in dbfread.open('people.dbf'):
    ...     print(record)
    ... 
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)}
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Records are read off disk one by one. If you have enough memory you
can load them all at once. The table will then behave like a list::

    >>> table = dbfread.read('people.dbf')
    >>> table[1]
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

Both functions return a ``Table`` object. See below for attributes and
methods.

Using `dataset <http://dataset.readthedocs.org/en/latest/>`_ it's easy
to move your data into a more modern database. See
``examples/using_dataset.py``. Alternatively you can use the included
``examples/dbf2sqlite``.


Status
------

The library has been used to read Visual FoxPro files with a wide
range of data types, but is not widely tested with other DBF
formats. It should still work for most files.

``.FPT`` memo files are fully supported. The alternative ``.DBT`` memo
files will be supported if I find any examples to test with.

I intend for dbfread to be able to read any DBF file. If you have a
file it can't read, or you find a bug, I'd love to hear from you.


Requirements and Installing
---------------------------

dbfread is a pure Python module written for Python 3.2 and 2.7.

::

  pip install dbfread
    

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

load=False
  By default records and deleted records will be read off disk one by
  one.  If you pass ``True`` all records will be loaded into memory
  and the ``Table`` object will behave like a list. Deleted records
  will be available as a list in the ``deleted`` attribute.

  This defaults to ``True`` for ``read()``.
 
encoding=None
  By default dbfread will try to guess the character encoding from
  the language_driver byte. If this fails it uses "latin1". You can
  override this with the ``encoding`` argument.

lowernames=False
  Field names are typically uppercase. If you pass ``True`` all field
  names will be converted to lowercase.

recfactory=dict
  Takes a function that will be used to produce new records. The
  function should take a list of ``(name, value)`` tuples. For example
  if you want to preserve the order of fields you can pass
  ``recfactory=collections.OrderedDict``.

ignorecase=True
  Windows uses a case preserving file system which means
  ``people.dbf`` and ``PEOPLE.DBF`` are the same file. This causes
  problems in for example Linux where case is significant.  To get
  around this dbfread ignores case in file names. You can turn this
  off by passing ``ignorecase=False``.

parserclass=FieldParser
  The parser to use when parsing field values. You can use this to add
  new field types or do custom parsing by subclassing
  ``dbfread.field_parser.FieldParser``. (See
  ``examples/parserclass.py`` and ``examples/parserclass_debugstring.py``.

raw=False
  Returns all data values as byte strings. This can be used for
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

dbversion
  The name of the program that created the database (based on the
  ``dbversion`` byte in the header). Example: ``"FoxBASE+/Dbase III
  plus, no memory"``.

name
  Name of the table. This is the lowercased stem of the filename, for
  example the file ``/home/me/SHOES.dbf`` will have the name
  ``shoes``.

date
  Date when the file was last updated (as ``datetime.date``).

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


Caveats
-------

* some files with ``header.dbversion == 0`` do not in fact contain
  7-bit ASCII encoded strings, resulting in a decoding error.

* there is currently no way to ignore missing memo files.


License
-------

dbfread is released under the terms of the `MIT license
<http://en.wikipedia.org/wiki/MIT_License>`_.


Source code
------------

Latest stable release: http://github.com/olemb/dbfread/

Development version: http://github.com/olemb/dbfread/tree/develop/


Contact
-------

Ole Martin Bjorndalen - ombdalen@gmail.com
