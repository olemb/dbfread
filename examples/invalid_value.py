"""
A field parser that returns invalid values as InvalidValue objects
instead of raising ValueError.
"""
import dbfread
from dbfread import FieldParser, InvalidValue

class SafeFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            return InvalidValue(data)

for record in dbfread.open('files/invalid_value.dbf',
                           parserclass=SafeFieldParser):
    print(record)

