"""
Tests reading from database.
"""
import datetime
from .dbf import DBF

table = DBF('testcases/memotest.dbf')

# This relies on people.dbf having this exact content.
records = [{u'NAME': u'Alice',
            u'BIRTHDATE': datetime.date(1987, 3, 1),
            u'MEMO': u'Alice memo'},
           {u'NAME': u'Bob',
            u'BIRTHDATE': datetime.date(1980, 11, 12),
            u'MEMO': u'Bob memo'}]
deleted_records = [{u'NAME': u'Deleted Guy',
                    u'BIRTHDATE': datetime.date(1979, 12, 22),
                    u'MEMO': u'Deleted Guy memo'}]

assert len(table) == 2
assert len(table.deleted) == 1
assert list(table) == records
assert list(table.deleted) == deleted_records

table.load()
loaded_table = table
assert len(loaded_table) == 2
assert len(loaded_table.deleted) == 1
assert list(loaded_table) == records
assert list(loaded_table.deleted) == deleted_records

# This should not return old style table which was a subclass of list.
assert not isinstance(table, list)
