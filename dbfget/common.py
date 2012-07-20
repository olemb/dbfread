"""
Common things.
"""

#
# 
#
try:
    # Python 2.x
    _str = unicode
except NameError:
    # Pytyon 3.x
    _str = str

def parse_string(data, encoding):
    # Convert to unicode
    data = _str(data, encoding)
    
    # Strip zero and space padding
    data = data.rstrip('\x00')
    data = data.rstrip(' ')

    return data
