Keyword Arguments to open() / DBF()
===================================

load=False
  By default records and deleted records will be read off disk one by
  one.  If you pass ``True`` all records will be loaded into memory
  and the ``DBF`` object will behave like a list. Deleted records will
  be available as a list in the ``deleted`` attribute.
 
encoding=None
  Specify character encoding to use.

  By default dbfread will try to guess character encoding from the
  ``language_driver`` byte. If this fails it falls back on
  ``"ascii"``.

lowernames=False
  Field names are typically uppercase. If you pass ``True`` all field
  names will be converted to lowercase.

ordered=False
  Sometimes field order is important. If you pass ``ordered=True``,
  records will be returned as ordered dictionaries, which means you
  can loop over the fields in the order they appear in the file. This
  can be used when creating CSV files::

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

  The argument is overriden by ``recfactory``.

recfactory=None
  Takes a function that will be used to produce new records. The
  default is ``dict``. The function should take a list of ``(name,
  value)`` tuples. For example, this will return just the values as a
  list::

      def itemlist(items):
          return [value for (name, value) in items]

      dbfread.open('people.dbf', recfactory=itemlist)

  This overrides the ``ordered`` argument.

ignorecase=True
  Windows uses a case preserving file system which means
  ``people.dbf`` and ``PEOPLE.DBF`` are the same file. This causes
  problems in for example Linux where case is significant.  To get
  around this dbfread ignores case in file names. You can turn this
  off by passing ``ignorecase=False``.

parserclass=FieldParser
  The parser to use when parsing field values. You can use this to add
  new field types or do custom parsing by subclassing
  ``dbfread.FieldParser``. (See ``examples/parserclass.py``.)

ignore_missing_memofile=False
  If ``True`` and the memo file is not found all memo fields will be
  returned as ``None``.

raw=False
  Returns all data values as byte strings. This can be used for
  debugging or for doing your own decoding.
