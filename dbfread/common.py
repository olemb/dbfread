"""
Common things.
"""
import sys

py2 = sys.version_info[0] == 2

if py2:
    to_string = unicode
    _bytestring = str
else:
    to_string = str
    _bytestring = bytes

def parse_string(string, encoding):
    """Convert a byte string to unicode

    Also strips trailing spaces and null bytes.
    """
    return to_string(string.rstrip(b'\0 '), encoding)
