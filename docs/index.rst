.. dbfread documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dbfread - Read DBF files with Python
====================================

DBF is a file format used by databases such as dBase, Visual FoxPro,
FoxBase+ and Clipper.

The goal of dbfread is to read any DBF file and return its data as
native Python data types.

If you need to write DBF files, check out Ethan Furman's `dbf
<https://pypi.python.org/pypi/dbf/0.95.012>`_ package.

.. code-block:: python

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    {'NAME': 'Alice', 'BIRTHDATE': datetime.date(1987, 3, 1)} 
    {'NAME': 'Bob', 'BIRTHDATE': datetime.date(1980, 11, 12)}

If you also need to write DBF files check out Ethan Furman's `dbf
<https://pypi.python.org/pypi/dbf/0.95.012>`_ package.


Source code
-----------

Latest stable release: http://github.com/olemb/dbfread/

Latest development version: http://github.com/olemb/dbfread/tree/develop/


About This Document
-------------------

This document is available at http://dbfread.readthedocs.org/

To build documentation locally::

    python setup.py docs                                                        

This requires Sphinx. The resulting files can be found in
``docs/_build/``.


Contents
------------

.. toctree::
   :maxdepth: 2

   installing
   introduction
   keyword_arguments
   methods_and_attributes
   field_types
   development_notes
   resources
   license
   authors
   acknowledgements


Indices and tables
==================

* :ref:`genindex`

* :ref:`modindex`

* :ref:`search`
