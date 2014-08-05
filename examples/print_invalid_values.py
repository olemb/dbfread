"""
A field parser that returns invalid values as InvalidValue objects
instead of raising ValueError.
"""
from dbfread import DBF, FieldParser, InvalidValue

class MyFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            return InvalidValue(data)

for record in DBF('files/invalid_value.dbf', parserclass=MyFieldParser):
    for name, value in record.items():
        if isinstance(value, InvalidValue):
            print('Found {!r} in field {}'.format(
                  value, name))
