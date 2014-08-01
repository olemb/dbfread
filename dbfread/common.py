"""
Common things.
"""

try:
    # Python 2.x
    to_string = unicode
except NameError:
    # Pytyon 3.x
    to_string = str

def parse_string(string, encoding):
    """Convert a byte string to unicode

    Also strips trailing spaces and null bytes.
    """
    return to_string(string.rstrip(b'\0 '), encoding)
