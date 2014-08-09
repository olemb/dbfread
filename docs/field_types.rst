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
B   binary         binary data (stored in memo file)
C   text           unicode string
D   date           datetime.date or None
F   float          float
G   OLE            OLE object (stored in memo file)
I   integer        int
L   logical        True, False or None
M   memo           unicode string (memo), byte string (picture or object)
                   or None (stored in memo file)
N   numeric        int, float or None
O   double         float (floats are doubles in Python)
T   time           datetime.datetime
==  =============  ========================================================


Adding Custom Field Types
-------------------------

You can add new field types by subclassing
:py:class:`FieldParser`. For example:

.. literalinclude:: ../examples/custom_field_type.py


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


InvalidValue
------------

The field parser will normally raise ``ValueError`` when invalid
values are encountered. If instead you want them returned as raw data
you can do this:

.. literalinclude:: ../examples/print_invalid_values.py

``InvalidValue`` is a subclass of ``bytes``, and allows you to tell
invalid data apart from valid data that happens to be byte
strings. You can test for this with::

    isinstance(value, InvalidData)

You can also tell from the ``repr()`` string::

    >>> value
    InvalidData(b'not a number')
