"""
Common things.
"""

try:
    # Python 2.x
    _str = unicode
except NameError:
    # Pytyon 3.x
    _str = str


def parse_string(string, encoding):
    """Convert a byte string to unicode

    Also strips trailing spaces and null bytes.
    """
    return _str(string, encoding).rstrip('\x00').rstrip(' ')
