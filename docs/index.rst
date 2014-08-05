.. dbfread documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dbfread - Read DBF Files with Python
====================================
 
DBF is a file format used by databases such dBase, Visual FoxPro, and
FoxBase+. dbfread is designed to make it easy to get data out of these
files. It is designed for use in batch jobs and one-off scripts,
typically for moving data over to another format or for inspecting or
debugging data files.

If you need to write DBF files check out `dbfpy
<https://pypi.python.org/pypi/dbfpy/>`_


.. code-block:: python

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
    OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])

If you also need to write DBF files check out Ethan Furman's `dbf
<http://pypi.python.org/pypi/dbf/0.95.012>`_ package.


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
   api_changes
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
