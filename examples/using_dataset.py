"""
Convert a DBF file to an SQLite table.

Requires dataset: http://dataset.readthedocs.org/en/latest/

Pass 'recfactory=collections.OrderedDict' to open() if you want to
preserve field order.
"""

import collections
import dataset
import dbfread

db = dataset.connect('sqlite:///:memory:')

table = db['people']
for record in dbfread.open('files/people.dbf', lowernames=True,
                           recfactory=collections.OrderedDict):
    table.insert(record)

print(table.find_one(name='Alice'))
