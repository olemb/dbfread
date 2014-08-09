.. highlight:: python

Exporting Data
==============

Here are some examples of how you can export data to other databases
or file formats.


CSV
---

::

    import sys
    import csv
    from dbfread import DBF

    table = DBF('files/people.dbf')
    writer = csv.writer(sys.stdout)

    writer.writerow(table.field_names)
    for record in table:
        writer.writerow(record.values())


dataset (SQL)
-------------

The `dataset <http://dataset.readthedocs.org/>`_ package makes it easy
to move data to a modern database. Here's how you can insert the
``people`` table into an SQLite database::

    import dataset
    from dbfread import DBF

    # Change to "dataset.connect('people.sqlite')" if you want a file.
    db = dataset.connect('sqlite:///:memory:')
    table = db['people']

    for record in DBF('files/people.dbf', lowernames=True):
        table.insert(record)

    # Select and print a record just to show that it worked.
    print(table.find_one(name='Alice'))

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
