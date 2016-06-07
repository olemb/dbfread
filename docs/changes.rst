Changes
=======

Release History
---------------

2.0.6 - 2016-06-07
^^^^^^^^^^^^^^^^^^

* Added support for long character (C) fields (up to 65535 bytes).
  (Requested by Eric Mertens and Marcelo Manzano.)

* Added support for Visual FoxPro varchar fields (V). (Thanks to Roman
  Kharin for reporting and bobintetley for providing a solution.)

* Bugfix (dbf2sqlite): some table or field names might actually collide with
  sql reserved words. (Fix by vthriller, pull request #15.)

* Documented how to convert records to Pandas data frames. (Thanks to
  Roman Yurchak for suggesting this.)


2.0.5 - 2015-11-30
^^^^^^^^^^^^^^^^^^

* Bugfix: memo field parser used str instead of bytes. (Fix submitted
  independently by Sebastian Setzer (via email) and by Artem Vlasov,
  pull request #11.)

* Bugfix: some field parsers called self._get_memo() instead of
  self.get_memo(). (Fix by Yu Feng, pull request #9.)


2.0.4 - 2015-02-07
^^^^^^^^^^^^^^^^^^

* DBF header and field headers are no longer read-only. For example
  you can now change field names by doing ``table.fields[0].name = 'price'``
  or read from files where field sizes in the header don't match those
  in the actual records by doing ``table.fields[0].length = 500``.

* fixed some examples that didn't work with Python 3.


2.0.3 - 2014-09-30
^^^^^^^^^^^^^^^^^^

* added currency field (Y). (Patch by Stack-of-Pancakes.)


2.0.2 - 2014-09-29
^^^^^^^^^^^^^^^^^^

* bugfix: a date with all zeroes in the DBF header resulted in
  'ValueError: month must be in 1..12'.  (Reported by Andrew Myers.)
  The ``date`` attribute is now set to ``None`` for any value that is
  not a valid date.


2.0.1 - 2014-09-19
^^^^^^^^^^^^^^^^^^

* bugfix: didn't handle field names with garbage after b'\0'
  terminator. (Patch by Cédric Krier.)

* now handles 0 (_NullFlags) fields that are more than 1 byte long.
  0 fields are now returned as byte strings instead of integers.
  (Reported by Carlos Huga.)

* the type B field is a double precision floating point numbers in
  Visual FoxPro. The parser crashed when it tried to interpret this as
  a string containing a number. (Reported by Carlos Huga.)

* API changes: memo field parsers now return the memo data (typically
  a unicode string or bytes object) instead of returning the
  index. This makes it easier to implement new memo types or extend
  the existing ones since memo fields are no longer a special case.


2.0.0 - 2014-08-12
^^^^^^^^^^^^^^^^^^

* ``dbfread.open()`` and ``dbfread.read()`` are now deprecated and
  will be removed in 1.4. Since the ``DBF`` object is no longer a
  subclass of list, these functions instead return backward compatible
  ``DeprecatedDBF`` objects.

* records are now returned as ordered dictionaries. This makes it
  easier to iterate over fields in the same order that they appear in
  the file.

* now reads (at least some) DBT files.

* added support for 6 new field types.

* added ``ignore_missing_memofile`` argument. If ``True`` and the memo
  file is not found all memo fields will be returned as ``None``.

* DBF now raises ``DBFNotFound`` and ``MissingMemoFile``. These
  inherit from IOError, so old code should still work.

* added ``InvalidValue``. This is currently not used by the library but
  can be useful for custom parsing.

* ``FieldParser`` is now available in the top scope.

* wrote documentation.

* switched to pytest for unit tests.


1.1.1 - 2014-08-03
^^^^^^^^^^^^^^^^^^

* example and test data files were missing from the manifest.


1.1.0 - 2014-08-03
^^^^^^^^^^^^^^^^^^

* the ``DBF`` object is no longer a subclass of list. Records are
  instead available in the ``records`` attribute, but the table can be
  iterated over like before. This change was made to make the API
  cleaner and easier to understand. ``read()`` is still included for
  backwards compatability, and returns an ``OldStyleTable`` object
  with the old behaviour.

* default character encoding is now ``"ascii"``. This is a saner default
  than the previously used ``"latin1"``, which would decode but could give
  the wrong characters.

* the DBF object can now be used as a context manager (using the
  "with" statement).


1.0.6 - 2014-08-02
^^^^^^^^^^^^^^^^^^

* critical bugfix: each record contained only the last
  field. (Introduced in 1.0.5, making that version unusable.)

* improved performance of record reading a bit.


1.0.5 - 2014-08-01
^^^^^^^^^^^^^^^^^^

This version is broken.

* more than doubled performance of record parsing.

* removed circular dependency between table and deleted record iterator.

* added ``dbversion`` attribute.

* added example ``dbfinfo.py``.

* numeric field (N) parser now handles invalid data correctly.

* added more unit tests.


1.0.4 - 2014-07-27
^^^^^^^^^^^^^^^^^^

* bugfix: crashed when record list was not terminated with b'\x1a'.
  (Bug first apperad in 1.0.2 after a rewrite.)

* bugfix: memo fields with no value were returned as ''. They are
  now returned correctly as None.

* bugfix: field header terminaters were compared with strings.

* added example parserclass_debugstring.py.


1.0.3 - 2014-07-26
^^^^^^^^^^^^^^^^^^

* reinstated hastily removed parserclass option.


1.0.2 - 2014-07-26
^^^^^^^^^^^^^^^^^^

* added example record_objects.py.

* removed parserclass option to allow for internal changes.  There is
  currently no (documented) way to add custom field types.


1.0.1 - 2014-07-26
^^^^^^^^^^^^^^^^^^

* bugfix: deleted records were ignored when using open().

* memo file is now opened and closed by each iterator instead of
  staying open all the time.


1.0.0 - 2014-07-25
^^^^^^^^^^^^^^^^^^

* records can now be streamed from the file, making it possible to
  read data files that are too large to fit in memory.

* documentation is more readable and complete.

* now installs correctly with easy_install.

* added "--encoding" option to dbf2sqlite which can be used to
  override character encoding.


0.1.0 - 2014-04-08
^^^^^^^^^^^^^^^^^^

Initial release.
