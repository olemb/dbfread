#!/usr/bin/env python2
"""
This creates the example file people.dbf.

You need the dbfpy library to run this.
"""
from __future__ import print_function
from dbfpy import dbf

def make_example_file(filename, fields, records, delete_last_record=False):
    field_names = [field[0] for field in fields]

    print('Creating', filename)
    print('  Fields:', ', '.join(field_names))
    print(' ', len(records), 'records')

    db = dbf.Dbf(filename, new=True)
    db.addField(*fields)

    for data in records:
        record = db.newRecord()
        for name, value in zip(field_names, data):
            record[name] = value
        record.store()

    if delete_last_record:
        # Delete the last one of those records.
        record.delete()
        record.store()

    try:
        db.close()
    except AttributeError:
        # This ignores the following error:
        #     self.memo.flush()
        # AttributeError: 'NoneType' object has no attribute 'flush'
        pass


make_example_file('people.dbf',
                  [('NAME', 'C', 16),
                   ('BIRTHDATE', 'D')],
                  [('Alice', (1987, 3, 1)),
                   ('Bob', (1980, 11, 12)),
                   ('Deleted Guy', (1979, 12, 22))],
                  delete_last_record=True)

make_example_file('../../testcases/memotest.dbf',
                  [('NAME', 'C', 16),
                   ('BIRTHDATE', 'D'),
                   ('MEMO', 'M')],
                  [('Alice', (1987, 3, 1), 'Alice memo'),
                   ('Bob', (1980, 11, 12), 'Bob memo'),
                   ('Deleted Guy', (1979, 12, 22), 'Deleted Guy memo')],
                  delete_last_record=True)
