Field Types
===========

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


Adding Custom Field Types
-------------------------

You can add new field types by subclassing
:py:class:`FieldParser`. For example, here's a how we handle stray
strings in our numeric (``N``) fields:

.. code-block:: python

    from dbfread import DBF, FieldParser

    class PortkartFieldParser(FieldParser):
        """Field parser that handles unusual things in the Telemator data."""
        def parseN(self, field, data):
            try:
                FieldParser.parseN(self, field, data)
            except ValueError:
                return dbfread.InvalidValue(data)

        ...

        table = DBF(filename,
                   load=True,
                   parserclass=PortkartFieldParser.

This will return return ``InvalidValue`` object that renders just like
strings, for example::

    InvalidValue(b'se scan')

See ``examples/`` for more examples.
