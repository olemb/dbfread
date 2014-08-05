Methods and Attributes
======================

Methods
-------

load()
   Load records into memory. This loads both records and deleted
   records. The ``records`` and ``deleted`` attributes will now be
   lists of records.

unload()
   Unload records from memory. The ``records`` and ``deleted``
   attributes will now be instances of ``RecordIterator``, which
   streams records from disk


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

      DBFHeader(dbversion=3, year=114, month=8, day=2, numrecords=3,
      headerlen=97, recordlen=25, reserved1=0, incomplete_transaction=0,
      encryption_flag=0, free_record_thread=0, reserved2=0, reserved3=0,
      mdx_flag=0, language_driver=0, reserved4=0)

fields
  A list of field headers from the file. Example of a field::

      DBFField(name=u'NAME', type=u'C', address=1, length=16, decimal_count=0,
      reserved1=0, workarea_id=0, reserved2=0, reserved3=0, set_fields_flag=0,
      reserved4='\x00\x00\x00\x00\x00\x00\x00', index_field_flag=0)
