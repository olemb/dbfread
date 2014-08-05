"""
Return records as objects with fields as attributes.
"""
from __future__ import print_function
from dbfread import DBF

class Record(object):
    def __init__(self, items):
        for name, value in items:
            setattr(self, name, value)

for record in DBF('files/people.dbf', recfactory=Record, lowernames=True):
    print(record.name, 'was born on', record.birthdate)
