.. highlight:: python

Exporting Data
==============

Here are some examples of how you can export data to other databases
or file formats.


CSV
---

This uses the standard library ``csv`` module:

.. literalinclude:: ../examples/print_csv.py

The output is::

    NAME,BIRTHDATE
    Alice,1987-03-01
    Bob,1980-11-12


dataset (SQL)
-------------

The `dataset <http://dataset.readthedocs.org/>`_ package makes it easy
to move data to a modern database. Here's how you can insert the
``people`` table into an SQLite database:

.. literalinclude:: ../examples/using_dataset.py

(This also creates the schema.)


dbf2sqlite
----------

You can use the included example program ``dbf2sqlite`` to insert
tables into an SQLite database::

    dbf2sqlite -o example.sqlite table1.dbf table2.dbf

This will create one table for each DBF file. You can also omit the
``-o example.sqlite`` option to have the SQL printed directly to
stdout.

If you get character encoding errors you can pass ``--encoding`` to
override the encoding, for example::

    dbf2sqlite --encoding=latin1 ...
