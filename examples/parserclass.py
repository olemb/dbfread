"""
Add custom field parsing by subclassing FieldParser.
"""
import dbfread
from dbfread.field_parser import FieldParser

class MyFieldParser(FieldParser):
    def parseC(self, field, data):
        # Return strings reversed.
        return self.str(data)[::-1]

for record in dbfread.open('people.dbf', parserclass=MyFieldParser):
    print(record['NAME'])
