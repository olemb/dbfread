import datetime
from pytest import raises
from .field_parser import FieldParser

class MockDBF(object):
    encoding = 'ascii'

class MockField(object):
    def __init__(self, type='', **kwargs):
        self.type = type
        self.__dict__.update(kwargs)

def make_field_parser(field_type):
    parser = FieldParser(MockDBF())
    field = MockField(field_type)

    def parse(data):
        return parser.parse(field, data)

    return parse

def test_0():
    parse = make_field_parser('0')

    assert parse(b'\x01') == 1
    assert parse(b'\x00') == 0

def test_C():
    parse = make_field_parser('C')

    assert type(parse(b'test')) == type(u'')

def test_D():
    parse = make_field_parser('D')

    assert parse(b'00000000') is None
    assert parse(b'        ') is None

    epoch = datetime.date(1970, 1, 1)
    assert parse(b'19700101') == epoch

    with raises(ValueError):
        parse(b'NotIntgr')

def test_F():
    parse = make_field_parser('F')

    assert parse(b'') is None
    assert parse(b' ') is None

    assert parse(b'0') == 0
    assert parse(b'1') == 1
    assert parse(b'-1') == -1
    assert parse(b'3.14') == 3.14

    with raises(ValueError):
        parse(b'jsdf')

# This also tests parse2B() (+)
def test_I():
    parse = make_field_parser('I')

    # Little endian unsigned integer.
    assert parse(b'\x00\x00\x00\x00') == 0
    assert parse(b'\x01\x00\x00\x00') == 1
    assert parse(b'\xff\xff\xff\xff') == -1

def test_L():
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

# This also tests B, G and P.
def test_M():
    parse = make_field_parser('M')

    assert parse(b'\x01\x00\x00\x00') == 1
    assert parse(b'1') == 1
    assert parse(b'') is None
    with raises(ValueError):
        parse(b'NotInteger')

def test_N():
    parse = make_field_parser('N')

    assert parse(b'') is None
    assert parse(b' ') is None
    assert parse(b'1') == 1
    assert parse(b'-99') == -99
    assert parse(b'3.14') == 3.14

    with raises(ValueError):
        parse(b'okasd')

def test_O():
    """Test double field."""
    parse = make_field_parser('O')

    assert parse(b'\x00' * 8) == 0.0
    assert parse(b'\x00\x00\x00\x00\x00\x00\xf0?') == 1.0
    assert parse(b'\x00\x00\x00\x00\x00\x00Y\xc0') == -100

# This also tests parse40() (@)
def test_T():
    parse = make_field_parser('T')

    assert parse(b'') is None
    assert parse(b' ') is None

    # Todo: add more tests.

def test_hex_field():
    class PlusFieldParser(FieldParser):
        encoding = 'latin1'

        def parse3F(self, field, data):
            """Parser for '?' field."""
            return None

    parser = PlusFieldParser(MockDBF())
    field = MockField('?')

    parser.parse(field, b'test')
