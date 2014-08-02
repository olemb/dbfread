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

    def read(self, file):
        """Read struct from a file-like object (implenting read())."""
        return self.unpack(file.read(self.struct.size))
