.. highlight:: python

Moving data to SQL, CSV, Pandas etc.
====================================


CSV
---

This uses the standard library ``csv`` module:

.. literalinclude:: ../examples/print_csv.py

The output is::

    NAME,BIRTHDATE
    Alice,1987-03-01
    Bob,1980-11-12


Pandas Data Frames
------------------

.. literalinclude:: ../examples/pandas_dataframe.py

This will print::

        BIRTHDATE   NAME
    0  1987-03-01  Alice
    1  1980-11-12    Bob

The ``iter()`` is required. Without it Pandas will not realize that it
can iterate over the table.

Pandas will create a new list internally before converting the records
to data frames. This means they will all be loaded into memory. There
seems to be no way around this at the moment.


dataset (SQL)
-------------

The `dataset <https://dataset.readthedocs.io/>`_ package makes it easy
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
