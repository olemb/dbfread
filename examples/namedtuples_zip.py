"""
Return records as named tuples, reading directly from a .zip file.

This saves a lot of memory.
"""
from collections import namedtuple
from zipfile import ZipFile
from dbfread import StreamDBF

with ZipFile('files/people.zip') as zfile:
    with zfile.open('people.dbf', 'r') as infile:
        table = StreamDBF(infile, lowernames=True)

        # Set record factory. This must be done after
        # the table is opened because it needs the field
        # names.
        Record = namedtuple('Record', table.field_names)
        factory = lambda lst: Record(**dict(lst))
        table.recfactory = factory

        for record in table:
            print(record.name)
