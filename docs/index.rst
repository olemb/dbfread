.. dbfread documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dbfread - Read DBF Files with Python
====================================

Version |version|
 
DBF is a file format used by databases such dBase, Visual FoxPro, and
FoxBase+. This library reads DBF files and returns the data as native
Python data types for further processing. It is primarily intended for
batch jobs and one-off scripts.


.. code-block:: python

    >>> from dbfread import DBF
    >>> for record in DBF('people.dbf'):
    ...     print(record)
    OrderedDict([('NAME', 'Alice'), ('BIRTHDATE', datetime.date(1987, 3, 1))])
    OrderedDict([('NAME', 'Bob'), ('BIRTHDATE', datetime.date(1980, 11, 12))])


Source code
-----------

Latest stable release: https://github.com/olemb/dbfread/

Latest development version: https://github.com/olemb/dbfread/tree/develop/


About This Document
-------------------

This document is available at https://dbfread.readthedocs.io/

To build documentation locally::

    python setup.py docs                                                        

This requires Sphinx. The resulting files can be found in
``docs/_build/``.


Contents
------------

.. toctree::
   :maxdepth: 2

   changes
   installing
   introduction
   exporting_data
   dbf_objects
   field_types
   api_changes
   resources
   license
   acknowledgements

