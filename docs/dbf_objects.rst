DBF Objects
===========

Arguments
---------

filename
  The DBF file to open.
 
  The file name is case insensitive, which means ``DBF('PEOPLE.DBF')``
  will open the file ``people.dbf``. If there is a memo file, it too
  will be looked for in a case insensitive manner, so
  ``DBF('PEOPLE.DBF')`` would find the memo file ``people.FPT``.

  ``DBFNotFound`` will be raised if the file is not found, and
  ``MissingMemoFile`` if the memo file is missing.

load=False
  By default records will streamed directly from disk. If you pass
  ``load=True`` they will instead be loaded into lists and made
  available as the ``records`` and ``deleted`` attributes.

  You can load and unload records at any time with the ``load()`` and
  ``unload()`` methods.
 
encoding=None
  Specify character encoding to use.

  By default dbfread will try to guess character encoding from the
  ``language_driver`` byte. If this fails it falls back on
  ASCII.

lowernames=False
  Field names are typically uppercase. If you pass ``True`` all field
  names will be converted to lowercase.

recfactory=collections.OrderedDict

  Takes a function that will be used to produce new records. The
  function will be called with a list of ``(name, value)`` pairs.

  If you pass ``recfactory=None`` you will get the original ``(name,
  value)`` list.

ignorecase=True
  Windows uses a case preserving file system which means
  ``people.dbf`` and ``PEOPLE.DBF`` are the same file. This causes
  problems in for example Linux where case is significant.  To get
  around this dbfread ignores case in file names. You can turn this
  off by passing ``ignorecase=False``.

parserclass=FieldParser
  The parser to use when parsing field values. You can use this to add
  new field types or do custom parsing by subclassing
  ``dbfread.FieldParser``. (See :doc:`field_types`.)

ignore_missing_memofile=False
  If you don't have the memo field you can pass
  ``ignore_missing_memofile=True``. All memo fields will then be
  returned as ``None``, so you at least get the rest of the data.

raw=False
  Returns all data values as byte strings. This can be used for
  debugging or for doing your own decoding.


Methods
-------

load()
   Load records into memory. This loads both records and deleted
   records. The ``records`` and ``deleted`` attributes will now be
   lists of records.

unload()
   Unload records from memory. The ``records`` and ``deleted``
   attributes will now be instances of ``RecordIterator``, which
   streams records from disk.


Attributes
----------

records
  If the table is loaded this is a list of records. If not, it's a
  ``RecordIterator`` object. In either case, iterating over it or
  calling ``len()`` on it will give the same results.

deleted
  If the table is loaded this is a list of deleted records. If not,
  it's a ``RecordIterator`` object. In either case, iterating over it
  or calling ``len()`` on it will give the same results.

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
  Date when the file was last updated (as ``datetime.date``) or
  ``None`` if the date was all zeroes or invalid.

field_names
  A list of field names in the order they appear in the file. This can
  for example be used to produce the header line in a CSV file.

encoding
  Character encoding used in the file. This is determined by the
  ``language_driver`` byte in the header, and can be overriden with the
  ``encoding`` keyword argument.

ignorecase, lowernames, recfactory, parserclass, raw
  These are set to the values of the same keyword arguments.

filename
  File name of the DBF file.

memofilename
  File name of the memo file, or ``None`` if there is no memo file.

header
  The file header. This is only intended for internal use, but is exposed
  for debugging purposes. Example::

      DBFHeader(dbversion=3, year=114, month=8, day=2, numrecords=3,
      headerlen=97, recordlen=25, reserved1=0, incomplete_transaction=0,
      encryption_flag=0, free_record_thread=0, reserved2=0, reserved3=0,
      mdx_flag=0, language_driver=0, reserved4=0)

fields
  A list of field headers from the file. Example of a field::

      DBFField(name='NAME', type='C', address=1, length=16, decimal_count=0,
      reserved1=0, workarea_id=0, reserved2=0, reserved3=0, set_fields_flag=0,
      reserved4=b'\x00\x00\x00\x00\x00\x00\x00', index_field_flag=0)

  Only the ``name``, ``type`` and ``length`` attributes are used.
