from dbfread.codepages import *
from pytest import *


def test_guess_encoding():

    assert guess_encoding(0x00) == 'ascii'
    with raises(LookupError):
        guess_encoding(0x200)

if __name__ == '__main__':
    pytest.main ()
