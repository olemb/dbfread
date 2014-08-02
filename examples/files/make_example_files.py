"""
This creates the example file people.dbf.

You need the dbfpy library to run this.
"""
from dbfpy import dbf

db = dbf.Dbf('people.dbf', new=True)
db.addField(
    ('NAME', 'C', 16),
    ('BIRTHDATE', 'D'),
    )

for name, birthdate in (
    ('Alice', (1987, 3, 1)),
    ('Bob', (1980, 11, 12)),
    ('Deleted Guy', (1979, 12, 22)),
):
    rec = db.newRecord()
    rec['NAME'] = name
    rec['BIRTHDATE'] = birthdate
    rec.store()

# Delete the last one of those records.
rec.delete()
rec.store()

try:
    db.close()
except AttributeError:
    # This ignores the following error:
    #     self.memo.flush()
    # AttributeError: 'NoneType' object has no attribute 'flush'
    pass
