"""
Parser for DBF fields.
"""
import datetime
import struct

from .common import to_string, parse_string


class FieldParser:
    def __init__(self, encoding):
        """Create a new field parser

        encoding is the character encoding to use when parsing
        strings."""
        self.encoding = encoding
        self._lookup = self._create_lookup_table()

    def _create_lookup_table(self):
        """Create a lookup table for field types."""
        lookup = {}

        for name in dir(self):
            if name.startswith('parse'):
                field_type = name[5:]
                if field_type:
                    lookup[field_type] = getattr(self, name)

        return lookup

    def str(self, data):
        """Convert binary data to string and strip padding."""
        return parse_string(data, self.encoding)
    
    def field_type_supported(self, field_type):
        """Checks if the field_type is supported by the parser

        field_type should be a one-character string like 'C' and 'N'.
        Returns a boolen which is True if the field type is supported.
        """
        return field_type in self._lookup

    def parse(self, field, data):
        """Parse field and return value"""
        try:
            func = self._lookup[field.type]
        except KeyError:
            raise ValueError('Unknown field type: {!r}'.format(field.type))
        else:
            return func(field, data)

    def parse0(self, field, data):
        """Parse flags field and return int"""
        return ord(data)

    def parseC(self, field, data):
        """Parse char field and return unicode string"""
        return to_string(data.rstrip(b'\0 '), self.encoding)

    def parseD(self, field, data):
        """Parse date field and return datetime.date or None"""
        try:
            return datetime.date(int(data[:4]), int(data[4:6]), int(data[6:8]))
        except ValueError:
            if data.strip(b' 0') == b'':
                # A record containing only spaces and/or zeros is
                # a NULL value.
                return None
            else:
                raise ValueError('invalid date {!r}'.format(data))
    
    def parseF(self, field, data):
        """Parse float field and return float or None"""
        if data.strip():
            return float(data)
        else:
            return None

    def parseI(self, field, data):
        """Parse Integer field and return float or None"""
        # Todo: is this 4 bytes on every platform?
        return struct.unpack('<i', data)[0]

    def parseL(self, field, data):
        """Parse logical field and return True, False or None"""
        if data in b'TtYy':
            return True
        elif data in b'FfNn':
            return False
        elif data in b'? ':
            return None
        else:
            # Todo: return something? (But that would be misleading!)
            message = 'Illegal value for logical field: {!r}'
            raise ValueError(message.format(data))

    def parseM(self, field, data):
        """Parse memo field (M)

        Returns memo index (an integer), which can be used to look up
        the corresponding memo in the memo file.
        """
        # Memo field (index as ' '-padded text or
        # 4 byte unsigned integer little endian. The index is used
        # to look up the entry in the memo file.)
        if len(data) == 4:
            # Todo: is this 4 bytes on every platform?
            return struct.unpack('<I', data)[0] or None
        else:
            # All spaces is a NULL value.
            if data.strip() == b'':
                return None

            # Integer as a string.
            try:
                return int(self.str(data))
            except ValueError:
                raise ValueError(
                    'Memo index is not an integer: {!r}'.format(data))

    def parseN(self, field, data):
        """Parse numeric field (N)

        Returns int, float or None if the field is empty.
        """
        try:
            return int(data)
        except ValueError:
            if not data.strip():
                return None
            else:
                # Account for , in numeric fields
                return float(data.replace(b',', b'.'))

    def parseT(self, field, data):
        """Parse time field (T)

        Returns datetime.datetime or None"""
        # Julian day (32-bit little endian)
        # Milliseconds since midnight (32-bit little endian)
        #
        # "The Julian day or Julian day number (JDN) is the number of days
        # that have elapsed since 12 noon Greenwich Mean Time (UT or TT) on
        # Monday, January 1, 4713 BC in the proleptic Julian calendar
        # 1. That day is counted as Julian day zero. The Julian day system
        # was intended to provide astronomers with a single system of dates
        # that could be used when working with different calendars and to
        # unify different historical chronologies." - wikipedia.org

        # Offset from julian days (used in the file) to proleptic Gregorian
        # ordinals (used by the datetime module)
        offset = 1721425  # Todo: will this work?

        if data.strip():
            # Note: if the day number is 0, we return None
            # I've seen data where the day number is 0 and
            # msec is 2 or 4. I think we can safely return None for those.
            # (At least I hope so.)
            #
            day, msec = struct.unpack('<LL', data)
            if day:
                dt = datetime.datetime.fromordinal(day - offset)
                delta = datetime.timedelta(seconds=msec/1000)
                return dt + delta
            else:
                return None
        else:
            return None
