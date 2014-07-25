0.2.0 - 
-------------------

* records can now be streamed from the file one, making it possible to
  read data files that are too large to fit in memory.

* default character encoding is not 'latin1'. This fixes the very common
  encoding error when ``language_driver`` is ``0``.

* now installs correctly with easy_install.

* added "--encoding" option to dbf2sqlite which can be used to
  override character encoding.


0.1.0 - 2014-04-08
-------------------

Initial release.
