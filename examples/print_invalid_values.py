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

table = DBF('files/invalid_value.dbf', parserclass=MyFieldParser)
for i, record in enumerate(table):
    for name, value in record.items():
        if isinstance(value, InvalidValue):
            print('records[{}][{!r}] == {!r}'.format(i, name, value))
