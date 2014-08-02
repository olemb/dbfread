from __future__ import print_function
import sys
import random
from unittest import TestCase, main
from contextlib import contextmanager
import datetime

import dbfread
from dbfread.field_parser import FieldParser

# http://docs.python.org/2/library/unittest.html                                

PY2 = (sys.version_info.major == 2)

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO

@contextmanager
def raises(exception):
    try:
        yield
        raise AssertionError('code should have raised exception')
    except exception:
        pass

class MockField(object):
    def __init__(self, type='', **kwargs):
        self.type = type
        self.__dict__.update(kwargs)

def make_field_parser(field_type):
    parser = FieldParser('latin1')
    field = MockField(field_type)

    def parse(data):
        return parser.parse(field, data)

    return parse

class TestReadAndLength(TestCase):
    def test_all(self):
        table = dbfread.open('testcases/memotest.dbf')

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

class TestFieldParsers(TestCase):
    def test_0(self):
        parse = make_field_parser('0')
        
        assert parse(b'\x01') == 1
        assert parse(b'\x00') == 0

    def test_C(self):
        parse = make_field_parser('C')
        
        assert type(parse(b'test')) == type(u'')

    def test_D(self):
        parse = make_field_parser('D')

        assert parse(b'00000000') is None
        assert parse(b'        ') is None

        epoch = datetime.date(1970, 1, 1)
        assert parse(b'19700101') == epoch

        with raises(ValueError):
            parse(b'NotIntgr')

    def test_F(self):
        parse = make_field_parser('F')

        assert parse(b'') is None
        assert parse(b' ') is None
        
        assert parse(b'0') == 0
        assert parse(b'1') == 1
        assert parse(b'-1') == -1
        assert parse(b'3.14') == 3.14

        with raises(ValueError):
            parse(b'jsdf')

    def test_I(self):
        parse = make_field_parser('I')

        # Little endian unsigned integer.
        assert parse(b'\x00\x00\x00\x00') == 0
        assert parse(b'\x01\x00\x00\x00') == 1
        assert parse(b'\xff\xff\xff\xff') == -1

    def test_L(self):
        parse = make_field_parser('L')

        for char in b'TtYy':
            assert parse(char) is True

        for char in b'FfNn':
            assert parse(char) is False

        for char in b'? ':
            assert parse(char) is None

        # Some invalid values.
        for char in b'!0':
            with raises(ValueError):
                parse(char)

    def test_M(self):
        parse = make_field_parser('M')

        assert parse(b'\x01\x00\x00\x00') == 1
        assert parse(b'1') == 1
        assert parse(b'') is None
        with raises(ValueError):
            parse(b'NotInteger')

    def test_N(self):
        parse = make_field_parser('N')

        assert parse(b'') is None
        assert parse(b' ') is None
        assert parse(b'1') == 1
        assert parse(b'-99') == -99
        assert parse(b'3.14') == 3.14
        with raises(ValueError):
            parse(b'okasd')

    def test_T(self):
        parse = make_field_parser('T')

        assert parse(b'') is None
        assert parse(b' ') is None

        # Todo: add more tests.

if __name__ == '__main__':
    main()
