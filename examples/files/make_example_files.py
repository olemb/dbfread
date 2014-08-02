"""
This creates the example file people.dbf.

You need the dbfpy library to run this.
"""
from dbfpy import dbf

def make_example_file(filename, fields, records, delete_last_record=False):
    db = dbf.Dbf(filename, new=True)
    db.addField(*fields)

    for data in records:
        record = db.newRecord()
        for name, value in zip([field[0] for field in fields], data):
            print(name, value)
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
