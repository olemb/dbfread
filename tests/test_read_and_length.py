"""
Tests reading from database.
"""
import datetime

from dbfread import dbf
from pytest import fixture

from dbfread.dbf import DBF

@fixture
def table():
    return DBF('tests/cases/memotest.dbf')

@fixture
def loaded_table():
    return DBF('tests/cases/memotest.dbf', load=True)

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

def test_len(table, loaded_table):
    assert len(table) == 2
    assert len(table.deleted) == 1

    assert len(loaded_table) == 2
    assert len(loaded_table.deleted) == 1


def test_list(table, loaded_table):
    assert list(table) == records
    assert list(table.deleted) == deleted_records

    assert list(loaded_table) == records
    assert list(loaded_table.deleted) == deleted_records

    # This should not return old style table which was a subclass of list.
    assert not isinstance(table, list)
