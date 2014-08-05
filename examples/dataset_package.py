"""
Convert a DBF file to an SQLite table.

Requires dataset: http://dataset.readthedocs.org/en/latest/
"""

import dataset
from dbfread import DBF

db = dataset.connect('sqlite:///:memory:')

table = db['people']
for record in DBF('files/people.dbf', lowernames=True, ordered=True):
    table.insert(record)

print(table.find_one(name='Alice'))
