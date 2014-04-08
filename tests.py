from __future__ import print_function
import sys
import random
from unittest import TestCase, main
from contextlib import contextmanager
import datetime
import dbfread

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

class TestFieldParsers(TestCase):
    def test_M(self):
        from dbfread.field_parser import FieldParser
        parser = FieldParser('latin1')

        def parse(data):
            return parser.parseM(MockField(), data)

        assert parse(b'\x01\x00\x00\x00') == 1
        assert parse(b'1') == 1
        assert parse(b'') is None
        with raises(ValueError):
            parse(b'NotInteger')

    def test_D(self):
        from dbfread.field_parser import FieldParser
        parser = FieldParser('latin1')

        def parse(data):
            return parser.parseD(MockField(), data)

        assert parse(b'00000000') is None
        assert parse(b'        ') is None

        epoch = datetime.date(1970, 1, 1)
        assert parse(b'19700101') == epoch
        with raises(ValueError):
            parse(b'NotIntgr')

if __name__ == '__main__':
    main()
