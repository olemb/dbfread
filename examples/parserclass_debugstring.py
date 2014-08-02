"""
Custom field parser that returns a debug string.
"""
import dbfread
from dbfread.field_parser import FieldParser

class DebugFieldParser(FieldParser):
    """Field that returns a debug string for each field value."""
    def field_type_supported(self, field_type):
        # Everything is supported.
        return True

    def parse(self, field, value):
        return '<type={} value={!r}>'.format(field.type, value)

for record in dbfread.open('files/people.dbf', parserclass=DebugFieldParser):
    print(record)
