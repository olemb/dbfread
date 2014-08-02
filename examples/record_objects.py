"""
Return records as objects with fields as attributes.
"""
import dbfread

class Record(object):
    def __init__(self, items):
        for name, value in items:
            setattr(self, name, value)

for record in dbfread.open('files/people.dbf',
                           recfactory=Record, lowernames=True):
    print(record.name)
