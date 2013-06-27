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
    string = _str(string, encoding)
    
    string = string.rstrip('\x00')
    string = string.rstrip(' ')

    return string
