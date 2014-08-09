Field Types
===========

Supported Field Types
---------------------

==  =============  ========================================================
:   Field type     Converted to
==  =============  ========================================================
\+  autoincrement  int
@   time           datetime.datetime
0   flags          int
C   text           unicode string
D   date           datetime.date or None
F   float          float
I   integer        int
L   logical        True, False or None
M   memo           unicode string (memo), byte string (picture or object)
                   or None
N   numeric        int, float or None
O   double         float (floats are doubles in Python)
T   time           datetime.datetime
==  =============  ========================================================


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


Special Characters in Field Type Names
--------------------------------------

For a field type like '+' (autoincrement) the method would be named
``parse+()``.  Since this is not allowed in Python you can instead use
its ASCII value in hexadecimal. For example, the '+' parser is called
``parse3F()``.

You can name your method with::

    >>> 'parse' + format(ord('?'), 'x').upper()
    'parse3F'

Just replace ``'?'`` with your field type.
