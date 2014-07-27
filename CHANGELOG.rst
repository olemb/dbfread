1.0.4 - 2014-07-27
------------------

* bugfix: crashed when record list was not terminated with b'\x1a'.
  (Bug first apperad in 1.0.2 after a rewrite.)

* bugfix: memo fields with no value were returned as ''. They are
  now returned correctly as None.

* bugfix: field header terminaters were compared with strings.

* added example parserclass_debugstring.py.


1.0.3 - 2014-07-26
------------------

* reinstated hastily removed parserclass option.


1.0.2 - 2014-07-26
------------------

* added example record_objects.py.

* removed parserclass option to allow for internal changes.  There is
  currently no (documented) way to add custom field types.


1.0.1 - 2014-07-26
------------------

* bugfix: deleted records were ignored when using open().

* memo file is now opened and closed by each iterator instead of
  staying open all the time.


1.0.0 - 2014-07-25
------------------

* records can now be streamed from the file, making it possible to
  read data files that are too large to fit in memory.

* documentation is more readable and complete.

* now installs correctly with easy_install.

* added "--encoding" option to dbf2sqlite which can be used to
  override character encoding.


0.1.0 - 2014-04-08
------------------

Initial release.
