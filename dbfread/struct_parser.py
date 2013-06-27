"""
Parser that converts (C style) binary structs named tuples.

The struct can be read from a file or a byte string.
"""

import struct
import collections


class StructParser:
    def __init__(self, name, format, names):
        self.format = format
        self.names = names
        self.struct = struct.Struct(format)
        self.tuple = collections.namedtuple(name, names)

    def unpack(self, data):
        """Unpack struct from binary string and return a named tuple."""
        items = zip(self.names, self.struct.unpack(data))
        t = self.tuple(**dict(items))
        return t

    def read(self, file, prepend=b''):
        """Read binary string from a file-like object (implenting read()
        and return data as a named tuple.
        The prepend option can be used to read byte or two from the file
        to decide whether to call read(). It will be prepended to the
        data before it is parsed.
        """
        data = prepend + file.read(self.struct.size - len(prepend))
        return self.unpack(data)

